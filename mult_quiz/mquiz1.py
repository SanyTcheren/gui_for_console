#!/home/sany/anaconda3/bin/python
"""Multiplication quiz."""

import os
import sys
import tty
import termios
from threading import Thread
from time import sleep
from random import randint


def render(box):
    """Draw field."""
    signs = 6  # width for each cell
    os.system('clear')
    print('┏' + '━'*((signs+1)*box['n_cells']-1) + '┓')
    print('┃' + box['question'].center((signs+1)*box['n_cells']-2) + '┃')
    print('┣' + ('━'*signs + '┳')*(box['n_cells']-1) + '━'*signs + '┫')
    answers = '┃'
    for num in range(box['n_cells']):
        answers += box['answers'][num].center(signs) + '┃'
    print(answers)
    print('┗' + ('━'*signs + '┻')*(box['n_cells']-1) + '━'*signs + '┛')
    print('❍'*int(box['progress']*(signs+1)*box['n_cells']))


def ask(box):
    """Worker for thread."""
    # Настраиваем терминал в режим ввода по одной клавиши
    fdescriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fdescriptor)
    try:
        tty.setcbreak(sys.stdin.fileno())
        # Запускаем демонов
        thr_timer = Thread(target=worker_timer, args=(box,), daemon=True)
        thr_key = Thread(target=worker_key, args=(box,), daemon=True)
        box['timer_off'] = False
        thr_key.start()
        thr_timer.start()
        thr_timer.join()
    finally:
        # возврат настроек терминала
        termios.tcsetattr(fdescriptor, termios.TCSADRAIN, old_settings)


def worker_key(box):
    """Listen keyboard and put to box."""
    counter = 3  # колличество попыток
    while True:
        key = sys.stdin.read(1)
        if key in '1234567890':
            box['answers'][box['cell']] = box['answers'][box['cell']] + key
        elif ord(key) in (8, 127):
            box['answers'][box['cell']] = box['answers'][box['cell']][:-1]
# Для окончания режима ввода даных используем пробел, потому что Enter
# отключен с помощью tty.setcbreak (33 строка). Без этого не получается
# совместить отрисовку экрана и ввод данных в нужную ячейку.
        if key == ' ':
            counter -= 1
            if counter > 0:
                if not check_answer(box):
                    box['answers'][box['cell']] = ''
                else:
                    box['answers'][box['cell']] = '✠'
                    box['timer_off'] = True
                    break
            else:
                if check_answer(box):
                    box['answers'][box['cell']] = '✠'
                else:
                    box['answers'][box['cell']] = '☠'
                box['timer_off'] = True
                break


def worker_timer(box):
    """Count timer and render field."""
    counter = 0
    period = 0.25
    timer = int(box['timer'])
    while counter < timer and not box['timer_off']:
        sleep(period)
        counter += period
        box['progress'] = counter/timer
        render(box)
    if check_answer(box):
        box['answers'][box['cell']] = '✠'
    else:
        box['answers'][box['cell']] = '☠'
    render(box)


def check_answer(box):
    """Проверка ответа."""
    check = False
    if (
        box['answers'][box['cell']] == '✠' or
        box['answers'][box['cell']] == box['correct']
    ):
        check = True
    return check


def get_question():
    """Get question and correct answer."""
    first = randint(2, 9)
    second = randint(2, 9)
    correct = str(first*second)
    question = f'{first} × {second} ＝'
    return (question, correct)


def main():
    """Render field and run thread."""
    n_cells = 5
    answers = ['' for x in range(n_cells)]
    box = {'answers': answers,    # Ответы на вопросы
           'cell': 0,             # Текущая ячейка с вопросом
           'n_cells': n_cells,    # Колличество ячеек с вопросами
           'question': '',        # Вопрос
           'correct': '1',        # Правильный ответ
           'timer': 8,            # Время таймера, с
           'timer_off': False,    # Остановка таймера
           'progress': 0}         # Шкала прогресса таймера
    for cell in range(n_cells):
        question, correct = get_question()
        box['question'] = question
        box['correct'] = correct
        box['cell'] = cell
        ask(box)


if __name__ == '__main__':
    main()

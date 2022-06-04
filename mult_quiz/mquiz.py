#!/home/sany/anaconda3/bin/python
"""Multiple quiz."""

import tty
import termios
import argparse
from os import system
from sys import stdin
from random import randint
from time import sleep
from threading import Thread
from functools import reduce


class Render:
    """Render field."""

    _true = '☑'
    _false = '☐'
    _full = '▓'
    _width = 22
    answer = ''
    question = ''
    archive = []

    def set_ques_arch(self, quest_arch):
        """Set question and archive."""
        self.question = quest_arch[0]
        self.archive = quest_arch[1]

    def set_input(self, user_answer):
        """Set answer."""
        self.answer = user_answer

    def arch_to_str(self):
        """Transform archive to string and resize width."""
        result = ''
        for note in self.archive:
            temp = self._true if note else self._false
            result += temp
        if len(result) > self._width:
            self._width = len(result)

        return result

    def pr_to_str(self, progress):
        """Transform progress to string."""
        length = int(progress*self._width)
        return (self._full*length).ljust(self._width)

    def render(self, progress):
        """Render field."""
        system('clear')
        arch = self.arch_to_str()
        print('╔' + '═'*self._width + '╗')
        print('║' + arch.ljust(self._width) + '║')
        print('╟' + '─'*self._width + '╢')
        print('║' + (self.question + self.answer).ljust(self._width) + '║')
        print('╟' + '─'*self._width + '╢')
        print('║' + self.pr_to_str(progress) + '║')
        print('╚' + '═'*self._width + '╝')
        print("hit SPACE if you're done")


class Question:
    """Question for quiz."""

    question = ''
    answer = ''
    archive = []
    result = None
    _min = 2
    _max = 9

    def __init__(self, n_min, n_max):
        """Create question with range."""
        self._min = n_min
        self._max = n_max

    def check(self, user_answer):
        """Check answer."""
        self.result = user_answer == self.answer
        return self.result

    def next(self):
        """Create new question."""
        if self.result is not None:
            self.archive.append(self.result)
        num1 = randint(self._min, self._max)
        num2 = randint(self._min, self._max)
        self.answer = str(num1*num2)
        self.question = f'{num1} × {num2} = '
        return (self.question, self.archive)


class Asker:
    """Asker for quiz."""

    answer = ''
    _timer_sleep = 0.1
    _timer_on = True

    def __init__(self, timer, count):
        """Initialize asker."""
        self.timer = timer
        self.count = count

    def thr_timer(self, render):
        """Render quiz with progress of timer."""
        steps = 0
        while self._timer_on and steps <= self.timer:
            progress = steps/self.timer
            render(progress)
            sleep(self._timer_sleep)
            steps += self._timer_sleep
        render(1)

    def thr_input(self, check, set_input):
        """Input for quiz, control count answer."""
        steps = 0
        result = False
        while True:
            key = stdin.read(1)
            if key in '1234567890':
                self.answer += key
            elif ord(key) in (8, 127):
                self.answer = self.answer[:-1]
            elif key == ' ':
                steps += 1
                result = check(self.answer)
                self.answer = ''
            set_input(self.answer)
            if result or steps == self.count:
                self._timer_on = False
                break

    def ask(self, render, check, set_input):
        """Ask question."""
        self.answer = ''
        f_descriptor = stdin.fileno()
        old_settings = termios.tcgetattr(f_descriptor)
        try:
            tty.setcbreak(f_descriptor)
            thr_timer = Thread(
                target=self.thr_timer,
                args=(render,),
                daemon=True
            )
            thr_input = Thread(
                target=self.thr_input,
                args=(check, set_input),
                daemon=True
            )
            self._timer_on = True
            thr_input.start()
            thr_timer.start()
            thr_timer.join()
        finally:
            termios.tcsetattr(
                f_descriptor,
                termios.TCSADRAIN,
                old_settings
            )


class Quiz:
    """My quiz."""

    def __init__(self, asker, question, render):
        """Initialize my quiz."""
        self.asker = asker
        self.question = question
        self.render = render

    def run(self, number):
        """Run quiz."""
        while number > 0:
            number -= 1
            self.render.set_ques_arch(self.question.next())
            self.asker.ask(
                self.render.render,
                self.question.check,
                self.render.set_input)
            self.render.set_input('')
        self.pr_amount()

    def pr_amount(self):
        """Print amount."""
        amount = 0
        # записываем последний ответ в архив
        _, archive = self.question.next()
        if len(archive) > 0:
            amount = reduce(lambda a, b: a + b, archive)
        amount_str = f'righ {amount}, from {len(archive)}.'
        self.render.set_ques_arch((amount_str, archive))
        self.render.set_input('')
        self.render.render(amount/len(archive))


def main(args):
    """Start programm."""
    render = Render()
    question = Question(args.n_min, args.n_max)
    asker = Asker(args.timer, args.count)
    quiz = Quiz(asker, question, render)
    while True:
        quiz.run(args.number)
        repeat = input('(r)epeat:').lower().strip()
        question.result = None
        if repeat != 'r':
            return


def create_parser():
    """Create parser for quiz."""
    parser = argparse.ArgumentParser(
        description='Multiple quiz.',
        epilog='@2022 Sany Tcheren.'
    )
    parser.add_argument('-l', '--n_min', type=int, default=2,
                        help='min number for multiple')
    parser.add_argument('-r', '--n_max', type=int, default=9,
                        help='max nubber for multiple')
    parser.add_argument('-t', '--timer', type=int, default=8,
                        help='time for answer, sec')
    parser.add_argument('-c', '--count', type=int, default=3,
                        help='count answer fo question')
    parser.add_argument('-n', '--number', type=int, default=10,
                        help='number of questions')
    return parser


if __name__ == '__main__':
    my_parser = create_parser()
    my_args = my_parser.parse_args()
    main(my_args)

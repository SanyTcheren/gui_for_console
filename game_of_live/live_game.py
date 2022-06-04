"""Игра жизнь."""
import curses
from copy import deepcopy

def greating():
    """Приветствие."""
    return(
        '''
        Добро пожаловать в игру Жизнь.
        Правило игры:
            На игровом поле распологаются живые и мертвые клетки,
            если у клетки есть три живых соседа - то на следующем ходу она оживает,
            если у клетки есть два живых соседа - то она остается живой
            все остальные умирают или остаются мертвыми
        На следующем вам необходимо задать первые клетки жизни:
            <RIGHT><LEFT><UP><DOWN>   перемещение клетки клавишами
            <A>                       установка клетки
            <S>                       переход к игре
            <Q>                       выход из игры
        Для продолжения нажмите любую клавишу
        ''')

def finish(stdscr):
    """Конец игры."""
    stdscr.addstr(0,0,'Жизнь погибла, для выхода нажмите Q, для новой жизни нажмите R')
    is_end = True
    while True:
        key = stdscr.getkey()
        if key.upper() == 'R':
            is_end = False
        if key.upper() in ['R','Q']:
            return is_end

def field_print(stdscr,field):
    """Печать игрового поля."""
    for line,string  in enumerate(field):
        for pos,val in enumerate(string):
            if val:
                stdscr.addstr(line+1, 2*pos+2, '  ',curses.color_pair(2))
            else:
                stdscr.addstr(line+1, 2*pos+2, '  ',curses.color_pair(1))

def init(stdscr):
    """Инициализация начальных условий."""
    maxyx = stdscr.getmaxyx()

    field = [[0]*int(maxyx[1]/2-2) for i in range(maxyx[0]-2)]

    coord_y = 0
    coord_x = 0
    while True:
        stdscr.clear()
        field_print(stdscr,field)
        stdscr.addstr(coord_y, coord_x, '  ', curses.color_pair(3))
        stdscr.refresh()

        key = stdscr.getkey()
        if key.upper() in ['S','Q']:
            break
        if key.upper() == 'A':
            field[coord_y-1][int(coord_x/2)-1] = not field[coord_y-1][int(coord_x/2)-1]
        elif key == 'KEY_RIGHT' and coord_x < (maxyx[1]-4):
            coord_x += 2
        elif key == 'KEY_DOWN' and coord_y < (maxyx[0]-2):
            coord_y += 1
        elif key == 'KEY_LEFT' and coord_x > 2:
            coord_x -= 2
        elif key == 'KEY_UP' and coord_y > 1:
            coord_y -= 1
    return field

def field_is_live(field):
    """Проверяет что на поле есть хоть одна живая клетка."""
    for line in field:
        for value in line:
            if value:
                return True
    return False

def field_next(field):
    """Преобразование поля для следующего шага."""
    new_field = deepcopy(field)
    for line,string in enumerate(field):
        for pos in range(len(string)):
            counter = count_lives(field,line,pos)
            if counter < 2 or counter > 3:
                new_field[line][pos] = False
            elif counter == 3:
                new_field[line][pos] = True
    return new_field

def count_lives(field,line,pos):
    """Подсчет живых клеток возле заданной."""
    counter = 0
    line_start = 0 if line == 0 else line-1
    line_end = len(field)-1 if line == len(field)-1 else line+1
    pos_start = 0 if pos == 0 else pos-1
    pos_end = len(field[0])-1 if pos == len(field[0])-1 else pos+1
    for string in range(line_start,line_end+1):
        for position in range(pos_start, pos_end+1):
            if position == pos and string == line:
                continue
            if field[string][position]:
                counter += 1
    return counter

def main(stdscr):
    """Главная функция игры Жизнь."""
    stdscr.clear()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)

    stdscr.addstr(greating())
    stdscr.getkey()

    while True:
        field = init(stdscr)
        while field_is_live(field):
            field_print(stdscr,field)
            stdscr.refresh()
            key = stdscr.getkey()
            if key.upper() == 'Q':
                break
            field = field_next(field)

        if finish(stdscr):
            break

if __name__ == '__main__':
    curses.wrapper(main)

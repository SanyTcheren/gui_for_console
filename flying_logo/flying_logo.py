"""Flying logo with curses."""

import curses
import argparse
from enum import Enum
from random import choice, randint
from threading import Thread
from time import sleep


class Score:
    """Счет в игре."""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.value = 0

    def render(self):
        """Render score."""
        value = f'SCORE:{self.value}'.ljust(10)
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height-2, width-12, value, curses.color_pair(3))

    def add(self, removed):
        """Add removed logos."""
        self.value += removed


class Direction(Enum):
    """Направления."""

    UP_RIGHT = 1
    UP_LEFT = 2
    DOWN_RIGHT = 3
    DOWN_LEFT = 4


class Logo:
    """Логотипы."""

    sign = [
        '📛', '📀', '🚀', '🛸', '⚽', '🎱', '🏀', '🌎', '🌜', '🪐', '💥', '🌟',
        '🌞', '🌍', '🤪', '👽', '💀', '👻', '⚡', '🔥', '🌕', '🌔', '💫', '🍃',
        '🪰', '🐉', '🪶', '🏈', '🪃', '🏐', '🛰', '🔨', '⛏', '🥾', '🕋', '🪂'
    ]
    speed = 5

    def __init__(self, field):
        self.field = field
        height, width = field.getmaxyx()
        self.value = choice(Logo.sign)
        self.coord = [randint(2, height-3), 2*randint(2, width//2-3)]
        self.direct = choice(list(Direction))
        self._speed_count = 0

    def __str__(self):
        return f'{self.value}:{self.coord}'

    def render(self):
        """Render alive logo, return removed."""
        removed = self._move()
        if not removed:
            self.field.addstr(self.coord[0], self.coord[1], self.value)
        return removed

    def _future(self):
        height, width = self.field.getmaxyx()
        coord = {
            self.direct == Direction.UP_RIGHT: (
                [self.coord[0]+1, self.coord[1]+2]),
            self.direct == Direction.UP_LEFT: (
                [self.coord[0]+1, self.coord[1]-2]),
            self.direct == Direction.DOWN_LEFT: (
                [self.coord[0]-1, self.coord[1]-2]),
            self.direct == Direction.DOWN_RIGHT: (
                [self.coord[0]-1, self.coord[1]+2])
        }[True]
        coord[0] = coord[0] if coord[0] > 0 else 0
        coord[0] = coord[0] if coord[0] < height-1 else height-1
        coord[1] = coord[1] if coord[1] > 0 else 0
        coord[1] = coord[1] if coord[1] < width-2 else width-2
        return coord

    def _rotate(self, line):
        self.direct = {
            self.direct == Direction.UP_RIGHT: (
                Direction.UP_LEFT if line else Direction.DOWN_RIGHT),
            self.direct == Direction.UP_LEFT: (
                Direction.UP_RIGHT if line else Direction.DOWN_LEFT),
            self.direct == Direction.DOWN_LEFT: (
                Direction.DOWN_RIGHT if line else Direction.UP_LEFT),
            self.direct == Direction.DOWN_RIGHT: (
                Direction.DOWN_LEFT if line else Direction.UP_RIGHT)
        }[True]

    def _move(self):
        height, width = self.field.getmaxyx()
        if self._speed_count >= Logo.speed:
            self._speed_count = 0
            coord = self._future()
            self.coord = coord
            if coord[1]-1 < 0 or coord[1]+2 >= width:
                self._rotate(1)
            if coord[0]-1 < 0 or coord[0]+1 >= height:
                self._rotate(0)
        else:
            self._speed_count += 1
        return self.coord in [
            [0, 0],
            [0, width-2],
            [height-1, 0],
            [height-1, width-2]]

    def bump(self, logos):
        """Обработка столкновений."""
        if self._speed_count == 0:  # Обрабатываем только после движения лого
            for logo in logos:
                if (
                    logo.coord[0] == self.coord[0] and
                    logo.coord[1] in [self.coord[1]-2, self.coord[1]+2]
                ):
                    self._rotate(1)
                if (
                    logo.coord[1] == self.coord[1] and
                    logo.coord[0] in [self.coord[0]-1, self.coord[0]+1]
                ):
                    self._rotate(0)

    @staticmethod
    def faster():
        """Ускорение лого."""
        if Logo.speed > 1:
            Logo.speed -= 1

    @staticmethod
    def slower():
        """Замедление лого."""
        Logo.speed += 1


class ListLogo():
    """List logos."""

    def __init__(self, field):
        self.field = field
        self.logos = [Logo(field)]

    def add(self):
        """Add logo."""
        self.logos.append(Logo(self.field))

    def render(self):
        """Render list of logo."""
        removed = []
        for logo in self.logos:
            remove = logo.render()
            if remove:
                removed.append(logo)
        for logo in removed:
            self.logos.remove(logo)
        return len(removed)

    def bump(self):
        """Обработка столкновений."""
        for logo in self.logos:
            logo.bump(self.logos)


class Button:
    """Button."""

    def __init__(self, value, func, selected=False):
        self.value = value
        self.action = func
        self.selected = selected

    def toggle(self):
        """Переключение кнопки."""
        self.selected = not self.selected

    def execute(self):
        """Выполняем коллбек."""
        self.action()


class GroupButton:
    """Группа кнопок."""

    def __init__(self, stdscr, button):
        self.stdscr = stdscr
        button.selected = True
        self.buttons = [button]
        self.selected = 0

    def render(self):
        """Render group of buttons."""
        height, _ = self.stdscr.getmaxyx()
        column = 2
        for button in self.buttons:
            pair = 2 if button.selected else 3
            self.stdscr.addstr(
                height-2, column,
                button.value,
                curses.color_pair(pair))
            column += 1 + len(button.value)

    def add(self, buttons):
        """Add button in group."""
        for button in buttons:
            self.buttons.append(button)

    def next(self):
        """Выбор следующий кнопки из списка."""
        self.buttons[self.selected].toggle()
        self.selected = (
            self.selected+1 if self.selected < len(self.buttons)-1 else 0)
        self.buttons[self.selected].toggle()

    def back(self):
        """Выбор предыдущей кнопки."""
        self.buttons[self.selected].toggle()
        self.selected = (
            self.selected-1 if self.selected > 0 else len(self.buttons)-1)
        self.buttons[self.selected].toggle()

    def push(self):
        """Нажатие на кнопку."""
        self.buttons[self.selected].execute()


class FlyApp:
    """Base class."""

    phase = 0.01  # Частота обновления экрана

    def __init__(self, stdscr, height, width):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)

        stdscr.resize(height+4, width+4)
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(4))

        field = stdscr.subwin(height, width, 1, 2)
        field.bkgd(' ', curses.color_pair(3))

        self.stdscr = stdscr
        self.field = field
        self.app_live = True
        self.score = Score(stdscr)
        self.logos = ListLogo(field)

        b_add = Button(' ADD+ ', self.logos.add)
        b_group = GroupButton(stdscr, b_add)
        b_next = Button(' FAST ', Logo.faster)
        b_back = Button(' SLOW ', Logo.slower)
        b_quit = Button(' QUIT ', self.quit)
        b_group.add([b_next, b_back, b_quit])
        self.buttons = b_group

    def quit(self):
        """Выход из симуляции."""
        self.app_live = False

    def _field_clear(self):
        """Перед каждой отрисовкой стираем поле."""
        height, width = self.field.getmaxyx()
        # field.clear() - будет глючить
        for line in range(height):
            self.field.addstr(line, 0, ' '*(width-1))
        self.field.addstr(0, 0, '☬')
        self.field.addstr(height-1, 0, '☫')
        self.field.addstr(0, width-2, '☣')
        self.field.addstr(height-1, width-2, '☢')

    def _render(self):
        while self.app_live:
            self._field_clear()

            removed = self.logos.render()
            self.logos.bump()
            self.score.add(removed)
            self.score.render()

            self.field.noutrefresh()
            self.stdscr.noutrefresh()
            curses.doupdate()
            sleep(FlyApp.phase)

    def _input(self):
        while self.app_live:
            self.buttons.render()
            key = self.field.getch()
            if key in [10, 32]:  # ENTER, SPACE
                self.buttons.push()
            elif key == 68:  # L_ARROW
                self.buttons.back()
            elif key == 67:  # R_ARROW
                self.buttons.next()

    def run(self):
        """Запуск тредов с отрисовкой и обработкой клавиатуры."""
        thr_render = Thread(target=self._render, daemon=True)
        thr_input = Thread(target=self._input, daemon=True)
        thr_render.start()
        thr_input.start()
        thr_render.join()


def main(stdscr, height=5, width=40):
    """Flying logo with curses."""
    height = 5 if height is None else height if height > 5 else 5
    width = 40 if width is None else 2*(width//2) if width > 40 else 40
    fly_app = FlyApp(stdscr, height, width)
    fly_app.run()


def create_parser():
    """Create parser."""
    parser = argparse.ArgumentParser(
        description='Летающие логотипы.',
        epilog='@2022 Sany Tcheren.'
    )
    parser.add_argument('-l', '--height', type=int,
                        help="field's height")
    parser.add_argument('-w', '--width', type=int,
                        help="field's width")
    return parser


if __name__ == '__main__':
    my_parser = create_parser()
    my_namespace = my_parser.parse_args()
    curses.wrapper(main, my_namespace.height, my_namespace.width)

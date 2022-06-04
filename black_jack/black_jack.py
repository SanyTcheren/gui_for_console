#!/home/sany/anaconda3/bin/python
"""Black Jack CLI game."""

import argparse
import curses
from copy import deepcopy
from random import shuffle

RULES = """Rules:
    Try to get as close to 21 without going over.
    Kings, Queens, and Jacks are worth 10 points.
    Aces are worth 1 or 11 points.
    Cards 2 through 10 are worth their face value.
    (H)it to take another card.
    (S)tand to stop taking cards.
    On your first play, you can (D)ouble down to increase your bet
    but must hit exactly one more time before standing.
    In case of a tie, the bet is returned to the player.
    The dealer stops hitting at 17."""


class Score():
    """Score for black jack."""

    def __init__(self, amount, bet):
        """Initialize score."""
        self.amount = amount
        self.default_bet = bet
        self.bet = 0
        self.bills = [['', '']]*100

    def move(self):
        """Move before next round."""
        self.bet = self.default_bet
        self.amount = self.amount - self.bet

    def double(self):
        """Double bet."""
        self.amount = self.amount - self.bet
        self.bet = self.bet + self.bet

    def add_bill(self, bill):
        """Add bill to bills."""
        self.bills.append(bill)

    def refresh_bills(self, bill):
        """Refresh last bill."""
        self.bills.pop()
        self.bills.append(bill)

    def referee(self, result):
        """Referee game by result."""
        if result == 'win':
            self.amount += 2*self.bet
        if result == 'tie':
            self.amount += self.bet
        self.bet = 0


class Deck():
    """Deck of 52 cards for black jack."""

    suits = ['♥', '♦', '♣', '♠']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A']

    def __init__(self):
        """Create deck."""
        self.deck = [Card(value, suit)
                     for value in self.values
                     for suit in self.suits]

    def get_card(self):
        """Get one card."""
        return self.deck.pop()

    def shuflle(self):
        """Shufle deck."""
        shuffle(self.deck)


class Card():
    """Card for black jack."""

    red_suits = ['♥', '♦']
    black_suits = ['♣', '♠']
    number_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    ten_values = ['J', 'D', 'K']
    ace_values = ['A']
    pattern_close = [
        '╔═══╗',
        '║╳╳╳║',
        '║╳╳╳║',
        '║╳╳╳║',
        '╚═══╝'
    ]

    def __init__(self, value, suit):
        """Initiaization card."""
        self.value = value
        self.suit = suit
        self.pattern_open = [
            '╔═══╗',
            '║' + f'{value}'.ljust(3) + '║',
            f'║ {suit} ║',
            '║' + f'{value}'.rjust(3) + '║',
            '╚═══╝'
        ]

    def get_close(self):
        """Return lines of close card."""
        return self.pattern_close

    def get_open(self):
        """Return lines of open card."""
        return self.pattern_open


class Hands():
    """Player for black jack."""

    def __init__(self, name):
        """Create player."""
        self.name = name
        self.cards = []

    def reset(self):
        """Reset cards."""
        self.cards = []

    def put_card(self, card):
        """Put card in hand."""
        self.cards.append(card)

    def score(self):
        """Count score."""
        score = 0
        aces = 0
        for card in self.cards:
            if card.value in card.number_values:
                score += int(card.value)
            elif card.value in card.ten_values:
                score += 10
            elif card.value in card.ace_values:
                score += 11
                aces += 1
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score


def pr_field(stdscr, score, width, height, closed):
    """Return string with field amount and bet."""
    amount = score.amount
    bet = score.bet
    bills = deepcopy(score.bills)
    lines = []
# Render Header
    lines.append(
        '┏' + '━'*int((width-4)/2) + '━┳' + '━'*int((width-4)/2) + '┓')
    lines.append(
        '┃' + f'AMOUNT:{amount}'.center(int((width-4)/2), ' ') + ' ┃' +
        f'BET:{bet}'.center(int((width-4)/2), ' ') + '┃')
    lines.append(
        '┣' + '━'*int((width-4)/2) + '━┻' + '━'*int((width-4)/2-6) + '┳━━┯━━┫')
# Render Main
    height -= 2
    bill = list(bills.pop())
    if closed:
        bill[0] = '╳╳'
    lines.append('┃' + ' '*(width - 8) + '┃' + f'{bill[0]}'.center(2) +
                 '│' + f'{bill[1]}'.center(2) + '┃')
    lines.append('┃' + ' '*(width - 8) + '┠──┼──┨')
    while height > 0:
        height -= 1
        bill = bills.pop()
        lines.append('┃' + ' '*(width - 8) + '┃' + f'{bill[0]}'.center(2) +
                     '│' + f'{bill[1]}'.center(2) + '┃')
# Render Footer
    lines.append('┣' + '━'*(width-8) + '┻━━┷━━┫')
    lines.append(
        '┃' + '(H)it (S)tand (D)ouble (Q)uit'.center(width - 2, ' ') + '┃')
    lines.append('┗' + '━'*(width - 2) + '┛')
    stdscr.addstr('\n'.join(lines), curses.color_pair(1))


def pr_card(stdscr, card, y_start, x_start, closed=False):
    """Print card on field."""
    lines = card.get_open()
    color = 2 if card.suit in card.black_suits else 3
    if closed:
        lines = card.get_close()
        color = 1
    for line in lines:
        stdscr.addstr(y_start, x_start, line, curses.color_pair(color))
        y_start += 1


def init_game(stdscr):
    """Initialise game."""
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_GREEN)
    height = 10
    width = 50
    x_start = 2
    x_delta = 6
    y_diller = 3
    y_player = 8

    def render(cards, score, closed=True):
        """Drawing field and card."""
        nonlocal stdscr, width, height, x_start, x_delta, y_diller, y_player
        stdscr.clear()
        pr_field(stdscr, score, width, height, closed)
        pr_card(stdscr, cards['diller'][0], y_diller, x_start, closed)
        count = 1
        for card in cards['diller'][1:]:
            pr_card(
                stdscr, card, y_diller,
                x_start + x_delta * count)
            count += 1
        count = 0
        for card in cards['player']:
            pr_card(
                stdscr, card, y_player,
                x_start + x_delta * count)
            count += 1

    return render


def check_win(player, diller):
    """Check win in black jack."""
    p_score = player.score()
    d_score = diller.score()
    if p_score > 21:
        result = 'lose'
    elif d_score > 21:
        result = 'win'
    elif p_score > d_score:
        result = 'win'
    elif p_score < d_score:
        result = 'loss'
    elif d_score == p_score:
        result = 'tie'
    return result


def pr_result(stdscr, result):
    """Add to field result game."""
    stdscr.addstr(0, 22, '╔═════╗', curses.color_pair(2))
    stdscr.addstr(1, 22, f'║{result[:3].upper().center(5)}║',
                  curses.color_pair(2))
    stdscr.addstr(2, 22, '╚═════╝', curses.color_pair(2))


def game(stdscr, amount, bet):
    """Game in Black Jack with start amount."""
    render = init_game(stdscr)

    diller = Hands('diller')
    player = Hands('player')
    score = Score(amount, bet)

    game_live = True
    while game_live:
        deck = Deck()
        score.move()

        deck.shuflle()
        diller.reset()
        player.reset()
        diller.put_card(deck.get_card())
        diller.put_card(deck.get_card())
        player.put_card(deck.get_card())
        player.put_card(deck.get_card())

        score.add_bill([diller.score(), player.score()])
        cards = {'diller': diller.cards, 'player': player.cards}

        render(cards, score)
        while game_live:
            key = stdscr.getkey()
            if key.upper() == 'Q':
                game_live = False
            elif key.upper() == 'H':
                player.put_card(deck.get_card())
                score.refresh_bills([diller.score(), player.score()])
            elif key.upper() == 'S':
                break
            elif key.upper() == 'D':
                score.double()
                player.put_card(deck.get_card())
                score.refresh_bills([diller.score(), player.score()])
            else:
                continue
            render(cards, score)
            if player.score() > 21:
                break
        render(cards, score, False)
        while game_live and diller.score() < 17 and player.score() <= 21:
            diller.put_card(deck.get_card())
            score.refresh_bills([diller.score(), player.score()])
            render(cards, score, False)

        result = check_win(player, diller)
        score.referee(result)
        render(cards, score, False)
        pr_result(stdscr, result)
        stdscr.getkey()


def create_parser():
    """Create parser for programm."""
    parser = argparse.ArgumentParser(
        description='Black Jack CLI application.',
        epilog='@2022 Sany Thceren.'
    )
    parser.add_argument('-r', '--rules', action='store_true',
                        help='print rules of game and exit.')
    parser.add_argument('-a', '--amount', default=1000, type=int,
                        help='Your start amount.')
    parser.add_argument('-b', '--bet', default=100, type=int,
                        help='bet in game.')
    return parser


if __name__ == '__main__':
    bj_parser = create_parser()
    bj_args = bj_parser.parse_args()
    if bj_args.rules:
        print(RULES)
    else:
        curses.wrapper(game, bj_args.amount, bj_args.bet)

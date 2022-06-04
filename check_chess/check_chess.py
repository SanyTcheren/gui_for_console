"""Check chess board for some position."""
import os
import json
from colorama import Style, Back, Fore, init
init()

def pr_board(figures,board):
    os.system('clear')
    print(Fore.BLACK, Style.BRIGHT)
    for index,line in enumerate(board):
        print('  ',end='')
        for position,figure in enumerate(line):
            back = Back.WHITE
            if index%2 != position%2:
                back = Back.BLUE
            print(back + figures.get(figure,'  ') + Back.RESET, end='')
        print()
    print(Fore.RESET + Style.RESET_ALL + Back.RESET)

def get_chess(file_json='chess.json'):
    """Get chess for print."""
    with open(file_json,'r') as file_in:
        chess = json.load(file_in)
    return chess

def check(board):
    """
    Check board.

    bking == wking == 1
    quens < 2
    bpawns < 9
    wpawns < 9
    other < 3
    bishop on other color cell
    """
    figures = (
        ["brook","bknight","bbishop","bqueen","bking","bpawn"] +
        ["wrook","wknight","wbishop","wqueen","wking","wpawn"]
    )
    map_figs = {key:0 for key in figures}
    bbishops = []
    wbishops = []
    for index,line in enumerate(board):
        for position, value in enumerate(line):
            if value == 'bbishop':
                bbishops.append((index,position))
            if value == 'wbishop':
                wbishops.append((index,position))
            if value in figures:
                map_figs[value] += 1
    if map_figs['bking'] != 1:
        print('Error! On the board more then 1 or no bking')
        return False
    if map_figs['wking'] != 1:
        print('Error! On the board more then 1 or no wking')
        return False
    if map_figs['bpawn'] > 8:
        print('Error! On the board more then 8 bpawn')
        return False
    if map_figs['wpawn'] > 8:
        print('Error! On the board more then 8 wpawn')
        return False
    for fig in ['bqueen','wqueen']:
        if map_figs[fig] > 1:
            print(f'Error! On the board more then 1 {fig}')
            return False
    for fig in ['brook','bbishop','bknight','wrook','wbishop','wknight']:
        if map_figs[fig] > 2:
            print(f'Error! On the board more then 2 {fig}')
            return False
    if map_figs['bbishop'] == 2:
        if (bbishops[0][0]%2 == bbishops[0][1]%2) == (bbishops[1][0]%2 == bbishops[1][1]%2):
            print('Error! Bbishops on same color cells.')
            return False
    if map_figs['wbishop'] == 2:
        if (wbishops[0][0]%2 == wbishops[0][1]%2) == (wbishops[1][0]%2 == wbishops[1][1]%2):
            print('Error! Wbishops on same color cells.')
            return False
    return True



def main(board={}):
    """Get chess board and check it."""
    chess = get_chess()
    figures = chess['figures']
    if board == {}:
        board = chess['board']
    pr_board(figures,board)
    check(board)

if __name__ == '__main__':
    main()

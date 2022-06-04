"""TicToc game."""
import os
from sys import stderr

clear = lambda: os.system('clear')

def pr_board(board):
    """Print game borad."""
    clear()
    moves = board.copy()
    for cell,value in moves.items():
        if value == ' ':
            moves[cell] = cell
        else:
            moves[cell] = ' '
    print('┌───┬───┬───┐┌───┬───┬───┐')
    print(f'│ {moves["7"]} │ {moves["8"]} │ {moves["9"]} ││ {board["7"]} │ {board["8"]} │ {board["9"]} │')
    print('├───┼───┼───┤├───┼───┼───┤')
    print(f'│ {moves["4"]} │ {moves["5"]} │ {moves["6"]} ││ {board["4"]} │ {board["5"]} │ {board["6"]} │')
    print('├───┼───┼───┤├───┼───┼───┤')
    print(f'│ {moves["1"]} │ {moves["2"]} │ {moves["3"]} ││ {board["1"]} │ {board["2"]} │ {board["3"]} │')
    print('└───┴───┴───┘└───┴───┴───┘')

def move_player(player, board):
    """Get move and change board."""
    while True:
        cell = input(f'{player}: ')
        if cell not in '123456789' or board.get(cell) != ' ':
            print('Error! Choose a free cell!', file=stderr)
            continue
        break
    board[cell] = player

def check_winner(player,board):
    """Find and get winner."""
    win_cells = ['123', '456', '789', '147', '258', '369', '159', '357']
    for cells in win_cells:
        if player==board[cells[0]]==board[cells[1]]==board[cells[2]]:
            return True
    return False

def check_moves(board):
    """Check available moves."""
    for cell in board.values():
        if cell == ' ':
            return True
    return False

def main():
    """Play in tic-tac"""
    players=['╳','●']
    game_live = True
    board = {str(x):' ' for x in range(1,10)}
    while game_live:
        for player in players:
            pr_board(board)
            move_player(player,board)
            if check_winner(player,board):
                game_live = False
                pr_board(board)
                print(f'{player} WIN!')
                break
            if not check_moves(board):
                game_live = False
                pr_board(board)
                print('DRAW!')
                break
    key = input('(q)uit?: ')
    if key.lower() != 'q':
        main()

if __name__ == '__main__':
    main()



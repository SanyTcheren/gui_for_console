"""Tests for check_chess."""

import json
import check_chess

def main():
    with open('boards.json','r') as file:
        boards = json.load(file)
    print(boards)
    check_chess.main(boards['board1'])

if __name__ == '__main__':
    main()

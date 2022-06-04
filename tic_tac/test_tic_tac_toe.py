"""Tests for tic_tac_toe."""

import unittest
import tic_tac_toe as ttt

class TestTTT(unittest.TestCase):

    def test_check_winner(self):
        players=['╳','●']
        win_cells = ['123', '456', '789', '147', '258', '369', '159', '357']
        board = {str(x):' ' for x in range(1,10)}
        self.assertFalse(ttt.check_winner(players[0],board))

        board['1'] = players[0]
        board['2'] = players[0]
        board['6'] = players[0]
        self.assertFalse(ttt.check_winner(players[0],board))
        for cells in win_cells:
            for cell in range(1,10):
                cell = str(cell)
                board[cell] = players[0] if cell in cells else ' '
            ttt.pr_board(board)
            self.assertTrue(ttt.check_winner(players[0],board))


if __name__ == '__main__':
    unittest.main()

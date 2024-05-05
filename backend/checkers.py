from board import *

class Checkers:
    def __init__(self, p1, p2):
        self.board = Board()
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.playerSymbol = "B"

    def check_win(self):
        # Check if the game has ended and determine the winner
        pass

    def reset(self):
        # Reset the board to its initial state
        pass


def main():
    checker = Checkers(None, None)
    print(checker.board.getHash())
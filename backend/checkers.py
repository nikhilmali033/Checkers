import math
import numpy as np

class Checkers:
    def __init__(self, p1, p2):
        self.board = np.zeros((8,8), dtype='U1')
        self.initialize_board()
        self.boardHash = None
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.playerSymbol = "B"
    
    def initialize_board(self):
        for i in range(8):
            for j in range(8):
                isBlack = ((i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1))
                if (i < 3 and isBlack):
                    self.board[i,j] = "B"
                elif (i > 4 and isBlack):
                    self.board[i, j] = "R"

    def getHash(self):
        self.boardHash = str(self.board.reshape(8 * 8))
        return self.boardHash

    def check_win(self):
        # Check if the game has ended and determine the winner
        pass

    def reset(self):
        # Reset the board to its initial state
        pass


def main():
    checker = Checkers(None, None)
    print(checker.board)

if __name__ == "__main__":
    main()
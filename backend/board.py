import numpy as np
import math

class Board:
    def __init__(self):
        self.board = np.zeros((8,8))
        self.boardHash = None

    def initialize_board(self):
        for i in range(8):
            for j in range(8):
                isBlack = ((math.floor(i / 8) % 2 == 0 and (i % 8) % 2 == 0) or (math.floor(i / 8) % 2 == 1 and (i % 8) % 2 == 1))
                if (i < 3 and isBlack):
                    self.board[i,j] = "B"
                elif (i > 4 and isBlack):
                    self.board[i, j] = "R"

    def getHash(self):
        self.boardHash = str(self.board.reshape(8 * 8))
        return self.boardHash

    def reset(self):
        # Reset the board to its initial state
        pass
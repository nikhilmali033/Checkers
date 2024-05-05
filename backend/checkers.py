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

    def get_valid_moves(self, piece):
        valid_moves = []
        row, col = piece.position
        color = piece.color

        # Regular moves
        if color == "red":
            # Red pieces move upwards
            if row > 0:
                if col > 0 and self.board[row - 1][col - 1] is None:
                    valid_moves.append((row - 1, col - 1))
                if col < 7 and self.board[row - 1][col + 1] is None:
                    valid_moves.append((row - 1, col + 1))
        else:
            # Black pieces move downwards
            if row < 7:
                if col > 0 and self.board[row + 1][col - 1] is None:
                    valid_moves.append((row + 1, col - 1))
                if col < 7 and self.board[row + 1][col + 1] is None:
                    valid_moves.append((row + 1, col + 1))

        # Capturing moves
        self.get_capturing_moves(piece, row, col, valid_moves, set())

        # TODO: Handle king pieces
        # Add valid moves for king pieces (moving backwards)
        # pass
        if piece.is_king:
            if color == "red":
                if row < 7:
                    if col > 0 and self.board[row + 1][col - 1] is None:
                        valid_moves.append((row + 1, col - 1))
                    if col < 7 and self.board[row + 1][col + 1] is None:
                        valid_moves.append((row + 1, col + 1))
            if color == "black":
                if row > 0:
                    if col > 0 and self.board[row - 1][col - 1] is None:
                        valid_moves.append((row - 1, col - 1))
                    if col < 7 and self.board[row - 1][col + 1] is None:
                        valid_moves.append((row - 1, col + 1))

        return valid_moves
    
    def get_capturing_moves(self, piece, row, col, valid_moves, visited):
        color = piece.color
        opponent_color = "black" if color == "red" else "red"
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row = row + 2 * dr
            new_col = col + 2 * dc
            mid_row = row + dr
            mid_col = col + dc

            if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_row, new_col) not in visited:
                if (self.board[mid_row][mid_col] is not None and
                    self.board[mid_row][mid_col].color == opponent_color and
                    self.board[new_row][new_col] is None):

                    # Check if the movement direction is valid for the color -> only works if piece  not a king
                    if (color == 'red' and dr < 0) or (color == 'black' and dr > 0):
                        visited.add((new_row, new_col))
                        if valid_moves: #forced jumps 
                            valid_moves.clear()
                        valid_moves.append((new_row, new_col))
                        self.get_capturing_moves(piece, new_row, new_col, valid_moves, visited)

        return valid_moves


def main():
    checker = Checkers(None, None)
    print(checker.board)

if __name__ == "__main__":
    main()
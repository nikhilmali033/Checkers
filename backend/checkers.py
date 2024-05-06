import numpy as np
import math

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.is_king = False

    def __str__(self):
        if self.color == 'black':
            if self.is_king:
                return 'BK'
            else:
                return 'B'
        else:
            if self.is_king:
                return 'RK'
            else:
                return 'R'

class Board:
    def __init__(self):
        self.board = np.zeros((8,8), dtype='U1')
        self.selected_piece = None
        self.turn = "black"
        self.initialize_board()

    def get_hash(self, board):
        data = board.copy()
        hashVal = 0
        for i in data.reshape(8 * 8):
            if i == 'R':
                i = 1
            elif i == 'RK':
                i = 2
            elif i == 'B':
                i = 3
            elif i == 'BK':
                i = 4
            else:
                i = 0
            hashVal = hashVal * 3 + i
        return int(hashVal)

    def initialize_board(self):
        for i in range(8):
            for j in range(8):
                isBlack = ((i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1))
                if (i < 3 and isBlack):
                    self.board[i,j] = "B"
                elif (i > 4 and isBlack):
                    self.board[i, j] = "R"

    def get_captures_by_move(self, piece):
        captures_by_move = {}
        row, col = piece.position
        color = piece.color

        # Regular moves
        if color == "red":
            # Red pieces move upwards
            if row > 0:
                if col > 0 and self.board[row - 1][col - 1] == '':
                    captures_by_move[(row - 1, col - 1)] = []
                if col < 7 and self.board[row - 1][col + 1] == '':
                    captures_by_move[(row - 1, col + 1)] = []
        else:
            # Black pieces move downwards
            if row < 7:
                if col > 0 and self.board[row + 1][col - 1] == '':
                    captures_by_move[(row + 1, col - 1)] = []
                if col < 7 and self.board[row + 1][col + 1] == '':
                    captures_by_move[(row + 1, col + 1)] = []
        # Handle king pieces
        # Add valid moves for king pieces (moving backwards)
        if piece.is_king:
            if color == "red":
                if row < 7:
                    if col > 0 and self.board[row + 1][col - 1] == '':
                        captures_by_move[(row + 1, col - 1)] = []
                    if col < 7 and self.board[row + 1][col + 1] == '':
                        captures_by_move[(row + 1, col + 1)] = []
            if color == "black":
                if row > 0:
                    if col > 0 and self.board[row - 1][col - 1] == '':
                        captures_by_move[(row - 1, col - 1)] = []
                    if col < 7 and self.board[row - 1][col + 1] == '':
                        captures_by_move[(row - 1, col + 1)] = []
        # Capturing moves
        captures_by_move = self.get_capturing_moves(piece, row, col, captures_by_move, set())

        return captures_by_move

    def get_capturing_moves(self, piece, row, col, captures_by_move, visited=None):
        if captures_by_move is None:
            captures_by_move = {}
        if visited is None:
            visited = set()
    
        color = piece.color
        opponent_color = "B" if color == "red" else "R"
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
        for dr, dc in directions:
            new_row = row + 2 * dr
            new_col = col + 2 * dc
            mid_row = row + dr
            mid_col = col + dc
    
            if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_row, new_col) not in visited:
                if (self.board[mid_row, mid_col] != '' and
                        opponent_color in self.board[mid_row, mid_col] and
                        self.board[new_row, new_col] == ''):
                    # Check if the movement direction is valid for the color
                    if (color == 'red' and dr < 0) or (color == 'black' and dr > 0) or piece.is_king:
                        visited.add((new_row, new_col))
                        if (new_row, new_col) not in captures_by_move:
                            captures_by_move[(new_row, new_col)] = []
                        captures_by_move[(new_row, new_col)].append([(mid_row, mid_col)])
                        if (row, col) in captures_by_move:
                            captures_by_move[(new_row, new_col)].extend(captures_by_move[(row, col)])

                        # print("Before")
                        # print(captures_by_move)

                        # Continue checking for additional captures
                        captures_by_move = self.get_capturing_moves(piece, new_row, new_col, captures_by_move, visited)
                        # print("after")
                        # print(captures_by_move)
    
        return captures_by_move

    def get_next_state(self, piece, new_position, captured_pieces):
        next_state = self.board.copy()
        old_position = piece.position
        next_state[old_position[0], old_position[1]] = ''

        # Remove the captured pieces
        for piec in captured_pieces:
            for row, col in piec:
                next_state[row, col] = ''

        # Promote to king if a piece reaches the end of the board
        if piece.color == "red" and new_position[0] == 0:
            piece.is_king = True
        elif piece.color == "black" and new_position[0] == 7:
            piece.is_king = True

        # Place the piece in the new position
        next_state[new_position[0], new_position[1]] = str(piece)
        return next_state


    def check_win(self):
        if self.end is not None:
            return self.end
        
        rCount = 0
        bCount = 0

        for i in self.board.reshape(8*8):
            if i == 'R' or i == 'RK':
                rCount = rCount + 1
            elif i == 'B' or i == 'BK':
                bCount = bCount + 1
        
        if rCount == 0:
            self.winner = 'B'
            self.end = True
        elif bCount == 0:
            self.winner = 'R'
            self.end = True
        else:
            self.end = False
        
        return self.end, self.winner

    def reset(self):
        # Reset the board to its initial state
        self.board = []
        self.selected_piece = None
        self.turn = "red"
        self.initialize_board()

    def get_all_moves(self):
        for index, piece in np.ndenumerate(self.board):
            if self.turn == "black" and 'B' in piece:
                print(index)
                color = "red" if "R" in piece else "black"
                cur = Piece(color, index)
                moves = self.get_captures_by_move(cur)
                print(moves)
                for pos, captured in moves.items():
                    print(f"Moved Piece {index} to {pos}")
                    next_state = self.get_next_state(cur, pos, captured)
                    print(self.get_hash(next_state))
                    print(next_state)


def main():
    board = Board()
    board.get_all_moves()

if __name__ == "__main__":
    main()

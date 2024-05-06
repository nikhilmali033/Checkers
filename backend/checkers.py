import numpy as np
import math
from player import Player

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.is_king = False

    def __str__(self):
        if self.color == 'red':
            if self.is_king:
                return 'RK'
            else:
                return 'R'
        else:
            if self.is_king:
                return 'BK'
            else:
                return 'B'


class Board:
    def __init__(self, p1 : Player, p2 : Player, feedback=True):
        self.selected_piece = None
        self.turn = "black"
        self.initialize_board()
        self.p1 = p1
        self.p2 = p2
        self.current_player : Player = None
        self.feedback = feedback
        self.end = None
        self.winner = None

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
        self.board = np.zeros((8,8), dtype='U2')
        for i in range(8):
            for j in range(8):
                isBlack = ((i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1))
                if (i < 3 and isBlack):
                    self.board[i,j] = "B"
                elif (i > 4 and isBlack):
                    self.board[i, j] = "R"

    def get_captures_by_move(self, piece : Piece):
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
        # Handle king pieces
        if piece.is_king:
            # Move backward and forward for kings
            if color == "red":
            # Red kings can move both up and down
                if row > 0:
                    if col > 0 and self.board[row - 1][col - 1] == '':
                        captures_by_move[(row - 1, col - 1)] = []
                    if col < 7 and self.board[row - 1][col + 1] == '':
                        captures_by_move[(row - 1, col + 1)] = []
                if row < 7:
                    if col > 0 and self.board[row + 1][col - 1] == '':
                        captures_by_move[(row + 1, col - 1)] = []
                    if col < 7 and self.board[row + 1][col + 1] == '':
                        captures_by_move[(row + 1, col + 1)] = []
            elif color == "black":
            # Black kings can also move both up and down
                if row > 0:
                    if col > 0 and self.board[row - 1][col - 1] == '':
                        captures_by_move[(row - 1, col - 1)] = []
                    if col < 7 and self.board[row - 1][col + 1] == '':
                        captures_by_move[(row - 1, col + 1)] = []
                if row < 7:
                    if col > 0 and self.board[row + 1][col - 1] == '':
                        captures_by_move[(row + 1, col - 1)] = []
                    if col < 7 and self.board[row + 1][col + 1] == '':
                        captures_by_move[(row + 1, col + 1)] = []


        # Capturing moves
        captures_by_move = self.get_capturing_moves(piece, row, col, captures_by_move, set())

        return captures_by_move

    def get_capturing_moves(self, piece : Piece, row, col, captures_by_move, visited=None):
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

    def get_next_state(self, piece : Piece, new_position, captured_pieces):
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

        #if self.end is not None:
         #   return self.end, self.winner
        
        rCount = 0
        bCount = 0
        for i in self.board.reshape(8*8):
            if i == 'R' or i == 'RK':
                rCount =+ 1
            elif i == 'B' or i == 'BK':
                bCount =+ 1
        
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
        actions = []
        for index, piece in np.ndenumerate(self.board):
            if self.current_player.symbol in piece:
                # print(index) Piece Coordinate Tuple
                color = "red" if "R" in piece else "black"
                cur = Piece(color, index)
                if piece == "RK" or piece == "BK":
                    cur.is_king = True

                moves = self.get_captures_by_move(cur)
                print(moves)
                for pos, captured in moves.items():
                    # print(f"Moved Piece {index} to {pos}")
                    next_state = self.get_next_state(cur, pos, captured)
                    hash = self.get_hash(next_state)
                    # print(hash)
                    # print(next_state)
                    actions.append((hash, next_state))
            
        return actions
    
    def feedCurrentState(self):
        self.p1.feedState(self.get_hash(self.board))
        self.p2.feedState(self.get_hash(self.board))
    
    def giveReward(self, winner):
        if winner == "B":
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif winner == "R":
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)  # small reward if draw
            self.p2.feedReward(0.1)


    def play(self):
        self.reset()
        rounds = 0
        while True:
            
            if self.current_player == self.p1:
                self.current_player = self.p2
            else:
                self.current_player = self.p1
                
            print(f"It's {self.current_player.symbol}'s turn.")
            moves = self.get_all_moves()
            if len(moves) == 0:
                return 'Tie'
            
            
            hash, next_state = self.current_player.chooseAction(moves)

        
            print(next_state)
            self.board = next_state
            isEnd, winner = self.check_win()
            self.feedCurrentState()
            if isEnd:
                if self.feedback:
                    self.giveReward(winner)
                return winner
            if rounds > 500:
                return 'Tie'
            rounds = rounds + 1


def main():
    p1 = Player("B")
    p2 = Player("R")
    board = Board(p1, p2)
    winner = board.play()
    if winner == 'Tie':
        print("Game ended in a Tie")
    else:
        print(f"{winner} Won!")
    

if __name__ == "__main__":
    main()

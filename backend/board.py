import pygame
from pygame.examples.go_over_there import screen

from backend.piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.turn = "red"
        self.initialize_board()

    def initialize_board(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if row < 3 and (row + col) % 2 == 1:
                    self.board[row].append(Piece("black", (row, col)))
                elif row > 4 and (row + col) % 2 == 1:
                    self.board[row].append(Piece("red", (row, col)))
                else:
                    self.board[row].append(None)

    def get_piece(self, row, col):
        return self.board[row][col]

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
        # Capturing moves
        self.get_capturing_moves(piece, row, col, valid_moves)

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
                        if valid_moves:  # forced jumps
                            valid_moves.clear()
                        valid_moves.append((new_row, new_col))
                        self.get_capturing_moves(piece, new_row, new_col, valid_moves, visited)

        return valid_moves

    def highlight_square(self, position, color):
        row, col = position
        pygame.draw.rect(screen, color, (col * 100, row * 100, 100, 100), 4)
        pygame.display.update()

    def unhighlight_squares(self):
        self.selected_piece = None
        self.render()

    def highlight_valid_moves(self, valid_moves):
        for move in valid_moves:
            self.highlight_square(move, (255, 0, 0))  # Red color for possible moves

    def select_piece(self, row, col):
        if row is None or col is None:
            self.selected_piece = None
            self.unhighlight_squares()
        else:
            print("running")
            self.selected_piece = self.board[row][col]
            self.highlight_square(self.selected_piece.position, (255, 255, 0))  # Yellow color for selected piece
            pygame.display.update()

    def move_piece(self, piece, new_position):
        old_position = piece.position
        self.board[old_position[0]][old_position[1]] = None
        self.board[new_position[0]][new_position[1]] = piece
        piece.position = new_position

    def render(self):
        screen.fill((255, 255, 255))
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (150, 150, 150)
                pygame.draw.rect(screen, color, (col * 100, row * 100, 100, 100))
                if self.board[row][col]:
                    piece_color = (255, 0, 0) if self.board[row][col].color == "red" else (0, 0, 0)
                    pygame.draw.circle(screen, piece_color, (col * 100 + 50, row * 100 + 50), 40)
        pygame.display.flip()

    def check_win(self):
        # Check if the game has ended and determine the winner
        pass

    def reset(self):
        # Reset the board to its initial state
        pass
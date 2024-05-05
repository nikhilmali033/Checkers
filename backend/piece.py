class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.is_king = False

    def make_king(self):
        self.is_king = True
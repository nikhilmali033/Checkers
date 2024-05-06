class Judger:
    def __init__(self, p1, p2, feedback=True):
        self.p1 = p1
        self.p2 = p2
        self.feedback = feedback
        self.currentPlayer = None
        self.p1.setSymbol("B")
        self.p2.setSymbol("R")
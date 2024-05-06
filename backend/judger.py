class Judger:
    def __init__(self, p1, p2, feedback=True):
        self.p1 = p1
        self.p2 = p2
        self.feedback = feedback
        self.currentPlayer = None
        self.p1.setSymbol("B")
        self.p2.setSymbol("R")

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
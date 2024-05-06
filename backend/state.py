import numpy as np

class State:
    def __init__(self):
        self.data = np.zeros((8,8), dtype='U1')
        self.winner = None
        self.hashVal = None
        self.end = None
    
    def getHash(self):
        if self.hashVal is None:
            self.hashVal = 0
            for i in self.data.reshape(8 * 8):
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
                self.hashVal = self.hashVal * 3 + i
        return int(self.hashVal)
    
    def isEnd(self):
        if self.end is not None:
            return self.end
        
        rCount = 0
        bCount = 0

        for i in self.data.reshape(8*8):
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
        
        return self.end
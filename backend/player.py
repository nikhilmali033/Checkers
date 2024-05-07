import numpy as np
import pickle

class Player:
    def __init__(self, name, exp_rate=0.3):
            self.symbol = name
            self.states = []  # hash of all positions taken
            self.lr = 0.2
            self.exp_rate = exp_rate
            # self.decay_gamma = 0.9
            self.estimations = dict()  # state -> value
            self.loadPolicy()

    def feedState(self, state):
        self.states.append(state)


    def reset(self):
        self.states = []

    def chooseAction(self, positions):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            values = []
            for hash, state in positions:
                values.append((self.estimations.get(hash, 0), state))
            np.random.shuffle(values)
            values.sort(key=lambda x: x[0], reverse=True)
            action = values[0]
        # print("{} takes action {}".format(self.name, action))
        return action
    
    def feedReward(self, reward):
        if len(self.states) == 0:
            return
        target = reward
        for latestState in reversed(self.states):
            value = self.estimations.get(latestState, 0) + self.lr * (target - self.estimations.get(latestState, 0))
            self.estimations[latestState] = value
            target = value
        self.states = []

    def savePolicy(self):
        fw = open('optimal_policy_' + str(self.symbol), 'wb')
        pickle.dump(self.estimations, fw)
        fw.close()

    def loadPolicy(self):
        fr = open('optimal_policy_' + str(self.symbol),'rb')
        self.estimations = pickle.load(fr)
        fr.close()
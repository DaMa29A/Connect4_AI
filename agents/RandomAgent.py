import numpy as np
from .Agent import Agent

class RandomAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Random"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        if not valid_moves:
            raise Exception("No valid moves remaining.")
        return np.random.choice(valid_moves)
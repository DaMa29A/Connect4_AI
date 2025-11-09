import numpy as np
from configs.env_config import SEED

class Agent:
    def __init__(self, name, player_symbol=None):
        self.name = name
        self.player_symbol = player_symbol
        self.rng = np.random.RandomState(SEED)

    # obs -> board
    # action_mask -> available cols   
    def choose_action(self, obs, action_mask):
        raise NotImplementedError("subclass must implement 'choose_action'")
    
    def getName(self):
        return self.name

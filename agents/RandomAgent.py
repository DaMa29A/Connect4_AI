import numpy as np
from .Agent import Agent

class RandomAgent(Agent):
    def __init__(self, name="Random", player_symbol=None):
        super().__init__(name=name, player_symbol=player_symbol)

    def choose_action(self, obs, action_mask):
        valid_actions = np.where(action_mask == 1)[0]
        
        if len(valid_actions) == 0:
            raise RuntimeError("No valid actions available")  
            
        #return np.random.choice(valid_actions)
        return self.rng.choice(valid_actions)
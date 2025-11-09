import numpy as np
from .Agent import Agent
from utils.check_rules import check_attack_opportunities, is_playable

class RuleBasedL1Agent(Agent):
    def __init__(self, name="RuleBased_L1", player_symbol=None):
        super().__init__(name=name, player_symbol=player_symbol)
        if player_symbol is None:
            raise ValueError("RuleBased needs player_symbol (1 o -1).")

    def choose_action(self, obs, action_mask):
        # Get all available cols
        valid_cols = np.where(action_mask == 1)[0]
        if len(valid_cols) == 0:
            raise RuntimeError("No valid actions available") 

        # Agent symbol
        my_id = self.player_symbol

        # 1. Randomly selects one of the columns that guarantee a win. ---
        possible_win_moves = []
        attack_moves = check_attack_opportunities(obs, my_id, target_count=4)
        for r, c, _ in attack_moves:
            if is_playable(obs, r, c):
                possible_win_moves.append(c) 

        if possible_win_moves:
            valid_win_moves = [m for m in possible_win_moves if m in valid_cols]
            if valid_win_moves:
                #return np.random.choice(valid_win_moves)
                return self.rng.choice(valid_win_moves) 
                
        # 2. Random choice. ---
        #return np.random.choice(valid_cols)
        return self.rng.choice(valid_cols)
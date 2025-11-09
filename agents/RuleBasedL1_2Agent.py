import numpy as np
from .Agent import Agent
from utils.check_rules import check_attack_opportunities, is_playable

class RuleBasedL1_2Agent(Agent):
    def __init__(self, name="RuleBased_L1_2", player_symbol=None):
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
        winning_moves = check_attack_opportunities(obs, my_id, target_count=4)
        valid_win_moves = []
        for r, c, _ in winning_moves:
            if c in valid_cols and is_playable(obs, r, c):
                valid_win_moves.append(c)
        if valid_win_moves:
            #return np.random.choice(valid_win_moves)
            return self.rng.choice(valid_win_moves)

        # 2. Randomly selects one of the columns that creates a three-in-a-row threat. ---
        attack_threats = check_attack_opportunities(obs, my_id, target_count=3)
        valid_threat_moves = []
        for r, c, _ in attack_threats:
            if c in valid_cols and is_playable(obs, r, c):
                valid_threat_moves.append(c)
        if valid_threat_moves:
            #return np.random.choice(valid_threat_moves)
            return self.rng.choice(valid_threat_moves)

        # 3. Random choice. ---
        #return np.random.choice(valid_cols)
        return self.rng.choice(valid_cols)
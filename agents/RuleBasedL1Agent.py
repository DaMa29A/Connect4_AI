import numpy as np
from .Agent import Agent
from utils.check_rules import check_attack_opportunities

class RuleBasedL1Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L1"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        if not valid_moves:
            return 0 

        my_id = self.env.next_player_to_play

        # Cerca opportunità di attacco (Vittoria) ---
        possible_win_moves = [] 
        attack_moves = check_attack_opportunities(self.env.board, my_id, target_count=4)
        for r, c, _ in attack_moves:
            if self.env.is_playable_cell(r, c):
                possible_win_moves.append(c) 

        if possible_win_moves:
            return np.random.choice(possible_win_moves) 

        # Mossa casuale (Fallback) ---
        return np.random.choice(valid_moves)
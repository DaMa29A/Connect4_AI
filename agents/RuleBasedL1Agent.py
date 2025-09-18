import numpy as np
from .Agent import Agent
from utils.check_rules import check_attack_opportunities

class RuleBasedL1Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L1"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        my_id = self.env.next_player_to_play

        # Cerca opportunità di attacco
        attack_moves = check_attack_opportunities(self.env.board, my_id)
        for r, c in attack_moves:
            if self.env.is_playable_cell(r, c):
                return c

        # Altrimenti, mossa casuale
        return np.random.choice(valid_moves)
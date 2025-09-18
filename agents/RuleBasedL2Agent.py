import numpy as np
from .Agent import Agent
from env.env_config import ROWS_COUNT
from utils.check_rules import check_attack_opportunities, check_defensive_opportunities

class RuleBasedL2Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L2"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        my_id = self.env.next_player_to_play

        # 1. Mossa vincente (attacco diretto)
        winning_moves = check_attack_opportunities(self.env.board, my_id)
        for r, c in winning_moves:
            if self.env.is_playable_cell(r, c):
                return c

        # 2. Blocca mossa vincente dell’avversario
        defensive_moves = check_defensive_opportunities(self.env.board, my_id)
        for r, c in defensive_moves:
            if self.env.is_playable_cell(r, c):
                return c

        # 3. Mossa casuale
        return np.random.choice(valid_moves)

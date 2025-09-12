# import numpy as np
# from .Agent import Agent

# # Un agente che se può vincere con una mossa, la fa; altrimenti, sceglie una mossa valida a caso.
# class RuleBasedL1Agent(Agent):
#     def __init__(self, env):
#         super().__init__(env)
#         self.name = "Rule-Based L1"

#     def choose_action(self):
#         valid_moves = self.env.get_valid_actions()

#         for move in valid_moves:
#             simulated_env = self.env.clone()
#             simulated_env.play_action(move)
#             row = simulated_env.last_move_row
#             col = simulated_env.last_move_col

#             if simulated_env.check_win_around_last_move(row, col):
#                 return move  # Mossa vincente trovata

#         # Nessuna mossa vincente, scegli casualmente
#         return np.random.choice(valid_moves)

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
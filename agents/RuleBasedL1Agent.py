import numpy as np
from .Agent import Agent

class RuleBasedL1Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L1"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()

        for move in valid_moves:
            simulated_env = self.env.clone()
            simulated_env.play_action(move)
            row = simulated_env.last_move_row
            col = simulated_env.last_move_col

            if simulated_env.check_win_around_last_move(row, col):
                return move  # 🏆 Mossa vincente trovata

        # 🎲 Nessuna mossa vincente, scegli casualmente
        return np.random.choice(valid_moves)

    def getName(self):
        return self.name

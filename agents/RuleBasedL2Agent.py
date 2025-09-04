import numpy as np
from .Agent import Agent
from env.env_config import ROWS_COUNT

class RuleBasedL2Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L2"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        my_id = self.env.next_player_to_play
        opponent_id = -my_id

        # Cerca mossa vincente per sé
        for move in valid_moves:
            simulated_env = self.env.clone()
            simulated_env.play_action(move)
            row = simulated_env.last_move_row
            col = simulated_env.last_move_col
            if simulated_env.check_win_around_last_move(row, col):
                return move  # Vinci subito

        # Blocca mossa vincente dell’avversario
        for move in valid_moves:
            simulated_env = self.env.clone()
            # Simula la mossa dell’avversario direttamente sulla board
            for r in range(ROWS_COUNT - 1, -1, -1):
                if simulated_env.board[r, move] == 0:
                    simulated_env.board[r, move] = opponent_id
                    simulated_env.last_move_row = r
                    simulated_env.last_move_col = move
                    break
            if simulated_env.check_win_around_last_move(simulated_env.last_move_row, simulated_env.last_move_col):
                return move  # Blocca l’avversario

        # Nessuna urgenza, mossa casuale
        return np.random.choice(valid_moves)
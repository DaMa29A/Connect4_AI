import numpy as np
from .Agent import Agent
from utils.check_rules import check_attack_opportunities, check_defensive_opportunities

class RuleBasedL2Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L2"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        # Handle the case where there are no valid moves
        if not valid_moves:
            return 0

        my_id = self.env.next_player_to_play

        # Mossa vincente (target_count=4) ---
        possible_win_moves = []
        winning_moves = check_attack_opportunities(self.env.board, my_id, target_count=4)
        for r, c, _ in winning_moves:
            if self.env.is_playable_cell(r, c):
                possible_win_moves.append(c) 

        if possible_win_moves:
            return np.random.choice(possible_win_moves) 

        # Blocca mossa vincente dell’avversario (target_count=4) ---
        possible_defense_moves = []
        defensive_moves = check_defensive_opportunities(self.env.board, my_id, target_count=4)
        for r, c, _ in defensive_moves:
            if self.env.is_playable_cell(r, c):
                possible_defense_moves.append(c)

        if possible_defense_moves:
            return np.random.choice(possible_defense_moves)

        # Mossa casuale ---
        # If no winning or blocking moves were found
        return np.random.choice(valid_moves)
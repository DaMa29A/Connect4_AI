import numpy as np
from .Agent import Agent
from utils.check_rules import check_attack_opportunities

class RuleBasedL1Agent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Rule-Based L1"

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        # Handle the case where there are no valid moves (shouldn't happen in a normal game end)
        if not valid_moves:
            return 0 

        my_id = self.env.next_player_to_play

        # --- Livello 1: Cerca opportunità di attacco (Vittoria) ---
        possible_win_moves = [] # Initialize list to gather winning moves
        attack_moves = check_attack_opportunities(self.env.board, my_id, target_count=4)
        for r, c, _ in attack_moves:
            if self.env.is_playable_cell(r, c):
                possible_win_moves.append(c) # Gather all valid winning columns

        # If any winning moves were found...
        if possible_win_moves:
            # Randomly choose one of them
            return np.random.choice(possible_win_moves) 

        # --- Livello 2: Mossa casuale (Fallback) ---
        # If no winning moves were found, play a random valid move
        return np.random.choice(valid_moves)
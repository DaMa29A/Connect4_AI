import numpy as np
from .Agent import Agent
from gui.gui_rend import check_gui_event
from env.env_config import COLUMNS_COUNT

class HumanAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Human"

    def choose_action(self):
        if self.env.render_mode == "console":
            while True:
                try:
                    col = int(input(f"Enter your move (0-{COLUMNS_COUNT - 1}): "))
                    if self.env.is_action_valid(col):
                        return col
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a valid integer.")
                    
        elif self.env.render_mode == "gui":
            while True:
                col = check_gui_event()
                if col is not None and self.env.is_action_valid(col):
                    return col
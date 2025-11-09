import numpy as np
from .Agent import Agent
from configs.env_config import COLUMNS_COUNT
from colorama import Fore, Style, init
init(autoreset=True)

class HumanAgent(Agent):
    def __init__(self, name = "Human", render_mode = None, player_symbol=None):
        super().__init__(name=name, player_symbol=player_symbol)
        self.render_mode = render_mode

    def choose_action(self, obs, action_mask):
        if self.render_mode == "console":
            while True:
                try:
                    prompt = f"{Fore.CYAN}{self.name}, choose your column (0-{COLUMNS_COUNT - 1}): {Style.RESET_ALL}"
                    col_str = input(prompt)
                    col = int(col_str)
                    
                    if not (0 <= col < COLUMNS_COUNT):
                        print(f"{Fore.RED}Error: Please enter a number between 0 and {COLUMNS_COUNT - 1}.")
                    elif not action_mask[col]:
                        print(f"{Fore.RED}Error: Column {col} is full.")
                    else:
                        return col
                        
                except ValueError:
                    print(f"{Fore.RED}Error: Please enter an integer only.")
                    
        elif self.render_mode == "gui":
            print("[Implementation in play.py]")
            pass
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from colorama import Fore, Style, init
init(autoreset=True)
from configs.env_config import ROWS_COUNT, COLUMNS_COUNT, REWARDS
from utils.check_rules import is_block_triplet, is_a_triplet, is_a_quadruplet, is_a_pair, is_block_pair
from gui.gui_rend import Connect4GUIRenderer
from agents.Agent import Agent 
from utils.BoardStats import BoardStats


class Connect4Env(gym.Env):
    metadata = {"render_modes": ["console", "gui"], "render_fps": 1}

    def __init__(self, opponent_class=None, render_mode=None, who_am_i=1, first_move_random=False, self_play=False, model_path=None):
        super().__init__()
        
        if render_mode and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Invalid render_mode: {render_mode}")
            
        self.render_mode = render_mode
        self.first_move_random = first_move_random
        self.self_play = self_play
        
        if self.self_play:
            opponent_class = None 
            
        self.who_am_i = who_am_i 
        self.agent_player_symbol = self.who_am_i
        self.opponent_player_symbol = -self.who_am_i
        
        self.first_player_to_move = 1
        self.next_player_to_play = self.first_player_to_move
        
        self.opponent = None
        if opponent_class is not None:
            class_name = opponent_class.__name__
            if class_name == "DQNAgent" or class_name == "PPOAgent":
                self.opponent = opponent_class(player_symbol=self.opponent_player_symbol, model_path=model_path)
            else:
                self.opponent = opponent_class(player_symbol=self.opponent_player_symbol) 

        self.action_space = spaces.Discrete(COLUMNS_COUNT)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32
        )

        self.board = np.zeros((ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32)
        self.last_move_row = None
        self.last_move_col = None
        self.winner = None
        self.terminated = False

        self.board_stats = BoardStats()

        self.gui_renderer = None
        if self.render_mode == "gui":
            self.gui_renderer = Connect4GUIRenderer()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed) 
        
        self.board = np.zeros((ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32)
        self.next_player_to_play = self.first_player_to_move
        self.last_move_row = None
        self.last_move_col = None
        self.winner = None
        self.terminated = False
        
        self.board_stats.reset() 
        
        # If the opponent (X) moves first
        if self.opponent is not None and self.agent_player_symbol == -1:
            self._play_opponent_move(is_first_move=True)
            self.board_stats.update_after_move(self.board, self.last_move_row, self.last_move_col, self.opponent_player_symbol)

        if self.render_mode:
            self.render()
            
        return self.get_board(), self.get_info()
    
    # Returns standard information, including the action mask.
    def get_info(self):
        return {"action_mask": self.get_action_mask()}

    def step(self, action):
        is_first_move_of_game = np.all(self.board == 0)
        
        if is_first_move_of_game and self.next_player_to_play == 1 and self.first_move_random:
             action = int(self.np_random.choice(self.get_valid_actions()))
        else:
             action = int(action)

        # Invalid move - END GAME
        if not self.is_action_valid(action):
            self.terminated = True
            self.winner = -self.next_player_to_play
            reward = REWARDS["invalid"]
            
            info = self.get_info()
            info["reward"] = reward
            info["last_move_row"] = -1 # Not valid
            info["last_move_col"] = action
            info["board_stats"] = self.board_stats
            
            return self.get_board(), reward, self.terminated, False, info
        
        # # Invalid move - RETRY
        # if not self.is_action_valid(action):
        #     reward = REWARDS["invalid"]
        #     info = self.get_info()
        #     self.terminated = False
        #     info["reward"] = reward
        #     info["last_move_row"] = -1 # Not valid
        #     info["last_move_col"] = action
        #     info["board_stats"] = self.board_stats
            
        #     return self.get_board(), reward, self.terminated, False, info

        # Play move
        player_making_move = self.next_player_to_play
        self._play_action(action, player_making_move)
        
        self.board_stats.update_after_move(self.board, self.last_move_row, self.last_move_col, player_making_move)
       
        self.terminated = self._is_finish()
        self.winner = self.get_winner()
        reward = self._calculate_reward(player_making_move)
        
        # Next round
        if not self.terminated:
            self.switch_player()

            # If opponent exists (training)
            if self.opponent is not None:
                self._play_opponent_move(is_first_move=False)
                
                self.board_stats.update_after_move(self.board, self.last_move_row, self.last_move_col, self.opponent_player_symbol)
                
                self.terminated = self._is_finish()
                self.winner = self.get_winner()
                
                if self.terminated:
                    reward = self._calculate_reward(self.opponent_player_symbol)
                
                if not self.terminated:
                    self.switch_player()

        if self.render_mode:
            self.render()
            
        info = self.get_info()
        info["reward"] = reward
        info["last_move_row"] = self.last_move_row
        info["last_move_col"] = self.last_move_col
        info["board_stats"] = self.board_stats
      
        return self.get_board(), reward, self.terminated, False, info
    
    def _play_opponent_move(self, is_first_move=False):
        obs = self.get_board()
        mask = self.get_action_mask()
        
        if is_first_move and self.first_move_random:
            action = int(self.np_random.choice(self.get_valid_actions()))
        else:
            action = self.opponent.choose_action(obs, mask)
            
        self._play_action(action, self.next_player_to_play)

    def _calculate_reward(self, player_who_moved):
        if self.terminated:
            if self.winner == 0: return REWARDS["draw"]
            if self.opponent is not None:
                return REWARDS["win"] if self.winner == self.agent_player_symbol else REWARDS["lose"]
            else:
                return REWARDS["win"] 

        if self.opponent is None:
            return REWARDS["valid_move"]
            
        if player_who_moved != self.agent_player_symbol:
            return REWARDS["valid_move"]
        
        r, c = self.last_move_row, self.last_move_col
        reward = 0.0
        
        if is_a_triplet(self.board, r, c, player_who_moved)[0]:
            reward = REWARDS["create_three"]
        elif is_a_pair(self.board, r, c, player_who_moved)[0]:
            reward = REWARDS["create_two"]
        
        if is_block_triplet(self.board, r, c, player_who_moved)[0]:
            reward += REWARDS["block_three"]
        elif is_block_pair(self.board, r, c, player_who_moved)[0]:
            reward += REWARDS["block_two"]
            
        return REWARDS["valid_move"] if reward == 0.0 else reward

    def _play_action(self, col, player):
        row = self.get_first_empty_row(col)
        if row is not None:
            self.board[row, col] = player
            self.last_move_row = row
            self.last_move_col = col
            
    def get_first_empty_row(self, col):
        for r in reversed(range(ROWS_COUNT)):
            if self.board[r, col] == 0:
                return r
        return None # Full col

    def get_board(self):
        return self.board.copy() 

    def is_action_valid(self, action):
        return 0 <= action < COLUMNS_COUNT and self.board[0, action] == 0
    
    def board_is_full(self):
        return np.all(self.board[0, :] != 0)

    def is_column_full(self, column):
        return self.board[0, column] != 0
    
    def get_valid_actions(self):
        return [c for c in range(COLUMNS_COUNT) if not self.is_column_full(c)]
    
    def get_action_mask(self):
        return (self.board[0, :] == 0).astype(np.int8)
    
    def switch_player(self):
        self.next_player_to_play *= -1
    
    def check_win_around_last_move(self):
        if self.last_move_row is None: return False
        player = self.board[self.last_move_row, self.last_move_col]
        if player == 0: return False
        return is_a_quadruplet(self.board, self.last_move_row, self.last_move_col, player)[0]
    
    def _is_finish(self): 
        if self.check_win_around_last_move():
            self.winner = self.board[self.last_move_row, self.last_move_col]
            return True
        if self.board_is_full():
            self.winner = 0
            return True
        self.winner = None
        return False

    def get_winner(self):
        return self.winner
    
    def render(self):
        if self.render_mode == "console":
            self.render_console()
        elif self.render_mode == "gui":
            if self.gui_renderer is None:
                 self.gui_renderer = Connect4GUIRenderer()
            self.gui_renderer.draw_board(self.get_board())
    
    def render_console(self):
        ROWS, COLS = self.board.shape
        print("\nCurrent board:")
        for r in range(ROWS):
            row_str = f"{r} | "
            for c in range(COLS):
                cell = self.board[r, c]
                if cell == 1:
                    row_str += f"{Fore.RED}X{Style.RESET_ALL} | "
                elif cell == -1:
                    row_str += f"{Fore.YELLOW}O{Style.RESET_ALL} | "
                else:
                    row_str += "  | "
            print(row_str.rstrip())
        print("‾" * (COLS * 4 + 3))
        col_labels = "    " + "   ".join(str(c) for c in range(COLS))
        print(col_labels + "\n")

    def close(self):
        if self.gui_renderer:
            self.gui_renderer.close()
            self.gui_renderer = None
import gymnasium
from gymnasium import spaces
import numpy as np
from colorama import Fore, Style
from gui.gui_rend import render_gui
from env.env_config import *

class Connect4Env(gymnasium.Env):
    def __init__(self, opponent=None, render_mode=None, first_player=None):
        self.opponent = opponent
        self.first_player = first_player if first_player is not None else 1
        self.next_player_to_play = 1
        self.render_mode = render_mode

        self.action_space = spaces.Discrete(COLUMNS_COUNT)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(ROWS_COUNT, COLUMNS_COUNT), dtype=np.int8)

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros((ROWS_COUNT, COLUMNS_COUNT), dtype=np.int8)
        self.next_player_to_play = self.first_player
        self.last_move_row = None
        self.last_move_col = None
        self.winner = None
        return self.board, {}

    def is_column_full(self, column):
        return self.board[0, column] != 0

    def board_is_full(self):
        return np.all(self.board != 0)

    def is_action_valid(self, action):
        return 0 <= action < COLUMNS_COUNT and not self.is_column_full(action)

    def switch_player(self):
        self.next_player_to_play = -1 * self.next_player_to_play

    def get_valid_actions(self):
        return [col for col in range(COLUMNS_COUNT) if not self.is_column_full(col)]

    def clone(self):
        new_env = Connect4Env(opponent=self.opponent, render_mode=self.render_mode, first_player=self.first_player)
        new_env.next_player_to_play = self.next_player_to_play
        new_env.board = self.board.copy()
        new_env.last_move_row = self.last_move_row
        new_env.last_move_col = self.last_move_col
        new_env.winner = self.winner
        return new_env

    def check_win_around_last_move(self, row, col):
        player = self.board[row, col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for step in range(-3, 4):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < ROWS_COUNT and 0 <= c < COLUMNS_COUNT and self.board[r, c] == player:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def is_finish(self):
        self.winner = None
        if self.last_move_row is None or self.last_move_col is None:
            return False
        if self.check_win_around_last_move(self.last_move_row, self.last_move_col):
            self.winner = self.board[self.last_move_row, self.last_move_col]
            return True
        if self.board_is_full():
            self.winner = 0
            return True
        return False

    def get_winner(self):
        return self.winner

    def play_action(self, action):
        for i in range(ROWS_COUNT - 1, -1, -1):
            if self.board[i, action] == 0:
                self.board[i, action] = self.next_player_to_play
                self.last_move_row = i
                self.last_move_col = action
                return

    def step(self, action, play_opponent=True):
        # Se la mossa è illegale → penalità e turno perso
        if not self.is_action_valid(action):
            reward = REWARDS["invalid_move"] # penalità per mossa invalida (puoi regolare il valore)
            # Non cambia stato della board, solo penalità e cambio turno
            print(f"Mossa invalida: {action}. Penalità applicata. Player {self.next_player_to_play} perde il turno.")
            self.switch_player()
            return self.board.copy(), reward, True, False, {} #Con True termina la partita
        
        
        action = action.item() if isinstance(action, np.ndarray) else action
        self.play_action(action)

        is_finish = self.is_finish()
        winner = self.get_winner()

        reward = REWARDS["valid_move"]
        if is_finish:
            if winner == self.next_player_to_play:
                reward = REWARDS["win"]
            elif winner == -self.next_player_to_play:
                reward = REWARDS["lose"]
            else:
                reward = REWARDS["draw"]

        self.switch_player()

        if is_finish:
            return self.board.copy(), reward, True, False, {}

        if play_opponent and self.opponent is not None:
            opponent_action = self.opponent.choose_action()
            obs, opp_reward, done, trunc, info = self.step(opponent_action, play_opponent=False)
            return obs, -opp_reward, done, trunc, info

        return self.board.copy(), reward, False, False, {}

    def get_board(self):
        return self.board.copy()

    def render(self, screen=None):
        if self.render_mode == "console":
            self.render_console_2()
        elif self.render_mode == "gui" and screen is not None:
            render_gui(screen, self.get_board())

    def render_console(self):
        print("\nCurrent board:")
        for row in self.board:
            row_str = ""
            for cell in row:
                if cell == 1:
                    row_str += f"{Fore.RED}X{Style.RESET_ALL} | "
                elif cell == -1:
                    row_str += f"{Fore.YELLOW}O{Style.RESET_ALL} | "
                else:
                    row_str += "  | "
            print(row_str[:-2])
        print("‾" * (COLUMNS_COUNT * 4 - 1))
        print("   ".join(str(i) for i in range(COLUMNS_COUNT)))
        print()
    
    def render_console_2(self):
        print(self.board)

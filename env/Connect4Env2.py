import numpy as np
import gymnasium as gym
from gymnasium import spaces
from colorama import Fore, Style
from gui.gui_rend import render_gui
from env.env_config import ROWS_COUNT, COLUMNS_COUNT, REWARDS


class Connect4Env(gym.Env):
    metadata = {"render_modes": ["console", "gui"]}

    def __init__(self, opponent=None, render_mode=None, first_player=1):
        super().__init__()
        self.opponent = opponent
        self.first_player = first_player
        self.next_player_to_play = first_player
        self.render_mode = render_mode

        # Azioni = colonne disponibili
        self.action_space = spaces.Discrete(COLUMNS_COUNT)
        # Osservazioni = griglia 6x7
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32
        )

        self.reset()

    # ----------------------
    # Utility funzioni base
    # ----------------------

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros((ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32)
        self.next_player_to_play = self.first_player
        self.last_move_row = None
        self.last_move_col = None
        self.winner = None
        return self.board.copy(), {"action_mask": self.get_action_mask()}

    def is_action_valid(self, action):
        return 0 <= action < COLUMNS_COUNT and not self.is_column_full(action)
    
    def is_column_full(self, column):
        return self.board[0, column] != 0

    def board_is_full(self):
        return np.all(self.board != 0)

    def get_valid_actions(self):
        """Restituisce lista delle colonne non piene."""
        return [c for c in range(COLUMNS_COUNT) if not self.is_column_full(c)]

    def get_action_mask(self):
        """Restituisce un array binario per masking: 1 = colonna valida, 0 = invalida."""
        mask = np.zeros(COLUMNS_COUNT, dtype=np.int8)
        for c in self.get_valid_actions():
            mask[c] = 1
        return mask

    def switch_player(self):
        self.next_player_to_play = -self.next_player_to_play

    def clone(self):
        new_env = Connect4Env(
            opponent=self.opponent, render_mode=self.render_mode, first_player=self.first_player
        )
        new_env.next_player_to_play = self.next_player_to_play
        new_env.board = self.board.copy()
        new_env.last_move_row = self.last_move_row
        new_env.last_move_col = self.last_move_col
        new_env.winner = self.winner
        return new_env

    # ----------------------
    # Controllo vittoria
    # ----------------------

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

    def check_three_effect(self, row, col, player, check_opponent=False):
        """
        Controlla se la mossa appena effettuata ha:
        - creato una triple proprie (check_opponent=False)
        - bloccato una triple dell'avversario (check_opponent=True)
        
        row, col: coordinate dell'ultima mossa
        player: ID del giocatore che ha fatto la mossa
        check_opponent: se True, verifica triple avversarie bloccate
        """
        opponent = -player
        directions = [(1,0), (0,1), (1,1), (1,-1)]

        for dr, dc in directions:
            count = 1 if not check_opponent else 0
            empty_spaces = 0

            # avanti
            for step in range(1, 3 if not check_opponent else 4):
                r, c = row + dr*step, col + dc*step
                if 0 <= r < ROWS_COUNT and 0 <= c < COLUMNS_COUNT:
                    cell = self.board[r, c]
                    if check_opponent:
                        if cell == opponent:
                            count += 1
                        elif cell == 0:
                            empty_spaces += 1
                            break
                        else:
                            break
                    else:
                        if cell == player:
                            count += 1
                        else:
                            break
                else:
                    break

            # indietro
            for step in range(1, 3 if not check_opponent else 4):
                r, c = row - dr*step, col - dc*step
                if 0 <= r < ROWS_COUNT and 0 <= c < COLUMNS_COUNT:
                    cell = self.board[r, c]
                    if check_opponent:
                        if cell == opponent:
                            count += 1
                        elif cell == 0:
                            empty_spaces += 1
                            break
                        else:
                            break
                    else:
                        if cell == player:
                            count += 1
                        else:
                            break
                else:
                    break

            # Verifica condizione triple
            if (not check_opponent and count == 3) or (check_opponent and count == 2 and empty_spaces > 0):
                return True

        return False
    
    def is_defensive_move(self, row, col, player):
        """Ritorna True se la mossa blocca una triple dell'avversario."""
        opponent = -player
        return self.check_three_effect(row, col, player, check_opponent=True)

    # ----------------------
    # Gestione mosse
    # ----------------------

    def play_action(self, action):
        for i in range(ROWS_COUNT - 1, -1, -1):
            if self.board[i, action] == 0:
                self.board[i, action] = self.next_player_to_play
                self.last_move_row = i
                self.last_move_col = action
                return

    def step(self, action, play_opponent=True):
        # Assicurati che action sia int
        action = int(action)

        # Azioni valide
        valid_moves = self.get_valid_actions()
        if not valid_moves:
            self.winner = 0
            return self.board.copy(), REWARDS["draw"], True, False, {
                "action_mask": self.get_action_mask()
            }

        if action not in valid_moves:
            # Penalizziamo mosse invalide (solo training)
            return self.board.copy(), REWARDS["invalid"], False, False, {
                "action_mask": self.get_action_mask()
            }

        # Giocatore attuale
        current_player = self.next_player_to_play

        # Applica la mossa
        self.play_action(action)

        # Controlla fine partita
        is_finish = self.is_finish()
        winner = self.get_winner()

        if is_finish:
            if winner == current_player:
                reward = REWARDS["win"]
            elif winner == -current_player:
                reward = REWARDS["lose"]
            else:
                reward = REWARDS["draw"]
        else:
            reward = REWARDS["valid_move"]

        # Cambia turno
        self.switch_player()

        if is_finish:
            return self.board.copy(), reward, True, False, {"action_mask": self.get_action_mask()}

        # Opponente (se c’è e siamo in gioco normale, non training)
        if play_opponent and self.opponent is not None:
            opponent_action = self.opponent.choose_action()
            obs, opp_reward, done, trunc, info = self.step(opponent_action, play_opponent=False)
            return obs, -opp_reward, done, trunc, info

        return self.board.copy(), reward, False, False, {"action_mask": self.get_action_mask()}

    # ----------------------
    # Rendering
    # ----------------------

    def get_board(self):
        return self.board.copy()

    def render(self, screen=None):
        if self.render_mode == "console":
            self.render_console()
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

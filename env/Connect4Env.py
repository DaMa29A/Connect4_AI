import numpy as np
import gymnasium as gym
from gymnasium import spaces
from colorama import Fore, Style, init
init(autoreset=True)
from gui.gui_rend import render_gui
from env.env_config import ROWS_COUNT, COLUMNS_COUNT, REWARDS
from utils.check_rules import is_defensive_move, is_a_triplet, is_a_quadruplet

class Connect4Env(gym.Env):
    # opponent_symbol: -1 (O) o 1 (X)
    # opponent: classe agente (es. RandomAgent)
    # render_mode: "console", "gui" o None
    def __init__(self, opponent_symbol=-1, opponent=None, render_mode=None, first_move_random=False):
        super().__init__()
        self.render_mode = render_mode
        self.first_move_random = first_move_random

        # Identità giocatori
        self.first_player = 1 # Inizia sempre X
        self.next_player_to_play = self.first_player
        self.opponent_symbol = opponent_symbol
        # Se viene passata una classe, istanzia l'agente
        self.opponent = opponent(self) if opponent is not None else None

        # Spazi Gym
        self.action_space = spaces.Discrete(COLUMNS_COUNT) # 7 colonne
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32
        )

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros((ROWS_COUNT, COLUMNS_COUNT), dtype=np.float32)
        self.next_player_to_play = self.first_player
        self.last_move_row = None
        self.last_move_col = None
        self.winner = None
        
        # Se l'opponent è X (1), deve iniziare la partita
        # if self.opponent is not None and self.opponent_symbol == self.first_player:
        #     self.opponent_step()
            
        # borad, info aggiuntive
        return self.board.copy(), {}
    
    def clone(self):
        new_env = Connect4Env(
            opponent_symbol=-1, opponent=None, render_mode=None
        )
        new_env.next_player_to_play = self.next_player_to_play
        new_env.board = self.board.copy()
        new_env.last_move_row = self.last_move_row
        new_env.last_move_col = self.last_move_col
        new_env.winner = self.winner
        return new_env

    def get_board(self):
        return self.board.copy()

    def is_action_valid(self, action):
        return 0 <= action < COLUMNS_COUNT and not self.is_column_full(action)
    
    def is_column_full(self, column):
        return self.board[0, column] != 0

    def board_is_full(self):
        return np.all(self.board != 0)

    def get_valid_actions(self):
        return [c for c in range(COLUMNS_COUNT) if not self.is_column_full(c)]
    
    def get_first_empty_row(self, col):
        for r in reversed(range(self.board.shape[0])):
            if self.board[r, col] == 0:
                return r
        return None

    def is_playable_cell(self, row, col):
        return self.get_first_empty_row(col) == row
    
    
    # Crea una maschera binaria che indica quali colonne sono ancora disponibili per giocare.
    # 1 = colonna valida, 0 = non valida.
    def get_action_mask(self):
        mask = np.zeros(COLUMNS_COUNT, dtype=np.int8)
        for c in self.get_valid_actions():
            mask[c] = 1
        return mask
    
    def switch_player(self):
        self.next_player_to_play = -self.next_player_to_play
    
    # Quando ci sono 4 pedine consecutive restituisce True
    def check_win_around_last_move(self, row, col):
        player = self.board[row, col]
        return is_a_quadruplet(self.board, row, col, player)
    
    def is_finish(self): 
        self.winner = None # reset winner
        # Se non è stata ancora fatta alcuna mossa, non può esserci una vittoria o pareggio
        if self.last_move_row is None or self.last_move_col is None:
            return False
        # Controlla se l’ultima mossa ha causato una vittoria
        if self.check_win_around_last_move(self.last_move_row, self.last_move_col):
            self.winner = self.board[self.last_move_row, self.last_move_col]
            return True
        # Se board piena e nessuno ha vinto, pareggio
        if self.board_is_full():
            self.winner = 0
            return True
        # Se nessuna delle condizioni sopra è vera, la partita continua
        return False

    def get_winner(self):
        return self.winner
    
    # Esegue l’azione (giocata) del giocatore corrente
    def play_action(self, action):
        for i in range(ROWS_COUNT - 1, -1, -1):
            if self.board[i, action] == 0:
                self.board[i, action] = self.next_player_to_play
                self.last_move_row = i
                self.last_move_col = action
                return
    
    def opponent_step(self):
        if self.opponent is not None:
            opponent_action = self.opponent.choose_action()
            obs, opp_reward, done, trunc, info = self.step(opponent_action, play_opponent=False)
            return obs, -opp_reward, done, trunc, info
    
    def step(self, action, play_opponent=True):
        # Apertura automatica dell'opponent se necessario
        if play_opponent and self.opponent_symbol == self.first_player and np.all(self.board == 0):
            self.opponent_step()
            
        # Prima mossa random se abilitato
        if self.first_move_random and np.all(self.board == 0):
            action = (np.random.choice(self.get_valid_actions()))
        
        action = int(action) # Action deve essere int

        # Azioni valide
        valid_moves = self.get_valid_actions()
        if not valid_moves:
            self.winner = 0
            return self.board.copy(), REWARDS["draw"], True, False, {}

        # Controlla se l’azione scelta è non valida
        if action not in valid_moves:
            print(f"Invalid action attempted: {action}")
            return self.board.copy(), REWARDS["invalid"], False, False, {}

        # Giocatore attuale
        current_player = self.next_player_to_play

        # Applica la mossa
        self.play_action(action)

        # Controlla fine partita
        is_finish = self.is_finish()
        winner = self.get_winner()

        # Ricompense
        if is_finish:
            if winner == self.opponent_symbol:
                reward = REWARDS["lose"]
            elif winner == -self.opponent_symbol:
                reward = REWARDS["win"]
            elif winner == 0:
                reward = REWARDS["draw"]
        else:
            reward = REWARDS["valid_move"]
            # Tripletta propria
            if is_a_triplet(self.board, self.last_move_row, self.last_move_col, current_player):
                reward += REWARDS["create_three"]
            # Blocco tripletta avversaria
            if is_defensive_move(self.board, self.last_move_row, self.last_move_col, current_player):
                reward += REWARDS["block_three"]

        # Cambia turno
        self.switch_player()

        if is_finish:
            return self.board.copy(), reward, True, False, {}

        # Opponent esegue la mossa se esiste ()
        if play_opponent:
            self.opponent_step()

        return self.board.copy(), reward, False, False, {}

        
    def render(self, screen=None):
        if self.render_mode == "console":
            self.render_console()
        elif self.render_mode == "gui" and screen is not None:
            render_gui(screen, self.get_board())
        else:
            pass
    
    # Mostra la board in console con colori
    def render_console(self):
        ROWS, COLS = self.board.shape
        print("\nCurrent board:")

        for r in range(ROWS):
            row_str = f"{r} | "  # numero di riga a sinistra
            for c in range(COLS):
                cell = self.board[r, c]
                if cell == 1:
                    row_str += f"{Fore.RED}X{Style.RESET_ALL} | "
                elif cell == -1:
                    row_str += f"{Fore.YELLOW}O{Style.RESET_ALL} | "
                else:
                    row_str += "  | "
            print(row_str.rstrip())

        # linea divisoria
        print("‾" * (COLS * 4 + 3))
        
        # etichette colonne
        col_labels = "    " + "   ".join(str(c) for c in range(COLS))
        print(col_labels + "\n")
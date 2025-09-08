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
        return [c for c in range(COLUMNS_COUNT) if not self.is_column_full(c)]

    """
    Crea una maschera binaria che indica quali colonne sono ancora disponibili per giocare.
    1 = colonna valida, 0 = invalida.
    """
    def get_action_mask(self):
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

    def get_board(self):
        return self.board.copy()
    
    def get_first_empty_row(self, col):
        """
        Restituisce l'indice della prima riga libera nella colonna specificata.
        Se la colonna è piena, restituisce None.
        """
        for r in reversed(range(self.board.shape[0])):
            if self.board[r, col] == 0:
                return r
        return None

    # ----------------------
    # Controllo vittoria
    # ----------------------
    
    """
    Conta se ci sono target_count pedine consecutive del player attorno alla posizione (row, col).
    """
    def count_consecutive_pieces(self, row, col, target_count, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1 if self.board[row, col] == player else 0  # Include la pedina se è del player

            # Verso avanti
            for step in range(1, target_count):
                r, c = row + step * dr, col + step * dc
                if 0 <= r < ROWS_COUNT and 0 <= c < COLUMNS_COUNT and self.board[r, c] == player:
                    count += 1
                else:
                    break

            # Verso indietro
            for step in range(1, target_count):
                r, c = row - step * dr, col - step * dc
                if 0 <= r < ROWS_COUNT and 0 <= c < COLUMNS_COUNT and self.board[r, c] == player:
                    count += 1
                else:
                    break

            if count >= target_count:
                return True

        return False

    # Quando ci sono 4 pedine consecutive restituisce True
    def check_win_around_last_move(self, row, col):
        player = self.board[row, col]
        return self.count_consecutive_pieces(row, col, target_count=4, player=player)

    def is_finish(self): 
        # reset winner
        self.winner = None
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

    """Controlla se la mossa 
        - ha bloccato una tripla dell'avversario
    [player] rappresenta il giocatore che sta facendo la mossa difensiva
    """
    def is_defensive_move(self, row, col, player):
        opponent = -player

        # La cella deve essere appena occupata dal player
        if self.board[row, col] != player:
            return False

        # Simula che l'avversario giochi lì
        simulated_env = self.clone()
        simulated_env.board[row, col] = opponent

        # Se l'avversario avrebbe fatto 4 in fila → la mossa ha bloccato
        return simulated_env.count_consecutive_pieces(row, col, target_count=4, player=opponent)

    """
        Controlla se l'avversario ha una triple potenziale da completare.
    """
    def has_opponent_threat(self, player):
        opponent = -player
        for r in range(ROWS_COUNT):
            for c in range(COLUMNS_COUNT):
                if self.board[r, c] == 0:
                    simulated_env = self.clone()
                    simulated_env.board[r, c] = opponent
                    if simulated_env.count_consecutive_pieces(r, c, target_count=4, player=opponent):
                        return True
        return False

    
    def is_offensive_move(self, row, col, player):
        """
        Verifica se la mossa ha creato una tripletta sfruttabile (con almeno un'estremità libera)
        o una quadrupla (vittoria).
        """
        # Controllo quadrupla diretta
        if self.count_consecutive_pieces(row, col, target_count=4, player=player):
            return True

        # Controllo tripletta sfruttabile
        if self.count_consecutive_pieces(row, col, target_count=3, player=player):
            directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
            for dr, dc in directions:
                for sign in [-1, 1]:
                    rr = row + sign * dr
                    cc = col + sign * dc
                    if 0 <= rr < ROWS_COUNT and 0 <= cc < COLUMNS_COUNT:
                        if self.board[rr][cc] == 0:
                            return True  # almeno un'estremità libera
        return False

    
    def has_offensive_threat(self, player):
        """
        Verifica se il giocatore ha una mossa che può creare una tripletta sfruttabile o una quadrupla.
        Considera solo celle libere che sono effettivamente giocabili (prima libera nella colonna).
        """
        for c in range(COLUMNS_COUNT):
            r = self.get_first_empty_row(c)
            if r is None:
                continue  # colonna piena

            simulated_env = self.clone()
            simulated_env.board[r, c] = player
            simulated_env.last_move_row = r
            simulated_env.last_move_col = c

            # Verifica quadrupla (vittoria)
            if simulated_env.count_consecutive_pieces(r, c, target_count=4, player=player):
                return True

            # Verifica tripletta con almeno un'estremità libera
            if simulated_env.count_consecutive_pieces(r, c, target_count=3, player=player):
                directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
                for dr, dc in directions:
                    for sign in [-1, 1]:
                        rr = r + sign * dr
                        cc = c + sign * dc
                        if 0 <= rr < ROWS_COUNT and 0 <= cc < COLUMNS_COUNT:
                            if simulated_env.board[rr][cc] == 0 and simulated_env.get_first_empty_row(cc) == rr:
                                return True  # estremità libera e giocabile
        return False


    
    
    
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
            print(f"Invalid action attempted: {action}")
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
            # Tripletta propria
            if self.count_consecutive_pieces(self.last_move_row, self.last_move_col, target_count=3, player=current_player):
                reward += REWARDS["create_three"]
            # Blocco tripletta avversaria
            if self.is_defensive_move(self.last_move_row, self.last_move_col, current_player):
                reward += REWARDS["block_three"]

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
    
    def render(self, screen=None):
        if self.render_mode == "console":
            self.render_console()
        elif self.render_mode == "gui" and screen is not None:
            render_gui(screen, self.get_board())
        else:
            pass

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

import numpy as np
from scipy.signal import convolve2d
from env.env_config import ROWS_COUNT, COLUMNS_COUNT

# Kernel per cercare linee orizzontali, verticali, diagonali
KERNELS = [
    np.array([[1, 1, 1, 0]]),           # orizzontale destra
    np.array([[0, 1, 1, 1]]),           # orizzontale sinistra
    np.array([[1], [1], [1], [0]]),     # verticale
    np.array([[0], [1], [1], [1]]),     # verticale inversa
    np.eye(4, dtype=int),               # diagonale \
    np.fliplr(np.eye(4, dtype=int))     # diagonale /
]

KERNELS_FULL = [
    np.array([[1, 1, 1, 1]]),               # Orizzontale
    np.array([[1], [1], [1], [1]]),         # Verticale
    np.eye(4, dtype=int),                   # Diagonale ↘
    np.fliplr(np.eye(4, dtype=int))         # Diagonale ↙
]

def get_kernels(target_count):
    if target_count == 4:
        return [
            np.array([[1, 1, 1, 1]]),
            np.array([[1], [1], [1], [1]]),
            np.eye(4, dtype=int),
            np.fliplr(np.eye(4, dtype=int))
        ]
    elif target_count == 3:
        return [
            np.array([[1, 1, 1]]),
            np.array([[1], [1], [1]]),
            np.eye(3, dtype=int),
            np.fliplr(np.eye(3, dtype=int))
        ]
    else:
        raise ValueError("Unsupported target_count")


# Controlla se una posizione è giocabile
def is_playable(board, r, c):
    if board[r, c] != 0:
        return False
    if r == ROWS_COUNT - 1:
        return True
    if board[r + 1, c] != 0:
        return True
    return False

# Controlla se ci sono opportunità di vittoria o difesa
def check_opportunities(board, target_id):
    occasions = []

    for kernel in KERNELS:
        conv = convolve2d(board == target_id, kernel, mode="valid")
        locs = np.argwhere(conv == 3)

        for r, c in locs:
            for i in range(kernel.shape[0]):
                for j in range(kernel.shape[1]):
                    if kernel[i, j] != 1:
                        continue
                    rr, cc = r + i, c + j
                    if 0 <= rr < ROWS_COUNT and 0 <= cc < COLUMNS_COUNT:
                        if board[rr, cc] == 0 and is_playable(board, rr, cc):
                            occasions.append((rr, cc))

    return list(set(occasions))

# Controlla se il giocatore può difendersi
def check_defensive_opportunities(board, player_id):
    return check_opportunities(board, target_id=-player_id)

# Controlla se il giocatore può attaccare
def check_attack_opportunities(board, player_id):
    return check_opportunities(board, target_id=player_id)

# Controlla se la mossa appena fatta è difensiva
def is_defensive_move(board, r, c, current_player):
    defensive_detected = False

    board_before = board.copy() # copia della board
    board_before[r, c] = 0  # rimuove temporaneamente la mossa appena fatta

    defensive_detected = (r, c) in check_defensive_opportunities(board_before, current_player)

    return defensive_detected

# Conta il numero di pedine consecutive in tutte le direzioni
def is_a_sequence(board, r, c, current_player, target_count):
    if board[r, c] != current_player:
        return False

    player_board = (board == current_player).astype(int)
    kernels = get_kernels(target_count)

    for kernel in kernels:
        conv = convolve2d(player_board, kernel, mode="valid")
        locs = np.argwhere(conv == target_count)

        for rr, cc in locs:
            if rr <= r < rr + kernel.shape[0] and cc <= c < cc + kernel.shape[1]:
                return True
    return False

# Controlla se la mossa appena fatta crea una tripla
def is_a_triplet(board, r, c, current_player):
    return is_a_sequence(board, r, c, current_player, target_count=3)

# Controlla se la mossa appena fatta crea una quadrupla
def is_a_quadruplet(board, r, c, current_player):
    result = is_a_sequence(board, r, c, current_player, target_count=4)
    return result
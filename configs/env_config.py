# Dimensioni griglia
COLUMNS_COUNT = 7
ROWS_COUNT = 6

# Rewards
REWARDS = {
    "win": 1.0,             # vittoria
    "lose": -1.0,           # sconfitta
    "draw": 0.5,            # pareggio
    "valid_move": -0.01,    # mossa valida ma non vincente
    "invalid": -1.0,        # mossa non valida (colonna piena)
    "create_three": 0.4,    # nuova tripletta creata
    "block_three": 0.4,     # tripla avversaria bloccata
    "create_two": 0.1,      # nuova doppietta creata
    "block_two": 0.1        # doppietta avversaria bloccata
}
# Dimensioni griglia
COLUMNS_COUNT = 7
ROWS_COUNT = 6

# Reward
REWARDS = {
    "win": 1.0,             # vittoria
    "lose": -1.0,           # sconfitta
    "draw": 0.3,            # pareggio
    "valid_move": 0.01,     # mossa valida ma non vincente
    "invalid": -2,          # mossa non valida (colonna piena)
    "create_three": 0.3,    # nuova tripletta creata
    "block_three": 0.2      # tripla avversaria bloccata
}

# Modalità di rendering
RENDER_MODE = "gui"  # oppure "console"

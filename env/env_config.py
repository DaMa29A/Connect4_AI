# Dimensioni griglia
COLUMNS_COUNT = 7
ROWS_COUNT = 6

# Reward
REWARDS = {
    "win": 1.0,           # vittoria
    "lose": -1.0,         # sconfitta
    "draw": 0.5,          # pareggio
    "valid_move": 0.0,    # mossa valida ma non vincente
    "invalid": -0.5,      # mossa non valida (colonna piena)
}

# Modalità di rendering
RENDER_MODE = "gui"  # oppure "console"

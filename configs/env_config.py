# Board dims
COLUMNS_COUNT = 7
ROWS_COUNT = 6

# Seed
SEED = 42

# Reward Shaping
# REWARDS = {
#     "win": 1.0,           # Win
#     "lose": -1.0,         # Lose
#     "draw": 0.5,          # Draw
#     "invalid": -1.0,      # Invalid Move
#     "valid_move": 0.0,    # Valid Move [0.0]

#     "create_three": 0.0,  # Create a row of 3 [0.5]
#     "create_two": 0.0,    # Create a row of 2 [0.2]
#     "block_three": 0.0,   # Blocks a row of 3 (opponent) (Opponent cannot create a row of 4) [0.3]
#     "block_two": 0.0      # Blocks a row of 2 (opponent) (Opponent cannot create a row of 3) [0.1]
# }

# REWARDS = {
#     "win": 1.0,           # Win
#     "lose": -1.0,         # Lose
#     "draw": 0.5,          # Draw
#     "invalid": -1.0,      # Invalid Move
#     "valid_move": -0.01,    # Valid Move [0.0]

#     "create_three": 0.4,  # Create a row of 3 [0.5]
#     "create_two": 0.1,    # Create a row of 2 [0.2]
#     "block_three": 0.4,   # Blocks a row of 3 (opponent) (Opponent cannot create a row of 4) [0.3]
#     "block_two": 0.1      # Blocks a row of 2 (opponent) (Opponent cannot create a row of 3) [0.1]
# }

# REWARDS = {
#     "win": 1.0,           # Win
#     "lose": -1.0,         # Lose
#     "draw": 0.5,          # Draw
#     "invalid": -1.0,      # Invalid Move
#     "valid_move": -0.001,    # Valid Move [0.0]

#     "create_three": 0.0,  # Create a row of 3 [0.5]
#     "create_two": 0.0,    # Create a row of 2 [0.2]
#     "block_three": 0.6,   # Blocks a row of 3 (opponent) (Opponent cannot create a row of 4) [0.3]
#     "block_two": 0.3      # Blocks a row of 2 (opponent) (Opponent cannot create a row of 3) [0.1]
# }

REWARDS = {
    "win": 1.0,           # Win
    "lose": -1.0,         # Lose
    "draw": 0.0,          # Draw
    "invalid": -1.0,      # Invalid Move
    "valid_move": -0.01,    # Valid Move [0.0]

    "create_three": 0.1,  # Create a row of 3 [0.5]
    "create_two": 0.05,    # Create a row of 2 [0.2]
    "block_three": 0.05,   # Blocks a row of 3 (opponent) (Opponent cannot create a row of 4) [0.3]
    "block_two": 0.02      # Blocks a row of 2 (opponent) (Opponent cannot create a row of 3) [0.1]
}
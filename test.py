from env.Connect4Env import Connect4Env

env = Connect4Env(render_mode="console")

env.step(0) #X
env.step(1) #O
print(f"Is valid action 0? {env.is_action_valid(0)}")
print(f"Is Column full? {env.is_column_full(0)}")
env.render() 

env.step(0) #X
env.step(0) #O
env.step(0) #X
env.step(0) #O
env.step(0) #X
print(f"\nIs valid action 0? {env.is_action_valid(0)}")
print(f"Is Column full? {env.is_column_full(0)}")
env.render()  

print(f"Valid actions: {env.get_valid_actions()}")
print(f"Action Mask: {env.get_action_mask()}")

row = env.last_move_row
col = env.last_move_col
print(f"Check win for last move at ({row}, {col}): {env.check_win_around_last_move(row, col)}")


env.step(1) #O
env.step(2) #X
env.step(1) #O
row = env.last_move_row
col = env.last_move_col
print(f"\nCheck win for last move at ({row}, {col}): {env.check_win_around_last_move(row, col)}")
env.step(2) #X
env.step(1) #O
row = env.last_move_row
col = env.last_move_col
print(f"Check win for last move at ({row}, {col}): {env.check_win_around_last_move(row, col)}")
env.render()  

env.step(2) #X
row = env.last_move_row
col = env.last_move_col
print(f"\n Is defensive move at ({row}, {col}) for player O? {env.is_defensive_move(row, col, 1)}")
env.render() 

env.step(2) #O
row = env.last_move_row
col = env.last_move_col
print(f"\n Is defensive move at ({row}, {col}) for player X? {env.is_defensive_move(row, col, -1)}")
env.render() 


env.step(6) #X
env.step(5) #O
env.step(6) #X
env.step(6) #O
row = env.last_move_row
col = env.last_move_col
print(f"\n Is defensive move at ({row}, {col}) for player X? {env.is_defensive_move(row, col, -1)}")
print(f"Has opponent threat? {env.has_opponent_threat(-1)}")
env.render()

env.step(4) #X
env.step(3) #O
env.step(4) #X
env.step(6) #O
env.step(4) #X
row = env.last_move_row
col = env.last_move_col
print(f"Has opponent threat? {env.has_opponent_threat(-1)}")
print(f"Is offensive move at ({row}, {col}) for player X? {env.is_offensive_move(row, col, 1)}")
env.render()

# RICORDA CHE LE RIGHE VANNO LETTE DA SOPRA A SOTTO (0 IN ALTO, 5 IN BASSO)
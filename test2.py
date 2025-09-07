from env.Connect4Env import Connect4Env

env = Connect4Env(render_mode="console")

env.step(2) #X
env.step(1) #O
env.step(2) #X
env.step(2) #O
env.step(4) #X
env.step(3) #O
env.step(2) #X
env.step(3) #O
env.step(2) #X
row = env.last_move_row
col = env.last_move_col
print(f"\n Is offensive move at ({row}, {col}) for player X? {env.is_offensive_move(row, col, 1)}")


env.step(3) #O
row = env.last_move_row
col = env.last_move_col
print(f"\n Is offensive move at ({row}, {col}) for player O? {env.is_offensive_move(row, col, -1)}")

env.render()
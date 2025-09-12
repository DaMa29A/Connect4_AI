from env.Connect4Env import Connect4Env
from utils.check_rules import is_a_triplet

env = Connect4Env(render_mode="console")
env.render()

env.step(5) #X
env.step(2) #O
env.step(5) #X
env.step(3) #O
env.step(5) #X

r = env.last_move_row
c = env.last_move_col
env.render()

print(f"Is a triplet ({r},{c})? {is_a_triplet(env.board, r, c, 1)}") # True
from env.Connect4Env import Connect4Env
from utils.check_rules import is_playable, check_defensive_opportunities, check_attack_opportunities, is_defensive_move

env = Connect4Env(render_mode="console")
env.render()

env.step(5) #X
env.step(2) #O
env.step(5) #X
env.step(3) #O
env.step(6) #X
env.step(1) #O

env.step(0) #X
r = env.last_move_row
c = env.last_move_col
env.render()

print(f"Is defensive move ({r},{c})? {is_defensive_move(env.board, r, c, current_player=1)}") # True

env.step(4) #O
env.step(4) #X
env.step(0) #O
env.step(4) #X
env.step(3) #O
env.step(3) #X
env.step(3) #O
env.render()
r = env.last_move_row
c = env.last_move_col
print(f"Is defensive move ({r},{c})? {is_defensive_move(env.board, r, c, current_player=-1)}") # True
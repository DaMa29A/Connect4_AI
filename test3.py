from env.Connect4Env import Connect4Env
from utils.check_rules import is_playable, check_defensive_opportunities, check_attack_opportunities

env = Connect4Env(render_mode="console")

env.render()

r = 5
c = 5
print(f"\nIs playable ({r},{c})? {is_playable(env.board, r, c)}") # True

r = 0
c = 5
print(f"Is playable ({r},{c})? {is_playable(env.board, r, c)}") # False

env.step(5) #X
env.render()
r = env.last_move_row
c = env.last_move_col
print(f"Last move at ({r},{c})")
print(f"Is playable ({r},{c})? {is_playable(env.board, r, c)}") # False


env.step(2) #O
env.step(5) #X
env.step(3) #O
env.step(6) #X
env.step(4) #O
env.step(4) #X
env.step(0) #O
env.step(4) #X
env.render()
x_defensives = check_defensive_opportunities(env.board, player_id=1)
o_defensives = check_defensive_opportunities(env.board, player_id=-1)
print(f"\nX defensive opportunities: {x_defensives}") # []  
print(f"O defensive opportunities: {o_defensives}") # []

env.step(3) #O
env.step(0) #X
env.step(3) #O
env.render()
x_defensives = check_defensive_opportunities(env.board, player_id=1)
o_defensives = check_defensive_opportunities(env.board, player_id=-1)
x_attacks = check_attack_opportunities(env.board, player_id=1)
o_attacks = check_attack_opportunities(env.board, player_id=-1)
print(f"\nX defensive opportunities: {x_defensives}") # []  
print(f"O defensive opportunities: {o_defensives}") # []
print(f"X attack opportunities: {x_attacks}") # []
print(f"O attack opportunities: {o_attacks}") # []
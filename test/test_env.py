import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent

# Crea l'ambiente con opponent -> devo solo fare mie mosse
env = Connect4Env(opponent_symbol=-1, opponent=RandomAgent,  render_mode="console")
env.step(3) # X
env.step(3) # X
env.render()

# Crea l'ambiente senza opponent -> faccio mosse di entrambi i giocatori
env = Connect4Env(opponent_symbol=-1,  render_mode="console")
env.step(0) #X
env.step(0) #O
env.render()

# Verifichiamo ricompense [X vince]
env = Connect4Env(opponent_symbol=-1,  render_mode="console")
env.step(0) #X
env.step(1) #O
env.step(0) #X
env.step(1) #O
env.step(2) #X
env.step(1) #O
env.step(6) #X
obs, reward, done, _, _ = env.step(1) #O
env.render()
print(f"Reward X (1): {reward}, Done: {done}") 

# first move random
env = Connect4Env(opponent_symbol=-1, opponent=RandomAgent, render_mode="console", first_move_random=True)
env.step(3) # X
env.step(3) # X
env.render()

from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
import numpy as np


env = Connect4Env(render_mode="console", first_player=1) #Inizia X
env.step(3)
env.render()

env = Connect4Env(render_mode="console", first_player=-1) #Inizia O
env.step(4) 
env.render()

opponent = RandomAgent(None)
env = Connect4Env(opponent = opponent ,render_mode="console", first_player=1) #Inizia X
opponent.env = env
env.force_opponent_opening() # fa giocare l'avversario Random che inizia come X
env.step(np.random.choice(env.get_valid_actions())) #O
env.render()


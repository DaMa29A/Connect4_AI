import os
import numpy as np
from stable_baselines3 import DQN
from env.Connect4Env2 import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from env.env_config import ROWS_COUNT, COLUMNS_COUNT
from gymnasium import spaces
from agents.rl_config import *

if __name__ == "__main__":
    #opponent = RandomAgent(None)
    #opponent = RuleBasedL1Agent(None)
    opponent = RuleBasedL2Agent(None)
    env = Connect4Env(opponent=opponent, render_mode=None)
    opponent.env = env  # collega l'env all'avversario

    if os.path.exists(MODEL_PATH_DQN):
        print(f"Trovato modello esistente: {MODEL_PATH_DQN} — lo carico...")
        model = DQN.load(MODEL_PATH_DQN, env=env)
    else:
        print("Nessun modello trovato, ne creo uno nuovo...")
        model = DQN(
            "MlpPolicy",
            env,
            learning_rate=1e-3,
            buffer_size=50000,
            batch_size=64,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.05,
            exploration_fraction=0.3,
            gamma=0.99,
            target_update_interval=500,
            verbose=1,
            #tensorboard_log="./logs_dqn/"
        )

    # Continua l'addestramento in entrambi i casi
    model.learn(total_timesteps=200_000)
    model.save(MODEL_PATH_DQN)
    print(f"Model saved in {MODEL_PATH_DQN}")
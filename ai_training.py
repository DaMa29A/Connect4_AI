import os
import numpy as np
import time
from datetime import datetime
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.callbacks import BaseCallback
from torch.utils.tensorboard import SummaryWriter
from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.DQNAgent import DQNAgent
from agents.rl_config import MODEL_PATH_DQN, MODEL_PATH_PPO

# Configurazioni
ALGORITHM = "DQN"  # "DQN" o "PPO"
TIME_STEPS = 150_000
START_AI = True
FIRST_MOVE_RANDOM = False

# Scegli l'avversario
#opponent = RandomAgent(None)
#opponent = RuleBasedL1Agent(None)
opponent = RuleBasedL2Agent(None)
#opponent = DQNAgent(None)

# Callback personalizzato per TensorBoard
class ActionLoggerCallback(BaseCallback):
    def __init__(self, writer, log_interval=10000, verbose=0):
        super().__init__(verbose)
        self.writer = writer
        self.action_counts = None
        self.log_interval = log_interval

    def _on_training_start(self):
        self.action_counts = np.zeros(self.training_env.action_space.n)

    def _on_step(self) -> bool:
        actions = self.locals.get("actions", None)
        if actions is not None:
            for a in actions:
                self.action_counts[a] += 1

        if self.num_timesteps % self.log_interval == 0:
            for i, count in enumerate(self.action_counts):
                self.writer.add_scalar(f"action_count/col_{i}", count, self.num_timesteps)
        return True

    def _on_training_end(self):
        for i, count in enumerate(self.action_counts):
            self.writer.add_scalar(f"action_count/col_{i}", count, self.num_timesteps)
        self.writer.close()


env = Connect4Env(opponent=opponent, render_mode=None)
opponent.env = env

if FIRST_MOVE_RANDOM:
    env.step(np.random.choice(env.get_valid_actions()))

# Timestamp leggibile per la run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
writer = SummaryWriter(log_dir=f"./logs/action_distribution_{ALGORITHM.lower()}/run_{timestamp}")

if START_AI:
    env.force_opponent_opening()

policy_kwargs = dict(net_arch=[128, 128])

# Setup modello
if ALGORITHM == "DQN":
    model_path = MODEL_PATH_DQN
    if os.path.exists(model_path):
        print(f"Carico modello DQN da {model_path}")
        model = DQN.load(model_path, env=env)
    else:
        print(f"Creo nuovo modello DQN...")
        model = DQN(
            "MlpPolicy",
            env,
            learning_rate=5e-4,
            buffer_size=100000,
            batch_size=256,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.01,
            exploration_fraction=0.6,
            gamma=0.99,
            target_update_interval=2000, 
            policy_kwargs=policy_kwargs,
            verbose=1,
            tensorboard_log="./logs/logs_dqn_training/"
        )
    model.learn(
        total_timesteps=TIME_STEPS,
        reset_num_timesteps=False,
        callback=ActionLoggerCallback(writer)
    )
    model.save(model_path)
    print(f"Modello DQN salvato in {model_path}")

elif ALGORITHM == "PPO":
    model_path = MODEL_PATH_PPO
    if os.path.exists(model_path):
        print(f"Carico modello PPO da {model_path}")
        model = PPO.load(model_path, env=env)
    else:
        print(f"Creo nuovo modello PPO...")
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=3e-4,          
            n_steps=2048,                
            batch_size=256,              
            n_epochs=10,                 
            gamma=0.995,                 
            gae_lambda=0.95,             
            clip_range=0.2, 
            verbose=1,
            tensorboard_log="./logs/logs_ppo_training/"
        )
    model.learn(
        total_timesteps=TIME_STEPS,
        reset_num_timesteps=False,
        callback=ActionLoggerCallback(writer)
    )
    model.save(model_path)
    print(f"Modello PPO salvato in {model_path}")

else:
    raise ValueError(f"Algoritmo non supportato: {ALGORITHM}")

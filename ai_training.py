import os
from stable_baselines3 import DQN, PPO
from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.rl_config import MODEL_PATH_DQN, MODEL_PATH_PPO

# Configurazioni
ALGORITHM = "DQN"  # "DQN" o "PPO"
TIME_STEPS = 150_000
FIRST_MOVE_RANDOM = False

# Scegli l'avversario
#opponent = RandomAgent
#opponent = RuleBasedL1Agent
opponent = RuleBasedL2Agent
#opponent = DQNAgent

# Start AI
env = Connect4Env(opponent_symbol=-1, opponent=opponent, render_mode=None, first_move_random=FIRST_MOVE_RANDOM)

# Setup modello
policy_kwargs = dict(net_arch=[128, 128])

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
            learning_rate=1e-4,
            buffer_size=50_000,
            batch_size=128,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.01,
            exploration_fraction=0.5,
            gamma=0.99,
            target_update_interval=1000, 
            #policy_kwargs=policy_kwargs,
            verbose=1,
            tensorboard_log="./logs/logs_dqn_training/"
        )
    model.learn(
        total_timesteps=TIME_STEPS,
        reset_num_timesteps=False
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
        reset_num_timesteps=False
    )
    model.save(model_path)
    print(f"Modello PPO salvato in {model_path}")

else:
    raise ValueError(f"Algoritmo non supportato: {ALGORITHM}")
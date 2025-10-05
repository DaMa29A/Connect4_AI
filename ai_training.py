import os
from stable_baselines3 import DQN, PPO
from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.rl_config import MODEL_PATH_DQN, MODEL_PATH_PPO

def train_ai(algorithm, time_steps, opponent, first_move_random):
    # Start AI
    env = Connect4Env(opponent_symbol=-1, opponent=opponent, render_mode=None, first_move_random=first_move_random)

    # Setup modello
    policy_kwargs = dict(net_arch=[128, 128])

    if algorithm == "DQN":
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
                policy_kwargs=policy_kwargs,
                verbose=1,
                tensorboard_log="./logs/logs_dqn_training/"
            )
        model.learn(
            total_timesteps=time_steps,
            reset_num_timesteps=False
        )
        model.save(model_path)
        print(f"Modello DQN salvato in {model_path}")

    elif algorithm == "PPO":
        model_path = MODEL_PATH_PPO
        if os.path.exists(model_path):
            print(f"Carico modello PPO da {model_path}")
            model = PPO.load(model_path, env=env)
        else:
            print(f"Creo nuovo modello PPO...")
            model = PPO(
                "MlpPolicy",
                env,
                # learning_rate=3e-4,          
                # n_steps=2048,                
                # batch_size=256,              
                # n_epochs=10,                 
                # gamma=0.995,                 
                # gae_lambda=0.95,             
                # clip_range=0.2, 
                learning_rate=1e-4,
                n_steps=1024,
                batch_size=256,
                n_epochs=15,
                gamma=0.995,
                gae_lambda=0.98,
                clip_range=0.1,
                verbose=1,
                policy_kwargs=policy_kwargs,
                tensorboard_log="./logs/logs_ppo_training/"
            )
        model.learn(
            total_timesteps=time_steps,
            reset_num_timesteps=False
        )
        model.save(model_path)
        print(f"Modello PPO salvato in {model_path}")

    else:
        raise ValueError(f"Algoritmo non supportato: {ALGORITHM}")


ALGORITHM = "PPO"  # Cambia in "DQN" per usare DQN
train_ai(ALGORITHM, 100_000, RandomAgent, True)
train_ai(ALGORITHM, 100_000, RandomAgent, False)
train_ai(ALGORITHM, 120_000, RuleBasedL1Agent, True)
train_ai(ALGORITHM, 120_000, RuleBasedL1Agent, False)
train_ai(ALGORITHM, 150_000, RuleBasedL2Agent, True)
train_ai(ALGORITHM, 150_000, RuleBasedL2Agent, False)
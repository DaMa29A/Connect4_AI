import os
from stable_baselines3 import DQN, PPO
from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.rl_config import MODEL_PATH_DQN, MODEL_PATH_PPO

# Scegli l'algoritmo: "DQN" oppure "PPO"
ALGORITHM = "DQN"
TIME_STEPS = 100_000

# Scegli l'avversario
opponent = RandomAgent(None)
# opponent = RuleBasedL1Agent(None)
# opponent = RuleBasedL2Agent(None)

# Imposta l'ambiente
env = Connect4Env(opponent=opponent, render_mode=None)
opponent.env = env  # collega l'env all'avversario

# Setup e training
if ALGORITHM == "DQN":
    model_path = MODEL_PATH_DQN
    if os.path.exists(model_path):
        print(f"Trovato modello DQN: {model_path} — lo carico...")
        model = DQN.load(model_path, env=env)
    else:
        print("Nessun modello DQN trovato, ne creo uno nuovo...")
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
            tensorboard_log="./logs/logs_dqn_training/"
        )
    model.learn(total_timesteps=TIME_STEPS)
    model.save(model_path)
    print(f"Modello DQN salvato in {model_path}")

elif ALGORITHM == "PPO":
    model_path = MODEL_PATH_PPO
    if os.path.exists(model_path):
        print(f"Trovato modello PPO: {model_path} — lo carico...")
        model = PPO.load(model_path, env=env)
    else:
        print("Nessun modello PPO trovato, ne creo uno nuovo...")
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=3e-4,
            n_steps=2048,
            batch_size=64,
            n_epochs=10,
            gamma=0.99,
            gae_lambda=0.95,
            clip_range=0.2,
            verbose=1,
            tensorboard_log="./logs/logs_ppo/"
        )
    model.learn(total_timesteps=TIME_STEPS)
    model.save(model_path)
    print(f"Modello PPO salvato in {model_path}")

else:
    raise ValueError(f"Algoritmo non supportato: {ALGORITHM}")
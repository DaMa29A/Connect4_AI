import os
from stable_baselines3 import PPO
from env.Connect4Env2 import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.rl_config import MODEL_PATH_PPO


if __name__ == "__main__":
    opponent = RandomAgent(None)
    env = Connect4Env(opponent=opponent, render_mode=None)
    opponent.env = env  # collega l'env all'avversario

    if os.path.exists(MODEL_PATH_PPO):
        print(f"Trovato modello esistente: {MODEL_PATH_PPO} — lo carico...")
        model = PPO.load(MODEL_PATH_PPO, env=env)
    else:
        print("Nessun modello trovato, ne creo uno nuovo...")
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
            tensorboard_log="./logs_ppo/"
        )

    # Continua l'addestramento in entrambi i casi
    model.learn(total_timesteps=100000)
    model.save(MODEL_PATH_PPO)
    print(f"Modello PPO salvato in {MODEL_PATH_PPO}")

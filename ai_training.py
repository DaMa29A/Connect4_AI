import os
from stable_baselines3 import DQN, PPO
from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.DQNAgent import DQNAgent
from agents.PPOAgent import PPOAgent
import configs.dqn_config as dqn_cfg
import configs.ppo_config as ppo_cfg
from get_statistics import run_match


def train_ai(algorithm, time_steps, opponent, first_move_random, who_start):
    opponent_name = opponent(None).getName() if opponent else "N/A"
    env = Connect4Env(
        opponent_symbol=-who_start, 
        opponent=opponent, 
        render_mode=None, 
        first_move_random=first_move_random)

    if algorithm == "DQN":
        model_path = dqn_cfg.MODEL_PATH
        
        if os.path.exists(model_path):
            print(f"Carico modello DQN da {model_path} e continuo l'allenamento...")
            model = DQN.load(model_path, env=env)
        else:
            print(f"Creo nuovo modello DQN...")
            model = DQN(
                policy=dqn_cfg.POLICY,
                env=env,
                learning_rate=dqn_cfg.LEARNING_RATE,
                buffer_size=dqn_cfg.BUFFER_SIZE,
                batch_size=dqn_cfg.BATCH_SIZE,
                gamma=dqn_cfg.GAMMA,
                target_update_interval=dqn_cfg.TARGET_UPDATE_INTERVAL,
                exploration_initial_eps=dqn_cfg.EXPLORATION_INITIAL_EPS,
                exploration_final_eps=dqn_cfg.EXPLORATION_FINAL_EPS,
                exploration_fraction=dqn_cfg.EXPLORATION_FRACTION,
                policy_kwargs=dqn_cfg.POLICY_KWARGS,
                verbose=dqn_cfg.VERBOSE,
                tensorboard_log=dqn_cfg.TENSORBOARD_LOG
            )
        
        model.learn(
            total_timesteps=time_steps,
            reset_num_timesteps=False,
            tb_log_name=f"DQN_vs_{opponent_name}"
        )
        model.save(model_path)
        print(f"Modello DQN salvato in {model_path}")

    elif algorithm == "PPO":
        model_path = ppo_cfg.MODEL_PATH

        if os.path.exists(model_path):
            print(f"Carico modello PPO da {model_path} e continuo l'allenamento...")
            model = PPO.load(model_path, env=env)
        else:
            print(f"Creo nuovo modello PPO...")
            # Usa i parametri dal file di config ppo_cfg
            model = PPO(
                policy=ppo_cfg.POLICY,
                env=env,
                learning_rate=ppo_cfg.LEARNING_RATE, 
                n_steps=ppo_cfg.N_STEPS,
                batch_size=ppo_cfg.BATCH_SIZE,
                n_epochs=ppo_cfg.N_EPOCHS,
                gamma=ppo_cfg.GAMMA,
                gae_lambda=ppo_cfg.GAE_LAMBDA,
                clip_range=ppo_cfg.CLIP_RANGE,
                ent_coef=ppo_cfg.ENT_COEF,
                verbose=ppo_cfg.VERBOSE,
                policy_kwargs=ppo_cfg.POLICY_KWARGS,
                tensorboard_log=ppo_cfg.TENSORBOARD_LOG
            )
            
        model.learn(
            total_timesteps=time_steps,
            reset_num_timesteps=False,
            tb_log_name=f"PPO_vs_{opponent_name}"
        )
        model.save(model_path)
        print(f"Modello PPO salvato in {model_path}")

    else:
        raise ValueError(f"Algoritmo non supportato: {ALGORITHM}")


BASE_LOG_DIR = "./logs"
BASE_IMAGE_DIR = os.path.join(BASE_LOG_DIR, "images")
if not os.path.exists(BASE_LOG_DIR):
        os.makedirs(BASE_LOG_DIR)
if not os.path.exists(BASE_IMAGE_DIR):
    os.makedirs(BASE_IMAGE_DIR)

# --- Curriculum di Training ---
ALGORITHM = "PPO"  # "DQN" o "PPO"
train_ai(ALGORITHM, 50_000, RandomAgent, True, 1)
train_ai(ALGORITHM, 50_000, RandomAgent, False, 1)
train_ai(ALGORITHM, 150_000, RuleBasedL1Agent, True, 1)
train_ai(ALGORITHM, 150_000, RuleBasedL1Agent, False, 1)
train_ai(ALGORITHM, 225_000, RuleBasedL2Agent, True, 1)
train_ai(ALGORITHM, 225_000, RuleBasedL2Agent, False, 1)
run_match(PPOAgent, RandomAgent)
run_match(PPOAgent, RuleBasedL1Agent)
run_match(PPOAgent, RuleBasedL2Agent)
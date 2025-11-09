import os
import time
import gymnasium as gym
from stable_baselines3 import DQN, PPO
from sb3_contrib import MaskablePPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from colorama import Fore, Style, init
init(autoreset=True)
from env.Connect4Env import Connect4Env 
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL1_2Agent import RuleBasedL1_2Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from sb3_contrib.common.wrappers import ActionMasker
from agents.DQNAgent import DQNAgent
from configs.paths_config import create_paths
from configs.env_config import SEED
from configs.dqn_config import DQN_CONFIGS, POLICY as DQN_POLICY
from configs.ppo_config import PPO_CONFIGS, POLICY as PPO_POLICY

def get_mask_from_env(env):
    return env.unwrapped.get_action_mask()

# --- Custom wrapper to control first column choice ---
class LogFirstActionWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.first_action_logged = False # Flag

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.first_action_logged = False
        return obs, info

    def step(self, action):
        # Check if first episode step
        if not self.first_action_logged:
            print(f"First column choice: {action}")
            self.first_action_logged = True
        return self.env.step(action)

# --- DQN Training ---
def train_dqn(config_name, opponent_class, who_am_i, first_move_random, total_timesteps):
    print(f"{Fore.GREEN}--- Starting DQN Training [{config_name}] ---{Style.RESET_ALL}")

    # Get opponent name
    opponent_name = opponent_class(player_symbol=0).getName() if opponent_class else "N/A"
    
    # Check if config exist
    try:
        config = DQN_CONFIGS[config_name]
    except KeyError:
        print(f"{Fore.RED}Error: '{config_name}' NOT found in DQN.{Style.RESET_ALL}")
        return

    # Paths
    model_file_path, tf_dir_path, ts_file_path, monitor_dir = create_paths("dqn", opponent_name, config_name)

    #
    class_name = opponent_class.__name__
    model_to_load = None
    if class_name == "DQNAgent" or class_name == "PPOAgent":
        model_to_load = model_file_path

    # Env
    env = Connect4Env(opponent_class=opponent_class, who_am_i=who_am_i, first_move_random=first_move_random, model_path=model_to_load)
    env = Monitor(env, filename=monitor_dir)
    env = LogFirstActionWrapper(env)
    env = DummyVecEnv([lambda: env])

    # --- Load/Create Model ---
    if os.path.exists(model_file_path):
        print(f"{Fore.CYAN}Load DQN model '{model_file_path}' ...{Style.RESET_ALL}")
        model = DQN.load(
            model_file_path, 
            env = env,
            tensorboard_log = tf_dir_path
        )
        model.set_random_seed(SEED)
    else:
        print(f"{Fore.CYAN}Create New DQN model (Config: {config_name})...{Style.RESET_ALL}")
        model = DQN(
            DQN_POLICY, 
            env, 
            verbose=1, 
            seed=SEED,
            tensorboard_log=tf_dir_path,
            **config
        )

    start_time = time.time()
    model.learn(
        total_timesteps=total_timesteps, 
        reset_num_timesteps=False, 
        tb_log_name=ts_file_path
    )
    end_time = time.time()
    print(f"DQN training ({config_name} vs {opponent_name}) finished in {end_time - start_time:.2f} s.")
    
    model.save(model_file_path)
    print(f"DQN model saved in {model_file_path}")

# --- PPO Training ---
def train_ppo(config_name, opponent_class, who_am_i, first_move_random, total_timesteps):
    print(f"{Fore.GREEN}--- Starting PPO Training [{config_name}] ---{Style.RESET_ALL}")

    # Get opponent name
    opponent_name = opponent_class(player_symbol=0).getName() if opponent_class else "N/A"
    
    # Check if config exist
    try:
        config = PPO_CONFIGS[config_name]
    except KeyError:
        print(f"{Fore.RED}Error: '{config_name}' NOT found in PPO.{Style.RESET_ALL}")
        return

    # Paths
    model_file_path, tf_dir_path, ts_file_path, monitor_dir = create_paths("ppo", opponent_name, config_name)

    #
    class_name = opponent_class.__name__
    model_to_load = None
    if class_name == "DQNAgent" or class_name == "PPOAgent":
        model_to_load = model_file_path

    # Env
    env = Connect4Env(opponent_class=opponent_class, who_am_i=who_am_i, first_move_random=first_move_random, model_path=model_to_load)
    #env = Monitor(env, filename=monitor_dir)
    #env = LogFirstActionWrapper(env)
    env = ActionMasker(env, get_mask_from_env)
    env = DummyVecEnv([lambda: env])

    # --- Load/Create Model ---
    if os.path.exists(model_file_path):
        print(f"{Fore.CYAN}Load PPO model '{model_file_path}' ...{Style.RESET_ALL}")
        model = MaskablePPO.load(
            model_file_path, 
            env = env,
            tensorboard_log = tf_dir_path
        )
        model.set_random_seed(SEED)
    else:
        print(f"{Fore.CYAN}Create New PPO model (Config: {config_name})...{Style.RESET_ALL}")
        model = MaskablePPO(
            PPO_POLICY, 
            env, 
            verbose=1, 
            seed=SEED,
            tensorboard_log=tf_dir_path,
            **config
        )

    start_time = time.time()
    model.learn(
        total_timesteps=total_timesteps, 
        reset_num_timesteps=False, 
        tb_log_name=ts_file_path
    )
    end_time = time.time()
    print(f"PPO training ({config_name} vs {opponent_name}) finished in {end_time - start_time:.2f} s.")
    
    model.save(model_file_path)
    print(f"PPO model saved in {model_file_path}")

# --- PPO No Mask Training ---
def train_ppo2(config_name, opponent_class, who_am_i, first_move_random, total_timesteps):
    print(f"{Fore.GREEN}--- Starting PPO Training [{config_name}] ---{Style.RESET_ALL}")

    # Get opponent name
    opponent_name = opponent_class(player_symbol=0).getName() if opponent_class else "N/A"
    
    # Check if config exist
    try:
        config = PPO_CONFIGS[config_name]
    except KeyError:
        print(f"{Fore.RED}Error: '{config_name}' NOT found in PPO.{Style.RESET_ALL}")
        return

    # Paths
    model_file_path, tf_dir_path, ts_file_path, monitor_dir = create_paths("ppo", opponent_name, config_name)

    #
    class_name = opponent_class.__name__
    model_to_load = None
    if class_name == "DQNAgent" or class_name == "PPOAgent":
        model_to_load = model_file_path

    # Env
    env = Connect4Env(opponent_class=opponent_class, who_am_i=who_am_i, first_move_random=first_move_random, model_path=model_to_load)
    env = Monitor(env, filename=monitor_dir)
    env = LogFirstActionWrapper(env)
    env = DummyVecEnv([lambda: env])

    # --- Load/Create Model ---
    if os.path.exists(model_file_path):
        print(f"{Fore.CYAN}Load PPO model '{model_file_path}' ...{Style.RESET_ALL}")
        model = PPO.load(
            model_file_path, 
            env = env,
            tensorboard_log = tf_dir_path
        )
        model.set_random_seed(SEED)
    else:
        print(f"{Fore.CYAN}Create New PPO model (Config: {config_name})...{Style.RESET_ALL}")
        model = PPO(
            DQN_POLICY, 
            env, 
            verbose=1, 
            seed=SEED,
            tensorboard_log=tf_dir_path,
            **config
        )

    start_time = time.time()
    model.learn(
        total_timesteps=total_timesteps, 
        reset_num_timesteps=False, 
        tb_log_name=ts_file_path
    )
    end_time = time.time()
    print(f"PPO training ({config_name} vs {opponent_name}) finished in {end_time - start_time:.2f} s.")
    
    model.save(model_file_path)
    print(f"PPO model saved in {model_file_path}")



if __name__ == "__main__":
    # --- Curriculum per DQN ---
    # CONFIG_DQN = "config_5"
    # train_dqn(CONFIG_DQN, RandomAgent, 1, False, 100_000)
    # train_dqn(CONFIG_DQN, RuleBasedL1_2Agent, 1, False, 150_000)
    # train_dqn(CONFIG_DQN, RuleBasedL2Agent, 1, False, 350_000)
    # # train_dqn(CONFIG_DQN, DQNAgent, 1, False, 100_000) #In DQNAgent ricorda di camnbiare nome modello  100k*2

    # --- Curriculum per PPO ---
    CONFIG_PPO = "config_6"
    train_ppo2(CONFIG_PPO, RandomAgent, 1, False, 100_000)
    train_ppo2(CONFIG_PPO, RuleBasedL1_2Agent, 1, False, 150_000)
    train_ppo2(CONFIG_PPO, RuleBasedL2Agent, 1, False, 350_000)
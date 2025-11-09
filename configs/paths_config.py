import os

MODELS_DIR = "models"
LOGS_DIR = "logs"       

# algorithm_name -> must be "dqn" or "ppo"
def create_paths(algorithm_name, opponent_name, config_name):
    # ------------------------ Create dirs structure ------------------------
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Logs
    alg_dir_path = os.path.join(LOGS_DIR, algorithm_name) # logs/dqn
    config_dir_path = os.path.join(alg_dir_path, config_name) # logs/dqn/config_1
    os.makedirs(config_dir_path, exist_ok=True)
    # Logs tensorflow
    tf_dir_path = os.path.join(config_dir_path, "tensorflow") # logs/dqn/config_1/tensorflow    # IN DQN.load
    os.makedirs(tf_dir_path, exist_ok=True)
    # Logs Monitor
    monitor_dir_path = os.path.join(config_dir_path, "monitor") # logs/dqn/config_1/monitor
    os.makedirs(monitor_dir_path, exist_ok=True)
    # Logs Matches
    matches_dir_path = os.path.join(config_dir_path, "matches") # logs/dqn/config_1/matches
    os.makedirs(matches_dir_path, exist_ok=True)

    # ------------------------ Create file name ------------------------
    # Model
    model_file_path = os.path.join(MODELS_DIR, f"{algorithm_name}_{config_name}.zip") # models/dqn_config_1.zip
    # Tensoflow
    ts_file_path = f"{algorithm_name}_vs_{opponent_name}" # IN model.learn
    # Monitor
    monitor_file_path = os.path.join(monitor_dir_path, f"{algorithm_name}_vs_{opponent_name}")

    return model_file_path, tf_dir_path, ts_file_path, monitor_file_path




def create_stats_path(algorithm_name: str, opponent_name: str, config_name: str):
    # logs_evaluation/dqn/config_1/matches
    base_match_dir = os.path.join(LOGS_DIR, algorithm_name, config_name, "matches")
    
    images_path = os.path.join(base_match_dir, "images", f"{algorithm_name}_vs_{opponent_name}")
    os.makedirs(images_path, exist_ok=True)
    
    steps_path = os.path.join(base_match_dir, "steps")
    os.makedirs(steps_path, exist_ok=True)
    
    steps_file_base = f"{algorithm_name}_vs_{opponent_name}.txt"
    steps_file = os.path.join(steps_path, steps_file_base)

    return steps_file, images_path



def get_model_path(algorithm_name, config_name):
    return os.path.join(MODELS_DIR, f"{algorithm_name}_{config_name}.zip") # models/dqn_config_1.zip
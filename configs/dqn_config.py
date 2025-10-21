from configs.rl_config import MODEL_PATH_DQN

# --- Percorsi ---
MODEL_PATH = MODEL_PATH_DQN
TENSORBOARD_LOG = "./logs/logs_dqn_training/"

# --- Architettura di Rete ---
POLICY = "MlpPolicy"
POLICY_KWARGS = dict(net_arch=[128, 128, 64])

# --- Iperparametri DQN ---
LEARNING_RATE = 5e-5
BUFFER_SIZE = 100_000
BATCH_SIZE = 64
GAMMA = 0.998
TARGET_UPDATE_INTERVAL = 1000
EXPLORATION_INITIAL_EPS = 1.0
EXPLORATION_FINAL_EPS = 0.01
EXPLORATION_FRACTION = 0.8
VERBOSE = 1
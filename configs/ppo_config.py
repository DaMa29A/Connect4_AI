from configs.rl_config import MODEL_PATH_PPO

# --- Percorsi ---
MODEL_PATH = MODEL_PATH_PPO
TENSORBOARD_LOG = "./logs/logs_ppo_training/"

# --- Architettura di Rete ---
POLICY = "MlpPolicy"
POLICY_KWARGS = dict(net_arch=[128, 128, 64])

# --- Iperparametri PPO ---
LEARNING_RATE = 3e-4
N_STEPS = 1024
BATCH_SIZE = 128
N_EPOCHS = 10
GAMMA = 0.995
GAE_LAMBDA = 0.95
CLIP_RANGE = 0.2
ENT_COEF = 0.01
VERBOSE = 1
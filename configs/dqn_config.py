# --- Network Architecture ---
POLICY = "MlpPolicy"

# --- Configs ---
config_1_data = {
    "learning_rate": 1e-3,
    "buffer_size": 50_000,   
    "learning_starts": 1_000, ##
    "batch_size": 64,
    "gamma": 0.99,           
    "train_freq": (4, "step"), ##
    "target_update_interval": 500,
    "exploration_initial_eps":1,
    "exploration_fraction": 0.3, 
    "exploration_final_eps": 0.05,
    "policy_kwargs": {
        "net_arch": [64, 64],
    }
}
config_2_data = {
    "learning_rate": 1e-3,
    "buffer_size": 50_000,   
    "learning_starts": 1_000, ##
    "batch_size": 64,
    "gamma": 0.99,           
    "train_freq": (4, "step"), ##
    "target_update_interval": 500,
    "exploration_initial_eps":1,
    "exploration_fraction": 0.3, 
    "exploration_final_eps": 0.05,
    "policy_kwargs": {
        "net_arch": [128, 128, 64],
    }
}
config_3_data = {
    "learning_rate": 1e-4,
    "buffer_size": 50_000, 
    "learning_starts": 1_000,
    "batch_size": 64,
    "gamma": 0.99,
    "train_freq": (4, "step"),
    "target_update_interval": 1000,
    "exploration_initial_eps":1,
    "exploration_fraction": 0.8, 
    "exploration_final_eps": 0.01,
    "policy_kwargs": {
        "net_arch": [128, 128, 64],
    }
}

config_4_data = {
        "learning_rate": 5e-4,        # Più veloce di Config 3, più stabile di Config 1
        "buffer_size": 100_000,       # Più memoria per la rete profonda
        "learning_starts": 1_000,
        "batch_size": 64,
        "gamma": 0.99,
        "train_freq": (4, "step"),
        "target_update_interval": 500, # Aggiornamento aggressivo (da Config 1)
        "exploration_initial_eps":1,
        "exploration_fraction": 0.5,   # Esplorazione media
        "exploration_final_eps": 0.01,
        "policy_kwargs": {
            "net_arch": [128, 128, 64], # Rete profonda
        }
    }

config_5_data =  {
        "learning_rate": 1e-4,        # Basso e Stabile (da Config 3)
        "buffer_size": 100_000,       # Aumentato (da Config 4)
        "learning_starts": 1_000,
        "batch_size": 64,
        "gamma": 0.99,
        "train_freq": (4, "step"),
        "target_update_interval": 1000, # Lento e Stabile (da Config 3)
        "exploration_initial_eps":1,
        "exploration_fraction": 0.8,   
        "exploration_final_eps": 0.01,
        "policy_kwargs": {
            "net_arch": [128, 128, 64], 
        }
    }

DQN_CONFIGS = {
    "config_1": config_1_data,
    "config_1_1": config_1_data,
    "config_1_2": config_1_data,
    "config_1_3": config_1_data,
    "config_1_4": config_1_data,
    "config_2": config_2_data, 
    "config_3": config_3_data,
    "config_4": config_4_data,
    "config_5": config_5_data,
}
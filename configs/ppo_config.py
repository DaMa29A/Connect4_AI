# --- Network Architecture ---
POLICY = "MlpPolicy"

# --- Configs ---
config_1_data = {
    "learning_rate": 3e-4,
    "n_steps": 4096,          
    "batch_size": 512,
    "n_epochs": 10,           
    "gamma": 0.995,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.01,          
    "policy_kwargs": {
        "net_arch": [128, 128, 64]  
    }
}

# config_2_data = {
#     "learning_rate": 3e-4,
#     "n_steps": 2048,          
#     "batch_size": 256,
#     "n_epochs": 10,           
#     "gamma": 0.995,
#     "gae_lambda": 0.95,
#     "clip_range": 0.2,
#     "ent_coef": 0.01,          
#     "policy_kwargs": {
#         "net_arch": [128, 128, 64]  
#     }
# }

config_2_data = {
        "learning_rate": 3.00E-04,
        "n_steps": 2048,          # Aggiornamenti più frequenti
        "batch_size": 256,        # Batch più focalizzati
        "n_epochs": 10,           
        "gamma": 0.995,
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "ent_coef": 0.01,
        "policy_kwargs": {
            "net_arch": [128, 128, 64]
        }
    }

config_3_data = {
        "learning_rate": 2.50E-04,  # Leggermente più stabile
        "n_steps": 2048,          
        "batch_size": 256,
        "n_epochs": 20,           # <-- AUMENTATO: Impara il doppio dai dati
        "gamma": 0.995,
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "ent_coef": 0.01,
        "policy_kwargs": {
            "net_arch": [128, 128, 64]
        }
    }

# config_3_data = {
#     "learning_rate": 2e-4,
#     "n_steps": 1024,          
#     "batch_size": 128,
#     "n_epochs": 10,           
#     "gamma": 0.995,
#     "gae_lambda": 0.95,
#     "clip_range": 0.2,
#     "ent_coef": 0.01,          
#     "policy_kwargs": {
#         "net_arch": [128, 128, 64]  
#     }
# }

config_4_data = {
        "learning_rate": 2.50E-04,
        "n_steps": 1024,          # Aggiornamenti più frequenti
        "batch_size": 128,        # Batch più piccoli
        "n_epochs": 30,           # Ripassa di più!
        "gamma": 0.995,
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "ent_coef": 0.005,        # Meno casualità
        "policy_kwargs": {
            "net_arch": [128, 128, 64]
        }
}

# config_4_data = {
#     "learning_rate": 3e-4,
#     "n_steps": 1024,          
#     "batch_size": 128,
#     "n_epochs": 10,           
#     "gamma": 0.995,
#     "gae_lambda": 0.95,
#     "clip_range": 0.2,
#     "ent_coef": 0.01,          
#     "policy_kwargs": {
#         "net_arch": [128, 128, 64]  
#     }
# }

config_5_data = {
        "learning_rate": 2.50E-04,
        "n_steps": 2048,          
        "batch_size": 256,
        "n_epochs": 20,           
        "gamma": 0.999,           # Aumenta la "pazienza"
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "ent_coef": 0.015,        # Aumenta l'esplorazione
        "policy_kwargs": {
            "net_arch": [128, 128, 64]
        }
    }
    
# config_5_data = {
#     "learning_rate": 4e-4,
#     "n_steps": 2048,          
#     "batch_size": 256,
#     "n_epochs": 10,           
#     "gamma": 0.995,
#     "gae_lambda": 0.95,
#     "clip_range": 0.2,
#     "ent_coef": 0.02,          
#     "policy_kwargs": {
#         "net_arch": [128, 128, 64]  
#     }
# }

# config_6_data = {
#     "learning_rate": 3.5e-4,
#     "n_steps": 2048,          
#     "batch_size": 512,
#     "n_epochs": 10,           
#     "gamma": 0.995,
#     "gae_lambda": 0.95,
#     "clip_range": 0.2,
#     "ent_coef": 0.015,          
#     "policy_kwargs": {
#         "net_arch": [128, 128, 64]  
#     }
# }

config_6_data =  {
        "learning_rate": 2.50E-04,
        "n_steps": 2048,          
        "batch_size": 256,
        "n_epochs": 30,           # <-- AUMENTATO: Ripassa di più
        "gamma": 0.999,           
        "gae_lambda": 0.95,
        "clip_range": 0.2,
        "ent_coef": 0.02,         # <-- AUMENTATO: Esplora di più
        "policy_kwargs": {
            "net_arch": [128, 128, 64]
        }
    }

config_7_data =  {
    "learning_rate": 3.00E-04,
    "n_steps": 4096,          
    "batch_size": 512,
    "n_epochs": 10,           
    "gamma": 0.995,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.02,          
    "policy_kwargs": {
        "net_arch": [128, 128, 64]
    }
}

config_8_data =  {
    "learning_rate": 2.50E-04,
    "n_steps": 4096,          
    "batch_size": 256,
    "n_epochs": 20,           
    "gamma": 0.999,  # Massima pazienza
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.005, # Esplorazione ridotta
    "policy_kwargs": {
        "net_arch": [128, 128, 64]
    }
}


PPO_CONFIGS = {
    "config_1": config_1_data,
    "config_2": config_2_data,
    "config_3": config_3_data,
    "config_4": config_4_data,
    "config_5": config_5_data,
    "config_6": config_6_data,
    "config_7": config_7_data,
    "config_8": config_8_data
}
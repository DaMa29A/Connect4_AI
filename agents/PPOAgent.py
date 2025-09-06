# import numpy as np
# import torch
# from .Agent import Agent
# from stable_baselines3 import PPO
# from .rl_config import MODEL_PATH_PPO

# class PPOAgent(Agent):
#     def __init__(self, env, deterministic=True, device="auto"):
#         super().__init__(env)
#         self.name = "PPO"
#         self.deterministic = deterministic
#         self.model = PPO.load(MODEL_PATH_PPO, device=device)

#     def choose_action(self):
#         valid_moves = self.env.get_valid_actions()
#         if not valid_moves:
#             raise Exception("No valid moves remaining.")

#         obs = self.env.get_board().astype(np.float32)
#         obs = np.expand_dims(obs, axis=0)
#         obs_tensor = torch.as_tensor(obs, device=self.model.device)

#         with torch.no_grad():
#             dist = self.model.policy.get_distribution(obs_tensor)

#             # Logits di dimensione (n_actions,)
#             logits = dist.distribution.logits.squeeze(0).detach().cpu().numpy()

#             # Mascheriamo le mosse illegali
#             mask = self.env.get_action_mask()
#             masked_logits = np.full_like(logits, fill_value=-np.inf, dtype=np.float32)
#             masked_logits[mask == 1] = logits[mask == 1]

#             if self.deterministic:
#                 action = int(np.argmax(masked_logits))
#             else:
#                 # Softmax solo sulle mosse valide
#                 max_logit = np.max(masked_logits[mask == 1])
#                 stable = masked_logits.copy()
#                 stable[mask == 1] -= max_logit
#                 exp_valid = np.exp(stable[mask == 1])
#                 probs_valid = exp_valid / np.sum(exp_valid)
#                 action = int(np.random.choice(np.where(mask == 1)[0], p=probs_valid))

#         return action

import numpy as np
import torch
from .Agent import Agent
from stable_baselines3 import PPO
from .rl_config import MODEL_PATH_PPO

class PPOAgent(Agent):
    def __init__(self, env, deterministic=True, device="auto"):
        super().__init__(env)
        self.name = "PPO"
        self.deterministic = deterministic
        self.model = PPO.load(MODEL_PATH_PPO, device=device)

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        if not valid_moves:
            raise Exception("No valid moves remaining.")

        obs = self.env.get_board().astype(np.float32)
        obs = np.expand_dims(obs, axis=0)
        obs_tensor = torch.as_tensor(obs, device=self.model.device)

        with torch.no_grad():
            dist = self.model.policy.get_distribution(obs_tensor)
            logits = dist.distribution.logits.squeeze(0).detach().cpu().numpy()

        # Maschera per mosse valide
        mask = self.env.get_action_mask()
        masked_logits = np.full_like(logits, fill_value=-np.inf, dtype=np.float32)
        masked_logits[mask == 1] = logits[mask == 1]

        if self.deterministic:
            # Sempre la mossa col logit massimo
            action = int(np.argmax(masked_logits))
        else:
            # Softmax solo sulle mosse valide
            valid_indices = np.where(mask == 1)[0]
            max_logit = np.max(masked_logits[valid_indices])
            stable = masked_logits[valid_indices] - max_logit
            exp_valid = np.exp(stable)
            probs_valid = exp_valid / np.sum(exp_valid)
            action = int(np.random.choice(valid_indices, p=probs_valid))

        return action

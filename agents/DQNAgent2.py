import numpy as np
import torch
from .Agent import Agent
from stable_baselines3 import DQN
from .rl_config import MODEL_PATH_DQN

class DQNAgent(Agent):
    def __init__(self, env, deterministic=True, device="auto"):
        super().__init__(env)
        self.name = "DQN"
        self.deterministic = deterministic
        self.model = DQN.load(MODEL_PATH_DQN, device=device)

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        if not valid_moves:
            raise Exception("No valid moves remaining.")

        obs = self.env.get_board().astype(np.float32)
        obs = np.expand_dims(obs, axis=0)
        obs_tensor = torch.as_tensor(obs, device=self.model.device)

        with torch.no_grad():
            q_values = self.model.policy.q_net(obs_tensor)

        q_values = q_values.cpu().numpy().flatten()

        # ❌ Settiamo -inf per mosse illegali
        mask = self.env.get_action_mask()
        q_values[mask == 0] = -np.inf

        action = int(np.argmax(q_values))
        return action

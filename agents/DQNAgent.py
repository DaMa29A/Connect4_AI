import numpy as np
import torch
from .Agent import Agent
from stable_baselines3 import DQN
from colorama import Fore

class DQNAgent(Agent):
    def __init__(self, name="DQN", player_symbol=None, deterministic=True, model_path="./models/dqn_config_1.zip"):
        super().__init__(name, player_symbol=player_symbol)
        self.deterministic = deterministic 

        try:
            self.model = DQN.load(model_path, device="auto")
            print(f"DQN model loaded from: {model_path}")
        except Exception as e:
            print(f"{Fore.RED}Error loading DQN model: {e}")
            raise

    # Chooses the best action by applying the mask to the model's Q-values.
    def choose_action(self, obs, action_mask):  
        # 1. Convert to tensor
        obs_tensor = torch.as_tensor(obs, device=self.model.device).unsqueeze(0)
        
        # 2. Get the Q-values
        with torch.no_grad():
            q_values = self.model.q_net(obs_tensor)
            q_values_np = q_values.cpu().numpy().squeeze(0)

        # 3. Apply the mask
        masked_q_values = np.full_like(q_values_np, -np.inf)
        valid_indices = np.where(action_mask == 1)[0]
        
        # Security check: exit if no valid moves
        if len(valid_indices) == 0:
            raise RuntimeError("No valid actions available") 

        masked_q_values[valid_indices] = q_values_np[valid_indices]
        
        # 4. Deterministic checks
        if self.deterministic:
            # Always select the action with the highest score.
            action = np.argmax(masked_q_values) 
        else:
            # Extract Q-values for valid moves only
            valid_q_values = masked_q_values[valid_indices] 
            # Stabilize Softmax (subtract the max to prevent overflow)
            max_q = np.max(valid_q_values)
            stable_q = valid_q_values - max_q
            # Calculate the probabilities
            exp_q = np.exp(stable_q)
            probs = exp_q / np.sum(exp_q)
            # Sample from the valid indices using the calculated probabilities
            action = np.random.choice(valid_indices, p=probs)

        return int(action)
from .Agent import Agent
from sb3_contrib import MaskablePPO
from colorama import Fore

class PPOAgent(Agent):
    def __init__(self, name="PPO", player_symbol=None, deterministic=True, model_path="./models/ppo_config_1.zip"):
        super().__init__(name, player_symbol=player_symbol)
        self.deterministic = deterministic 

        try:
            self.model = MaskablePPO.load(model_path, device="auto")
            print(f"PPO model loaded from: {model_path}")
        except Exception as e:
            print(f"{Fore.RED}Error loading PPO model: {e}")
            raise

    def choose_action(self, obs, action_mask):
        action, _states = self.model.predict(
            obs, 
            action_masks=action_mask,
            deterministic=self.deterministic
        )
        return int(action)
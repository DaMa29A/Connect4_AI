import numpy as np
import torch
from .Agent import Agent
from stable_baselines3 import PPO
from .rl_config import MODEL_PATH_PPO


class PPOAgent(Agent):
    def __init__(self, env, deterministic=True, device="auto"):
        """
        env: istanza di Connect4Env (o compatibile)
        deterministic: True = azione greedy (argmax tra mosse valide), False = campiona tra mosse valide
        device: "auto", "cpu", "cuda", o indice GPU
        """
        super().__init__(env)
        self.name = "PPO"
        self.deterministic = deterministic
        self.model = PPO.load(MODEL_PATH_PPO, device=device)

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        if not valid_moves:
            raise Exception("No valid moves remaining.")

        # Osservazione come float32 con dimensione batch
        obs = self.env.get_board().astype(np.float32)
        obs = np.expand_dims(obs, axis=0)

        # Tensore sul device del modello
        obs_tensor = torch.as_tensor(obs, device=self.model.device)

        # Ottieni la distribuzione delle azioni dalla policy (Categorical)
        with torch.no_grad():
            dist = self.model.policy.get_distribution(obs_tensor)
            # SB3 usa una Categorical con logits/probs di shape (batch, n_actions)
            if hasattr(dist.distribution, "logits") and dist.distribution.logits is not None:
                logits = dist.distribution.logits.squeeze(0)  # (n_actions,)
                logits_np = logits.detach().cpu().numpy()
                # Maschera: -inf sulle mosse NON valide
                masked_logits = np.full_like(logits_np, fill_value=-np.inf, dtype=np.float32)
                masked_logits[valid_moves] = logits_np[valid_moves]

                if self.deterministic:
                    action = int(np.argmax(masked_logits))
                else:
                    # Softmax solo sulle mosse valide
                    max_logit = np.max(masked_logits[valid_moves])
                    stable = masked_logits.copy()
                    stable[valid_moves] = stable[valid_moves] - max_logit
                    exp_valid = np.exp(stable[valid_moves])
                    probs_valid = exp_valid / np.sum(exp_valid)
                    action = int(np.random.choice(valid_moves, p=probs_valid))
            else:
                # Fallback: se per qualche motivo non abbiamo logits, usa predict e riprova finché non è valida
                action_pred, _ = self.model.predict(self.env.get_board(), deterministic=self.deterministic)
                if action_pred in valid_moves:
                    action = int(action_pred)
                else:
                    # prendi la migliore valida come ripiego
                    action = int(np.random.choice(valid_moves))

        print(f"Azione scelta (PPO, masked): {action}")

        # Debug opzionale, come nel DQNAgent
        action2, _ = self.model.predict(self.env.get_board(), deterministic=True)
        print(f"Azione scelta 2 (PPO .predict): {action2}")

        return action
import numpy as np
import torch
from .Agent import Agent
from stable_baselines3 import PPO # <-- PPO standard
from colorama import Fore

class PPOAgent(Agent):
    def __init__(self, name="PPO", player_symbol=None, deterministic=True, model_path="./models/ppo_config_1.zip"):
        super().__init__(name, player_symbol=player_symbol)
        self.deterministic = deterministic 

        try:
            # Carica il modello PPO standard
            self.model = PPO.load(model_path, device="auto")
            print(f"PPO model loaded from: {model_path}")
        except Exception as e:
            print(f"{Fore.RED}Error loading PPO model: {e}")
            raise

    # L'agente estrae i punteggi logits della policy e maschera a mano
    def choose_action(self, obs, action_mask):  
        
        # 1. Converti l'osservazione (numpy array) in un tensore PyTorch
        obs_tensor = torch.as_tensor(obs, device=self.model.device).unsqueeze(0)
        
        # 2. Ottieni la distribuzione delle azioni (policy)
        with torch.no_grad():
            # POLICY: Ottiene la distribuzione e gli stati del valore (value states)
            # Obs. è passato come tensore: (1, 6, 7)
            dist = self.model.policy.get_distribution(obs_tensor)
            
            # LOGITS: Estrai i punteggi non normalizzati per le 7 azioni
            # Squeeze rimuove la dimensione batch
            logits = dist.distribution.logits.squeeze(0).cpu().numpy()

        # 3. Applica la maschera (identico alla logica del tuo DQNAgent)
        masked_logits = np.full_like(logits, fill_value=-np.inf)
        valid_indices = np.where(action_mask == 1)[0]
        
        # Se non ci sono mosse valide, lancia l'eccezione
        if len(valid_indices) == 0:
            raise RuntimeError("No valid actions available") 

        # Applica i logits solo agli indici validi
        masked_logits[valid_indices] = logits[valid_indices]
        
        # 4. Scegli l'azione
        if self.deterministic:
            # Scegli l'azione con il logit più alto tra quelle valide
            action = np.argmax(masked_logits)
        else:
            # Scelta non deterministica (Campionamento Softmax)
            valid_logits = masked_logits[valid_indices] 
            
            # Stabilizza Softmax (per evitare problemi numerici)
            max_logit = np.max(valid_logits)
            stable_logits = valid_logits - max_logit
            
            # Calcola le probabilità e campiona
            exp_probs = np.exp(stable_logits)
            probs = exp_probs / np.sum(exp_probs)
            
            action = np.random.choice(valid_indices, p=probs)

        return int(action)
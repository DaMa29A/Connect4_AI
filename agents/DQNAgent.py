import numpy as np
import torch
from .Agent import Agent
from stable_baselines3 import DQN
from .rl_config import *

class DQNAgent(Agent):
    def __init__(self, env, deterministic=True, device="auto"):
        """
        env: istanza di Connect4Env (o compatibile)
        model_path: percorso del modello DQN salvato
        deterministic: True = azioni greedy, False = stocastiche (se supportato)
        device: "auto", "cpu", "cuda", o indice GPU
        """
        super().__init__(env)
        self.name = "DQN"
        self.deterministic = deterministic
        self.model = DQN.load(MODEL_PATH_DQN, device=device)

    def choose_action(self):
        valid_moves = self.env.get_valid_actions()
        if not valid_moves:
            raise Exception("No valid moves remaining.")

        # Prepara osservazione in float32 e con dimensione batch
        obs = self.env.get_board().astype(np.float32)
        obs = np.expand_dims(obs, axis=0)

        # Converti in tensore Torch sul device corretto
        obs_tensor = torch.as_tensor(obs, device=self.model.device)

        # Ottieni Q-values dalla rete neurale
        with torch.no_grad():
            q_values = self.model.policy.q_net(obs_tensor)

        q_values = q_values.cpu().numpy().flatten()

        # Maschera mosse illegali
        mask = np.full_like(q_values, fill_value=-np.inf, dtype=np.float32)
        mask[valid_moves] = q_values[valid_moves]

        # Seleziona la mossa migliore tra quelle valide
        #print(f"Maske: {mask}, Q-values: {q_values}")
        action = int(np.argmax(mask))
        print(f"Azione scelta: {action}")
        
        
        
        ## Tutto il codice potrebbe essere ridotto a questa linea di codice e restituire action2
        ## Ma action contiene solo mosse valide (colonne non piene), action2 potrebbe contenere anche quelle invalide (piene)
        action2, _ = self.model.predict(self.env.get_board(), deterministic=True)
        print(f"Azione scelta 2: {action2}")
        
        
        return action

    def getName(self):
        return self.name
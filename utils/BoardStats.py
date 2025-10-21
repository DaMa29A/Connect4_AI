import numpy as np
from utils.check_rules import check_attack_opportunities 
from configs.env_config import ROWS_COUNT, COLUMNS_COUNT

class BoardStats:
    def __init__(self):
        # DIZIONARI: {(r, c, player_id): length}
        self.attack_moves = {}       
        self.defensive_moves = {}    
        self.attacks_done = {}       
        self.defenses_done = {}      

    def add_move(self, move_type, r, c, player_id, length):
        """Aggiunge una mossa al dizionario con la sua lunghezza."""
        key = (r, c, player_id)
        if move_type == 0:   # attacco
            self.attack_moves[key] = length
        elif move_type == 1: # difesa
            self.defensive_moves[key] = length

    def remove_move(self, move_type, r, c, player_id):
        """Rimuove una mossa dal dizionario usando la chiave."""
        key = (r, c, player_id)
        if move_type == 0:
            self.attack_moves.pop(key, None)
        elif move_type == 1:
            self.defensive_moves.pop(key, None)

    def update_after_move(self, board, r, c, player_id):
        """
        Aggiorna le statistiche dopo che 'player_id' ha giocato in (r, c).
        """
        opponent_id = -player_id
        key = (r, c, player_id)
        opp_key = (r, c, opponent_id)

        # --- FASE 1: Controlla se la mossa attuale completa un'opportunità ---
        
        # Attacco completato
        if key in self.attack_moves:
            # Prendi la lunghezza della minaccia prima di rimuoverla
            length = self.attack_moves.pop(key)
            self.defensive_moves.pop(opp_key, None) 
            
            # Aggiungi a 'done' CON la sua lunghezza
            self.attacks_done[key] = length

        # Difesa effettuata
        elif key in self.defensive_moves:
            # Prendi la lunghezza della minaccia che stavi bloccando
            length = self.defensive_moves.pop(key)
            self.attack_moves.pop(opp_key, None)
            
            # Aggiungi a 'done' CON la sua lunghezza
            self.defenses_done[key] = length
        

        # --- FASE 2: Ricalcola TUTTE le opportunità sulla nuova board ---
        
        self.attack_moves.clear()
        self.defensive_moves.clear()
        
        for p_id in [player_id, opponent_id]:
            opp_id = -p_id
            
            # Cerca minacce da 4 (Vittorie)
            threats_4 = check_attack_opportunities(board, p_id, target_count=4)
            for rr, cc, _ in threats_4:
                move_key = (rr, cc, p_id)
                # Non ri-aggiungere se è già stata completata
                if move_key not in self.attacks_done:
                    # Aggiunge o SOVRASCRIVE con il valore 4
                    self.add_move(0, rr, cc, p_id, 4)
                    self.add_move(1, rr, cc, opp_id, 4)
            
            # Cerca minacce da 3 (Triplette)
            threats_3 = check_attack_opportunities(board, p_id, target_count=3)
            for rr, cc, _ in threats_3:
                move_key = (rr, cc, p_id)
                # NON AGGIUNGERE SE:
                # 1. È già stata completata (è in attacks_done)
                # 2. È GIA' STATA REGISTRATA COME MINACCIA DA 4 (ha priorità)
                if move_key not in self.attacks_done and \
                   move_key not in self.attack_moves:
                    self.add_move(0, rr, cc, p_id, 3)
                    self.add_move(1, rr, cc, opp_id, 3)

    def get_attacks(self, player_id=None):
        """Restituisce una lista di tuple (r, c, pid, length)."""
        if player_id is None:
            return [(k[0], k[1], k[2], v) for k, v in self.attack_moves.items()]
        return [(k[0], k[1], k[2], v) for k, v in self.attack_moves.items() if k[2] == player_id]

    def get_defensives(self, player_id=None):
        """Restituisce una lista di tuple (r, c, pid, length)."""
        if player_id is None:
            return [(k[0], k[1], k[2], v) for k, v in self.defensive_moves.items()]
        return [(k[0], k[1], k[2], v) for k, v in self.defensive_moves.items() if k[2] == player_id]

    def get_attacks_done(self, player_id=None):
        """Restituisce una lista di tuple (r, c, pid, length)."""
        if player_id is None:
            return [(k[0], k[1], k[2], v) for k, v in self.attacks_done.items()]
        return [(k[0], k[1], k[2], v) for k, v in self.attacks_done.items() if k[2] == player_id]

    def get_defenses_done(self, player_id=None):
        """Restituisce una lista di tuple (r, c, pid, length)."""
        if player_id is None:
            return [(k[0], k[1], k[2], v) for k, v in self.defenses_done.items()]
        return [(k[0], k[1], k[2], v) for k, v in self.defenses_done.items() if k[2] == player_id]

    def reset(self):
        self.attack_moves.clear()
        self.defensive_moves.clear()
        self.attacks_done.clear()
        self.defenses_done.clear()

    def __repr__(self):
        repr_str = "────────────────────────────\n"
        # Aggiorna la stampa per includere la lunghezza (length)
        repr_str += "[Attack] opportunities for X (1): " + str(self.get_attacks(1)) + "\n"
        repr_str += "[Attack] opportunities for O (-1): " + str(self.get_attacks(-1)) + "\n"
        repr_str += "[Defense] opportunities for X (1): " + str(self.get_defensives(1)) + "\n"
        repr_str += "[Defense] opportunities for O (-1): " + str(self.get_defensives(-1)) + "\n"
        
        repr_str += "[Attacks done X]: " + str(self.get_attacks_done(1)) + "\n"
        repr_str += "[Attacks done O]: " + str(self.get_attacks_done(-1)) + "\n"
        repr_str += "[Defenses done X]: " + str(self.get_defenses_done(1)) + "\n"
        repr_str += "[Defenses done O]: " + str(self.get_defenses_done(-1)) + "\n"
        repr_str += "────────────────────────────"
        return repr_str
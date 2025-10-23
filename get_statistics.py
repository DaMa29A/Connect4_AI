import os
import datetime # Importa datetime per i timestamp
from env.Connect4Env import Connect4Env
from agents.HumanAgent import HumanAgent
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.PPOAgent import PPOAgent
from agents.DQNAgent import DQNAgent
import numpy as np
from utils.BoardStats import BoardStats
from utils.logger import *
from utils.plots import *


NUM_GAMES = 500  # Numero di partite per ogni match-up
BASE_LOG_DIR = "./logs"
BASE_IMAGE_DIR = os.path.join(BASE_LOG_DIR, "images")
RENDER_MODE = None # "console" or None

def run_match(agent1_class, agent2_class):
    """
    Esegue NUM_GAMES partite tra due tipi di agenti specificati
    e salva log e grafici in cartelle/file univoci.
    """
    
    # --- Inizializzazione Ambiente e Agenti ---
    # Nota: L'ambiente viene creato qui per passare 'env' agli agenti
    env = Connect4Env(render_mode=RENDER_MODE) 
    
    # Crea istanze degli agenti passati come classi
    # Passa l'ambiente 'env' creato sopra
    if agent2_class == DQNAgent:
        env = Connect4Env(render_mode=RENDER_MODE, first_move_random=True)
        agent1 = PPOAgent(env, deterministic=True, path="models/ppo_connect4_C3.zip")
        agent2 = DQNAgent(env, deterministic=True, path="models/dqn_connect4_C5.zip")
    elif agent2_class == PPOAgent:
        env = Connect4Env(render_mode=RENDER_MODE, first_move_random=True)
        agent1 = DQNAgent(env, deterministic=True, path="models/dqn_connect4_C5.zip")
        agent2 = PPOAgent(env, deterministic=True, path="models/ppo_connect4_C3.zip")
    else:
        agent1 = agent1_class(env) 
        agent2 = agent2_class(env)

    
    agent_names = {"X": agent1.getName(), "O": agent2.getName()}
    print("\n" + "="*60)
    print(f"Avvio Match: {agent_names['X']} (X) vs {agent_names['O']} (O) - {NUM_GAMES} partite")
    print("="*60)

    # --- Creazione Nomi File/Cartelle Univoci ---
    match_id = f"{agent_names['X']}_vs_{agent_names['O']}" # Es: DQN_vs_RB_L3
    # Aggiungi un timestamp per evitare sovrascritture se eseguito più volte
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"{match_id}_{timestamp}" 

    # Percorso per il file di log testuale
    log_file_path = os.path.join(BASE_LOG_DIR, f"game_log_{run_id}.txt")
    
    # Percorso per la sottocartella delle immagini
    image_subdir = os.path.join(BASE_IMAGE_DIR, run_id)
    if not os.path.exists(image_subdir):
        os.makedirs(image_subdir)
        print(f"Cartella immagini creata: {image_subdir}")
        
    # Nomi file per i grafici
    match_plot_path = os.path.join(image_subdir, "match_results.png")
    defense_plot_path = os.path.join(image_subdir, "defense_summary.png")
    offense_plot_path = os.path.join(image_subdir, "offense_summary.png")

    # --- Inizializzazione Statistiche ---
    results = {"X": 0, "O": 0, "Draw": 0}
    def_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
    attack_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
    board_stats = BoardStats()

    # --- Partite ---
    # Rimuovi il vecchio log se esiste 
    if os.path.exists(log_file_path):
         os.remove(log_file_path) 

    with open(log_file_path, "w", encoding="utf-8") as f:
        write_header(f, agent_names["X"], agent_names["O"])

        for game_num in range(1, NUM_GAMES + 1):
            if game_num % 50 == 0: # Stampa un aggiornamento ogni 50 partite
                 print(f"  Partita {game_num}/{NUM_GAMES}...")
                 
            write_game_start(f, game_num)
            obs, info = env.reset() # Resetta l'ambiente per ogni partita
            board_stats.reset()
            done = False
            step_count = 0
            
            # Stampa la board iniziale se in modalità console
            if RENDER_MODE == "console":
                 env.render() 
            
            while not done:
                current_player = env.next_player_to_play
                agent = agent1 if current_player == 1 else agent2
                player_symbol = "X" if current_player == 1 else "O"
                agent_name = agent_names[player_symbol]

                action = agent.choose_action()
                
                # Gestisci caso HumanAgent che potrebbe non avere row/col subito
                row, col = -1, -1 
                if isinstance(agent, HumanAgent):
                     col = action 
                     # Row viene calcolata dopo play_action, ma per il log serve prima
                     # Simula per ottenere la riga (non ideale ma funziona per il log)
                     temp_r = env.get_first_empty_row(action)
                     if temp_r is not None: row = temp_r
                else:
                    row = env.get_first_empty_row(action)
                    col = action

                # Controlla se la mossa è valida prima di procedere
                if row is None or col < 0:
                     print(f"Errore: Mossa non valida tentata da {agent_name} (Col: {col}). Salto turno?")
                     valid_actions = env.get_valid_actions()
                     if not valid_actions:
                          done = True
                          env.winner = 0 
                          break
                     action = np.random.choice(valid_actions)
                     row = env.get_first_empty_row(action)
                     col = action
                     
                is_defensive_play = (row, col, current_player) in board_stats.defensive_moves
                is_offensive_play = (row, col, current_player) in board_stats.attack_moves
                old_attacks = set(board_stats.attack_moves.keys())
                old_defenses = set(board_stats.defensive_moves.keys())

                obs, reward, done, _, _ = env.step(action)
                board_stats.update_after_move(env.board, row, col, current_player)

                step_count += 1
                if RENDER_MODE == "console":
                    env.render()

                write_turn_info(f, step_count, agent_name, player_symbol, row, col, reward)
                write_board(f, env.board)

                if is_defensive_play:
                    write_success(f, "DEFENSIVE", player_symbol, row, col)
                if is_offensive_play:
                    write_success(f, "ATTACK", player_symbol, row, col)

                new_attacks = set(board_stats.attack_moves.keys())
                new_defenses = set(board_stats.defensive_moves.keys())
                added_attacks = new_attacks - old_attacks
                for r_new, c_new, pid in added_attacks:
                    symbol = "X" if pid == 1 else "O"
                    write_opportunity(f, "Attack", symbol, r_new, c_new)
                added_defenses = new_defenses - old_defenses
                for r_new, c_new, pid in added_defenses:
                    symbol = "X" if pid == 1 else "O"
                    write_opportunity(f, "Defensive", symbol, r_new, c_new)
                
                f.write(str(board_stats) + "\n")

                if done:
                    break

            # Fine partita: Aggiorna statistiche cumulative
            attacks_done_X = board_stats.get_attacks_done(1)
            attacks_open_X = board_stats.get_attacks(1)
            defenses_done_X = board_stats.get_defenses_done(1)
            defenses_open_X = board_stats.get_defensives(1)
            attack_stats["X"]["occasions"] += len(attacks_done_X) + len(attacks_open_X)
            attack_stats["X"]["success"] += len(attacks_done_X)
            def_stats["X"]["occasions"] += len(defenses_done_X) + len(defenses_open_X)
            def_stats["X"]["success"] += len(defenses_done_X)

            attacks_done_O = board_stats.get_attacks_done(-1)
            attacks_open_O = board_stats.get_attacks(-1)
            defenses_done_O = board_stats.get_defenses_done(-1)
            defenses_open_O = board_stats.get_defensives(-1)
            attack_stats["O"]["occasions"] += len(attacks_done_O) + len(attacks_open_O)
            attack_stats["O"]["success"] += len(attacks_done_O)
            def_stats["O"]["occasions"] += len(defenses_done_O) + len(defenses_open_O)
            def_stats["O"]["success"] += len(defenses_done_O)

            winner = env.get_winner()
            if winner == 1:
                results["X"] += 1
            elif winner == -1:
                results["O"] += 1
            else:
                results["Draw"] += 1
            write_game_result(f, winner)

        # Fine ciclo partite
        write_final_stats(f, results, def_stats, attack_stats, agent_names["X"], agent_names["O"])
        print(f"Match completato. Log salvato in: {log_file_path}")

    # --- Salvataggio Grafici ---
    print(f"Salvataggio grafici in {image_subdir}...")
    try:
        plot_match_results(results, agent_names["X"], agent_names["O"], output_path=match_plot_path)
        plot_defense_summary(def_stats, agent_names["X"], agent_names["O"], output_path=defense_plot_path)
        plot_offense_summary(attack_stats, agent_names["X"], agent_names["O"], output_path=offense_plot_path)
        print("Grafici salvati.")
    except Exception as e:
         print(f"Errore durante il salvataggio dei grafici: {e}")


if __name__ == "__main__":
    # Assicurati che le cartelle base esistano
    if not os.path.exists(BASE_LOG_DIR):
        os.makedirs(BASE_LOG_DIR)
    if not os.path.exists(BASE_IMAGE_DIR):
        os.makedirs(BASE_IMAGE_DIR)

    # run_match(DQNAgent, RandomAgent)
    # run_match(DQNAgent, RuleBasedL1Agent)
    # run_match(DQNAgent, RuleBasedL2Agent)
    
    # run_match(PPOAgent, RandomAgent)
    # run_match(PPOAgent, RuleBasedL1Agent)
    # run_match(PPOAgent, RuleBasedL2Agent)

    # run_match(DQNAgent, PPOAgent)
    # run_match(PPOAgent, DQNAgent)

    print("\n--- Tutte le simulazioni completate ---")
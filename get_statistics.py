import os
import datetime
import numpy as np
import time
from colorama import Fore, Style, init
from env.Connect4Env import Connect4Env
from agents.HumanAgent import HumanAgent
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.RuleBasedL1_2Agent import RuleBasedL1_2Agent
from agents.PPOAgent import PPOAgent
from agents.DQNAgent import DQNAgent
from configs.paths_config import get_model_path, create_stats_path
from configs.env_config import SEED
from utils.BoardStats import BoardStats
from utils.logger import *
from utils.plots import *
init(autoreset=True)

# --- Configurazione Match ---
NUM_GAMES = 500
RENDER_MODE = None #"console" o None (GUI non supportata in questo loop)


def run_match(agent1_class, agent2_class, agent1_kwargs={}, agent2_kwargs={}, config="_", rand=False):
    agent1 = agent1_class(player_symbol=1, **agent1_kwargs)
    agent2 = agent2_class(player_symbol=-1, **agent2_kwargs)

    agent_names = {"X": agent1.getName(), "O": agent2.getName()}
    print("\n" + "="*60)
    print(f"Avvio Match: {agent_names['X']} (X) vs {agent_names['O']} (O) - {NUM_GAMES} partite")
    print("="*60)

    # Create env
    env = Connect4Env(render_mode=RENDER_MODE, self_play=True, first_move_random=rand) 

    # Files names
    steps_file, images_dir = create_stats_path(agent_names['X'], agent_names['O'], config)
    match_plot_path = os.path.join(images_dir, "match_results.png")
    defense_plot_path = os.path.join(images_dir, "defense_summary.png")
    offense_plot_path = os.path.join(images_dir, "offense_summary.png")

    # Stats
    results = {"X": 0, "O": 0, "Draw": 0}
    def_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
    attack_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}

    # Loop Matches
    if os.path.exists(steps_file):
        os.remove(steps_file)
    if os.path.exists(match_plot_path):
        os.remove(match_plot_path) 
    if os.path.exists(defense_plot_path):
        os.remove(defense_plot_path)
    if os.path.exists(offense_plot_path):
        os.remove(offense_plot_path)

    with open(steps_file, "w", encoding="utf-8") as f:
        write_header(f, agent_names["X"], agent_names["O"])

        for game_num in range(1, NUM_GAMES + 1):
            if game_num % (NUM_GAMES // 10) == 0: # Stampa 10 aggiornamenti
                print(f"Match {game_num}/{NUM_GAMES}...")
                
            write_game_start(f, game_num)
            
            # seed diverso per ogni partita altrimenti gioca sempre la stessa partita)
            episode_seed = SEED + game_num
            obs, info = env.reset(seed=episode_seed) 
            done = False
            step_count = 0
            
            if RENDER_MODE == "console":
                env.render() 
            
            while not done:
                current_player = env.next_player_to_play
                agent = agent1 if current_player == 1 else agent2
                player_symbol = "X" if current_player == 1 else "O"
                agent_name = agent_names[player_symbol]
                
                # --- MODIFICA CHIAVE API ---
                # Passa obs e action_mask all'agente
                action_mask = info["action_mask"]
                action = agent.choose_action(obs, action_mask)
                # -------------------------
                
                # Ottieni la riga *prima* dello step per il logging
                row = env.get_first_empty_row(action)
                if row is None: row = -1 # Mossa non valida
                col = action

                # Controlla stato *prima* della mossa per le stats
                board_stats = env.board_stats # Prendi l'oggetto stats
                is_defensive_play = (row, col, current_player) in board_stats.defensive_moves
                is_offensive_play = (row, col, current_player) in board_stats.attack_moves
                old_attacks = set(board_stats.attack_moves.keys())
                old_defenses = set(board_stats.defensive_moves.keys())

                # Esegui lo step
                obs, reward, done, _, info = env.step(action)
                step_count += 1
                
                if RENDER_MODE == "console":
                    env.render()

                # Logga il turno (ora 'info' contiene i dati aggiornati)
                write_turn_info(f, step_count, agent_name, player_symbol, info["last_move_row"], info["last_move_col"], reward)
                write_board(f, env.board)

                # Logga le stats (usa l'oggetto stats *aggiornato* da 'info')
                board_stats_updated = info["board_stats"]
                
                if is_defensive_play:
                    write_success(f, "DEFENSIVE", player_symbol, row, col)
                if is_offensive_play:
                    write_success(f, "ATTACK", player_symbol, row, col)

                new_attacks = set(board_stats_updated.attack_moves.keys())
                new_defenses = set(board_stats_updated.defensive_moves.keys())
                added_attacks = new_attacks - old_attacks
                for r_new, c_new, pid in added_attacks:
                    symbol = "X" if pid == 1 else "O"
                    write_opportunity(f, "Attack", symbol, r_new, c_new)
                added_defenses = new_defenses - old_defenses
                for r_new, c_new, pid in added_defenses:
                    symbol = "X" if pid == 1 else "O"
                    write_opportunity(f, "Defensive", symbol, r_new, c_new)
                
                f.write(str(board_stats_updated) + "\n")

                if done:
                    break

            # --- Fine partita: Aggiorna statistiche cumulative ---
            final_board_stats = info["board_stats"]
            
            # Statistiche per X (P1)
            attacks_done_X = final_board_stats.get_attacks_done(1)
            attacks_open_X = final_board_stats.get_attacks(1)
            defenses_done_X = final_board_stats.get_defenses_done(1)
            defenses_open_X = final_board_stats.get_defensives(1)
            attack_stats["X"]["occasions"] += len(attacks_done_X) + len(attacks_open_X)
            attack_stats["X"]["success"] += len(attacks_done_X)
            def_stats["X"]["occasions"] += len(defenses_done_X) + len(defenses_open_X)
            def_stats["X"]["success"] += len(defenses_done_X)

            # Statistiche per O (P2)
            attacks_done_O = final_board_stats.get_attacks_done(-1)
            attacks_open_O = final_board_stats.get_attacks(-1)
            defenses_done_O = final_board_stats.get_defenses_done(-1)
            defenses_open_O = final_board_stats.get_defensives(-1)
            attack_stats["O"]["occasions"] += len(attacks_done_O) + len(attacks_open_O)
            attack_stats["O"]["success"] += len(attacks_done_O)
            def_stats["O"]["occasions"] += len(defenses_done_O) + len(defenses_open_O)
            def_stats["O"]["success"] += len(defenses_done_O)

            # Risultati
            winner = env.get_winner()
            if winner == 1: results["X"] += 1
            elif winner == -1: results["O"] += 1
            else: results["Draw"] += 1
            write_game_result(f, winner)

        # Fine ciclo partite
        write_final_stats(f, results, def_stats, attack_stats, agent_names["X"], agent_names["O"])
        print(f"Match completato. Log salvato in: {steps_file}")

    # --- Salvataggio Grafici ---
    print(f"Salvataggio grafici in {images_dir}...")
    try:
        plot_match_results(results, agent_names["X"], agent_names["O"], output_path=match_plot_path)
        plot_defense_summary(def_stats, agent_names["X"], agent_names["O"], output_path=defense_plot_path)
        plot_offense_summary(attack_stats, agent_names["X"], agent_names["O"], output_path=offense_plot_path)
        print("Grafici salvati.")
    except Exception as e:
         print(f"Errore durante il salvataggio dei grafici: {e}")


if __name__ == "__main__":
    # PPO Matches
    CONFIG_PPO = "config_5"
    PPO_PATH = get_model_path("ppo", CONFIG_PPO)
    ppo_kwargs = {"model_path": PPO_PATH, "deterministic": True}

    run_match(PPOAgent, RandomAgent, agent1_kwargs=ppo_kwargs, config=CONFIG_PPO)
    run_match(PPOAgent, RuleBasedL1_2Agent, agent1_kwargs=ppo_kwargs, config=CONFIG_PPO)
    run_match(PPOAgent, RuleBasedL2Agent, agent1_kwargs=ppo_kwargs, config=CONFIG_PPO)

    # DQN Matches
    # CONFIG_DQN = "config_5"
    # DQN_PATH = get_model_path("dqn", CONFIG_DQN)
    # dqn_kwargs = {"model_path": DQN_PATH, "deterministic": True}

    # run_match(DQNAgent, RandomAgent, agent1_kwargs=dqn_kwargs, config=CONFIG_DQN)
    # run_match(DQNAgent, RuleBasedL1_2Agent, agent1_kwargs=dqn_kwargs, config=CONFIG_DQN)
    # run_match(DQNAgent, RuleBasedL2Agent, agent1_kwargs=dqn_kwargs, config=CONFIG_DQN)

    # PPO vs DQN Matches
    # CONFIG_PPO = "config_2"
    # CONFIG_DQN = "config_3"
    # PPO_PATH = get_model_path("ppo", CONFIG_PPO)
    # DQN_PATH = get_model_path("dqn", CONFIG_DQN)
    # ppo_kwargs = {"model_path": PPO_PATH, "deterministic": True}
    # dqn_kwargs = {"model_path": DQN_PATH, "deterministic": True}
    # run_match(PPOAgent, DQNAgent, agent1_kwargs=ppo_kwargs, agent2_kwargs=dqn_kwargs, config=f"{CONFIG_PPO}_vs_{CONFIG_DQN}", rand=True)
    # run_match(DQNAgent, PPOAgent, agent1_kwargs=dqn_kwargs, agent2_kwargs=ppo_kwargs, config=f"{CONFIG_DQN}_vs_{CONFIG_PPO}",rand=True)
    
    print("\n--- Tutte le simulazioni completate ---")
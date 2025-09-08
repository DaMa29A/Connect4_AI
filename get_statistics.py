# import os
# from env.Connect4Env import Connect4Env
# from agents.DQNAgent import DQNAgent
# from agents.RuleBasedL2Agent import RuleBasedL2Agent
# from agents.HumanAgent import HumanAgent
# from utils.plots import (
#     plot_match_results,
#     plot_defense_summary,
#     plot_offense_summary,
#     show_all_plots
# )
# from utils.logger import (
#     write_header,
#     write_game_start,
#     write_turn_info,
#     write_defensive_opportunity,
#     write_defensive_success,
#     write_offensive_opportunity,
#     write_offensive_success,
#     write_board,
#     write_game_result,
#     write_final_stats,
#     write_start_turn_info
# )

# LOG_FILE = "./logs/game_log.txt"
# NUM_GAMES = 1
# RENDER_MODE = "console"  # "console" or "gui"


# def main():
#     # DEFINIZIONE AMBIENTE E AGENTI
#     env = Connect4Env(render_mode=RENDER_MODE, first_player=1)
#     agent1 = DQNAgent(env, deterministic=True)
#     #agent2 = RuleBasedL2Agent(env)
#     agent2 = HumanAgent(env)

#     # RESET LOG FILE
#     if os.path.exists(LOG_FILE):
#         os.remove(LOG_FILE)

#     # STATISTICHE
#     results = {"X": 0, "O": 0, "Draw": 0}
#     def_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
#     off_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}

#     # LOGGING E SIMULAZIONE PARTITE
#     with open(LOG_FILE, "w", encoding="utf-8") as f:
#         write_header(f, agent1.getName(), agent2.getName())

#         # Per ogni partita
#         for game_num in range(1, NUM_GAMES + 1):
#             write_game_start(f, game_num) # Scrive numero partita
#             env.reset()
#             done = False
#             step_count = 0
#             # Finché la partita non è finita (per ogni turno)
#             while not done:
#                 current_agent = agent1 if env.next_player_to_play == 1 else agent2
#                 player_id = env.next_player_to_play
#                 opponent_id = -player_id
#                 player_symbol = "X" if player_id == 1 else "O"
#                 agent_name = current_agent.getName()

#                 # === Prima raccogli le occasioni in liste temporanee ===
#                 def_opportunities = []
#                 off_opportunities = []

#                 # === Ora fai la mossa vera ===
#                 copy_env = env.clone() # Copia per simulazioni prima di effettuare mossa
#                 action = current_agent.choose_action()
#                 obs, reward, done, _, info = env.step(action)
#                 step_count += 1
#                 row = env.last_move_row
#                 col = env.last_move_col

#                 env.render()
#                 write_turn_info(f, step_count, agent_name, player_symbol, action, reward, obs)

#                 # Simula occasioni difensive
#                 for c in copy_env.get_valid_actions():
#                     r = copy_env.get_first_empty_row(c) # Trova la prima riga vuota in colonna c
#                     if r is None:
#                         continue
#                     # Simula la mossa dell'avversario
#                     sim_env = copy_env.clone()
#                     sim_env.board[r, c] = opponent_id
#                     sim_env.last_move_row = r
#                     sim_env.last_move_col = c
                    
#                     if sim_env.count_consecutive_pieces(r, c, 4, opponent_id):
#                         def_stats[player_symbol]["occasions"] += 1
#                         def_opportunities.append((r, c, copy_env.get_board()))
#                         write_defensive_opportunity(f, player_symbol, r, c, obs)

#                 # Simula occasioni offensive
#                 for c in env.get_valid_actions():
#                     r = env.get_first_empty_row(c)
#                     if r is None:
#                         continue
#                     sim_env = env.clone()
#                     sim_env.board[r, c] = player_id
#                     sim_env.last_move_row = r
#                     sim_env.last_move_col = c
#                     if sim_env.count_consecutive_pieces(r, c, 3, player_id) or \
#                        sim_env.count_consecutive_pieces(r, c, 4, player_id):
#                         if not sim_env.check_win_around_last_move(r, c):
#                             off_stats[player_symbol]["occasions"] += 1
#                             off_opportunities.append((r, c, env.get_board()))
#                             write_offensive_opportunity(f, player_symbol, r, c, obs)

#                 # Successo difensivo
#                 if row is not None and col is not None:
#                     if env.is_defensive_move(row, col, player_id):
#                         def_stats[player_symbol]["success"] += 1
#                         write_defensive_success(f, player_symbol, row, col, obs)

#                 # Successo offensivo
#                 if row is not None and col is not None:
#                     if env.check_win_around_last_move(row, col):
#                         off_stats[player_symbol]["success"] += 1
#                         write_offensive_success(f, player_symbol, row, col, obs)
#                     elif env.is_offensive_move(row, col, player_id):
#                         off_stats[player_symbol]["success"] += 1
#                         write_offensive_success(f, player_symbol, row, col, obs)

#                 write_board(f, obs)

#             # Fine partita
#             winner = env.get_winner()
#             write_game_result(f, winner)
#             if winner == 1:
#                 results["X"] += 1
#             elif winner == -1:
#                 results["O"] += 1
#             else:
#                 results["Draw"] += 1

#         write_final_stats(f, results, def_stats, agent1.getName(), agent2.getName())

#         # Aggiungi statistiche offensive cumulative
#         f.write("\n=== Statistiche Offensive Cumulative ===\n")
#         for symbol, name in [("X", agent1.getName()), ("O", agent2.getName())]:
#             occ = off_stats[symbol]["occasions"]
#             succ = off_stats[symbol]["success"]
#             miss = max(0, occ - succ)
#             perc = (succ / occ * 100) if occ > 0 else 0
#             f.write(
#                 f"{name} ({symbol}): Occasioni: {occ} | Convertite: {succ} | "
#                 f"Non sfruttate: {miss} | Percentuale: {perc:.2f}%\n"
#             )

#     print(f"Partite completate. Log salvato in {LOG_FILE}")
#     print(f"Defensive Stats: {def_stats}    Offensive Stats: {off_stats}")

#     plot_match_results(results, agent1.getName(), agent2.getName())
#     plot_defense_summary(def_stats, agent1.getName(), agent2.getName())
#     plot_offense_summary(off_stats, agent1.getName(), agent2.getName())
#     show_all_plots()


# if __name__ == "__main__":
#     main()




import os
from env.Connect4Env import Connect4Env
from agents.DQNAgent import DQNAgent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.HumanAgent import HumanAgent
from utils.plots import (
    plot_match_results,
    plot_defense_summary,
    plot_offense_summary,
    show_all_plots
)
from utils.logger import (
    write_header,
    write_game_start,
    write_turn_info,
    write_defensive_opportunity,
    write_defensive_success,
    write_offensive_opportunity,
    write_offensive_success,
    write_board,
    write_game_result,
    write_final_stats,
)

LOG_FILE = "./logs/game_log.txt"
NUM_GAMES = 1
RENDER_MODE = "console"  # "console" or "gui"

def main():
    # Definizione ambiente e agenti
    env = Connect4Env(render_mode=RENDER_MODE, first_player=1)
    agent1 = DQNAgent(env, deterministic=True)
    agent2 = HumanAgent(env)

    # Reset log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Statistiche
    results = {"X": 0, "O": 0, "Draw": 0}
    def_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
    off_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}

    # Posizioni già registrate
    def_positions = {"X": set(), "O": set()}
    off_positions = {"X": set(), "O": set()}

    # Logging e simulazione partite
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        write_header(f, agent1.getName(), agent2.getName())

        for game_num in range(1, NUM_GAMES + 1):
            write_game_start(f, game_num)
            env.reset()
            done = False
            step_count = 0

            while not done:
                current_agent = agent1 if env.next_player_to_play == 1 else agent2
                player_id = env.next_player_to_play
                opponent_id = -player_id
                player_symbol = "X" if player_id == 1 else "O"
                agent_name = current_agent.getName()

                copy_env = env.clone()
                action = current_agent.choose_action()
                obs, reward, done, _, _ = env.step(action)
                step_count += 1
                row, col = env.last_move_row, env.last_move_col

                env.render()
                write_turn_info(f, step_count, agent_name, player_symbol, action, reward, obs)

                # Simula difese
                for c in copy_env.get_valid_actions():
                    r = copy_env.get_first_empty_row(c)
                    if r is None:
                        continue
                    sim_env = copy_env.clone()
                    sim_env.board[r, c] = opponent_id
                    sim_env.last_move_row = r
                    sim_env.last_move_col = c
                    if sim_env.count_consecutive_pieces(r, c, 4, opponent_id) and (r, c) not in def_positions[player_symbol]:
                        def_stats[player_symbol]["occasions"] += 1
                        def_positions[player_symbol].add((r, c))
                        write_defensive_opportunity(f, player_symbol, r, c, obs)

                # Simula attacchi
                for c in env.get_valid_actions():
                    r = env.get_first_empty_row(c)
                    if r is None:
                        continue
                    sim_env = env.clone()
                    sim_env.board[r, c] = player_id
                    sim_env.last_move_row = r
                    sim_env.last_move_col = c
                    if ((sim_env.count_consecutive_pieces(r, c, 3, player_id) or
                         sim_env.count_consecutive_pieces(r, c, 4, player_id)) and
                        (r, c) not in off_positions[player_symbol]):
                        off_stats[player_symbol]["occasions"] += 1
                        off_positions[player_symbol].add((r, c))
                        write_offensive_opportunity(f, player_symbol, r, c, obs)

                # Successo difensivo
                if row is not None and col is not None and (row, col) in def_positions[player_symbol]:
                    def_stats[player_symbol]["success"] += 1
                    write_defensive_success(f, player_symbol, row, col, obs)

                # Successo offensivo
                if row is not None and col is not None and (row, col) in off_positions[player_symbol]:
                    off_stats[player_symbol]["success"] += 1
                    write_offensive_success(f, player_symbol, row, col, obs)

                write_board(f, obs)

            # Fine partita
            winner = env.get_winner()
            write_game_result(f, winner)
            if winner == 1:
                results["X"] += 1
            elif winner == -1:
                results["O"] += 1
            else:
                results["Draw"] += 1

        # Statistiche finali
        write_final_stats(f, results, def_stats, agent1.getName(), agent2.getName())

        f.write("\n=== Statistiche Offensive Cumulative ===\n")
        for symbol, name in [("X", agent1.getName()), ("O", agent2.getName())]:
            occ = off_stats[symbol]["occasions"]
            succ = off_stats[symbol]["success"]
            miss = occ - succ
            perc = (succ / occ * 100) if occ > 0 else 0
            f.write(
                f"{name} ({symbol}): Occasioni: {occ} | Convertite: {succ} | "
                f"Non sfruttate: {miss} | Percentuale: {perc:.2f}%\n"
            )

    print(f"Partite completate. Log salvato in {LOG_FILE}")
    print(f"Defensive Stats: {def_stats}    Offensive Stats: {off_stats}")

    plot_match_results(results, agent1.getName(), agent2.getName())
    plot_defense_summary(def_stats, agent1.getName(), agent2.getName())
    plot_offense_summary(off_stats, agent1.getName(), agent2.getName())
    show_all_plots()


if __name__ == "__main__":
    main()


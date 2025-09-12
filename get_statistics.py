import os
from env.Connect4Env import Connect4Env
from agents.DQNAgent import DQNAgent
from agents.HumanAgent import HumanAgent
from agents.RandomAgent import RandomAgent
from utils.check_rules import check_defensive_opportunities, check_attack_opportunities
from utils.logger import (
    write_header, write_game_start, write_board, write_turn_info,
    write_game_result, write_final_stats, write_opportunity, write_success
)
from utils.plots import (
    plot_match_results, plot_defense_summary, plot_offense_summary, show_all_plots
)

LOG_FILE = "./logs/game_log.txt"
NUM_GAMES = 200
RENDER_MODE = None  # "console", "gui", or None

def main():
    env = Connect4Env(render_mode=RENDER_MODE, first_player=1)
    agent1 = DQNAgent(env, deterministic=True)
    agent2 = RandomAgent(env)
    #agent2 = HumanAgent(env)

    agent_names = {"X": agent1.getName(), "O": agent2.getName()}
    results = {"X": 0, "O": 0, "Draw": 0}
    def_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
    attack_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        write_header(f, agent_names["X"], agent_names["O"])

        for game_num in range(1, NUM_GAMES + 1):
            write_game_start(f, game_num)
            env.reset()
            done = False
            step_count = 0

            active_def_ops = {"X": set(), "O": set()}
            active_atk_ops = {"X": set(), "O": set()}

            while not done:
                current_player = env.next_player_to_play
                agent = agent1 if current_player == 1 else agent2
                player_symbol = "X" if current_player == 1 else "O"
                agent_name = agent_names[player_symbol]

                action = agent.choose_action()
                row = env.get_first_empty_row(action)
                col = action

                obs, reward, done, _, _ = env.step(action)
                step_count += 1
                env.render()

                write_turn_info(f, step_count, agent_name, player_symbol, row, col, reward)
                write_board(f, env.board)

                # Se la partita è finita dopo la mossa, non rilevare nuove opportunità
                # if env.is_finish():
                #     break
                # Se la partita è finita dopo la mossa, verifica se è stato un attacco riuscito
                if env.is_finish():
                    # Controlla se la cella appena giocata era già stata identificata come opportunità di attacco in turni precedenti.
                    if (row, col) in active_atk_ops[player_symbol]:
                        attack_stats[player_symbol]["success"] += 1
                        active_atk_ops[player_symbol].remove((row, col))
                        write_success(f, "ATTACK", player_symbol, row, col)
                    else:
                        # Verifica manuale se la mossa ha creato una sequenza vincente
                        final_attacks = check_attack_opportunities(env.board, current_player)
                        if (row, col) in final_attacks:
                            attack_stats[player_symbol]["occasions"] += 1
                            attack_stats[player_symbol]["success"] += 1
                            write_opportunity(f, "Attack", player_symbol, row, col)
                            write_success(f, "ATTACK", player_symbol, row, col)
                    break

                # Opportunità di attacco per chi ha appena giocato
                new_atk_ops = check_attack_opportunities(env.board, current_player)
                for r, c in new_atk_ops:
                    if (r, c) not in active_atk_ops[player_symbol]:
                        active_atk_ops[player_symbol].add((r, c))
                        attack_stats[player_symbol]["occasions"] += 1
                        write_opportunity(f, "Attack", player_symbol, r, c)

                # Opportunità di difesa per l’avversario
                opponent_id = -current_player
                opponent_symbol = "X" if opponent_id == 1 else "O"
                new_def_ops = check_defensive_opportunities(env.board, opponent_id)
                for r, c in new_def_ops:
                    if (r, c) not in active_def_ops[opponent_symbol]:
                        active_def_ops[opponent_symbol].add((r, c))
                        def_stats[opponent_symbol]["occasions"] += 1
                        write_opportunity(f, "Defensive", opponent_symbol, r, c)

                # Verifica se la mossa ha sfruttato un'opportunità
                if (row, col) in active_def_ops[player_symbol]:
                    def_stats[player_symbol]["success"] += 1
                    active_def_ops[player_symbol].remove((row, col))
                    write_success(f, "DEFENSIVE", player_symbol, row, col)

                if (row, col) in active_atk_ops[player_symbol]:
                    attack_stats[player_symbol]["success"] += 1
                    active_atk_ops[player_symbol].remove((row, col))
                    write_success(f, "ATTACK", player_symbol, row, col)

            winner = env.get_winner()
            if winner == 1:
                results["X"] += 1
            elif winner == -1:
                results["O"] += 1
            else:
                results["Draw"] += 1

            write_game_result(f, winner)

        write_final_stats(f, results, def_stats, attack_stats, agent_names["X"], agent_names["O"])

    plot_match_results(results, agent_names["X"], agent_names["O"])
    plot_defense_summary(def_stats, agent_names["X"], agent_names["O"])
    plot_offense_summary(attack_stats, agent_names["X"], agent_names["O"])
    show_all_plots()

if __name__ == "__main__":
    main()

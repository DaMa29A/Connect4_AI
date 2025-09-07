import os
from env.Connect4Env import Connect4Env
from agents.DQNAgent import DQNAgent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
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
    write_final_stats
)

LOG_FILE = "./logs/game_log.txt"
NUM_GAMES = 1

def main():
    env = Connect4Env(render_mode=None, first_player=1)
    agent1 = DQNAgent(env, deterministic=True)
    agent2 = RuleBasedL2Agent(env)

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    results = {"X": 0, "O": 0, "Draw": 0}
    def_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}
    off_stats = {"X": {"occasions": 0, "success": 0}, "O": {"occasions": 0, "success": 0}}

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
                player_symbol = "X" if player_id == 1 else "O"
                agent_name = current_agent.getName()

                action = current_agent.choose_action()
                obs, reward, done, _, info = env.step(action)
                step_count += 1
                row = env.last_move_row
                col = env.last_move_col

                env.render()

                write_turn_info(f, step_count, agent_name, player_symbol, action, reward, obs)

                # ---------- Rilevamento Opportunità Difensive ----------
                for c in range(env.action_space.n):
                    r = env.get_first_empty_row(c)
                    if r is None:
                        continue
                    sim_env = env.clone()
                    sim_env.board[r, c] = -player_id  # mossa avversario
                    if sim_env.count_consecutive_pieces(r, c, 4, -player_id):
                        def_stats[player_symbol]["occasions"] += 1
                        write_defensive_opportunity(f, player_symbol, r, c, obs)

                # ---------- Rilevamento Opportunità Offensive ----------
                for c in range(env.action_space.n):
                    r = env.get_first_empty_row(c)
                    if r is None:
                        continue
                    sim_env = env.clone()
                    sim_env.board[r, c] = player_id
                    if sim_env.count_consecutive_pieces(r, c, 4, player_id) or \
                       sim_env.count_consecutive_pieces(r, c, 3, player_id):
                        off_stats[player_symbol]["occasions"] += 1
                        write_offensive_opportunity(f, player_symbol, r, c, obs)

                # ---------- Successo Difensivo ----------
                if row is not None and col is not None:
                    if env.is_defensive_move(row, col, player_id):
                        def_stats[player_symbol]["success"] += 1
                        write_defensive_success(f, player_symbol, row, col, obs)

                # ---------- Successo Offensive ----------
                if row is not None and col is not None:
                    if env.is_offensive_move(row, col, player_id):
                        off_stats[player_symbol]["success"] += 1
                        write_offensive_success(f, player_symbol, row, col, obs)

                write_board(f, obs)

            winner = env.get_winner()
            write_game_result(f, winner)
            if winner == 1:
                results["X"] += 1
            elif winner == -1:
                results["O"] += 1
            else:
                results["Draw"] += 1

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

    plot_match_results(results, agent1.getName(), agent2.getName())
    plot_defense_summary(def_stats, agent1.getName(), agent2.getName())
    plot_offense_summary(off_stats, agent1.getName(), agent2.getName())
    show_all_plots()

if __name__ == "__main__":
    main()

import os
from env.Connect4Env import Connect4Env
from agents.DQNAgent import DQNAgent
from agents.PPOAgent import PPOAgent
from agents.RandomAgent import RandomAgent
from utils.plots import plot_match_results, plot_defensive_stats, show_all_plots, plot_defense_summary

LOG_FILE = "./logs/game_log.txt"
NUM_GAMES = 2

def format_board(board):
    symbols = {1: "X", -1: "O", 0: " "}
    rows = []
    for r in range(board.shape[0]):
        row_str = " | ".join(symbols[int(c)] for c in board[r])
        rows.append(row_str)
    return "\n" + "\n".join(rows) + "\n" + "-" * (board.shape[1] * 4 - 1) + "\n"

def main():
    env = Connect4Env(render_mode=None, first_player=1)
    agent1 = DQNAgent(env, deterministic=False) # Player 1 (X)
    agent2 = PPOAgent(env, deterministic=False) # Player 2 (O)

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    results = {"X": 0, "O": 0, "Draw": 0}
    def_stats = {
        "X": {"occasions": 0, "success": 0},
        "O": {"occasions": 0, "success": 0}
    }

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== Connect4 Match Log ===\n")
        f.write(f"Player 1 (X): {agent1.getName()}\n")
        f.write(f"Player 2 (O): {agent2.getName()}\n\n")

        for game_num in range(1, NUM_GAMES + 1):
            f.write(f"\n=== Partita {game_num} ===\n")
            env.reset()
            done = False
            step_count = 0

            while not done:
                current_agent = agent1 if env.next_player_to_play == 1 else agent2
                player_id = env.next_player_to_play
                player_symbol = "X" if player_id == 1 else "O"
                agent_name = current_agent.getName()

                # Prima della mossa: controlla se l’avversario ha una triple da bloccare
                threat_present = env.has_opponent_threat(player_id)

                action = current_agent.choose_action()
                obs, reward, done, _, info = env.step(action)

                step_count += 1
                row = env.last_move_row
                col = env.last_move_col

                env.render()

                defensive_flag = False
                if row is not None and col is not None and threat_present:
                    def_stats[player_symbol]["occasions"] += 1
                    if env.is_defensive_move(row, col, player_id):
                        def_stats[player_symbol]["success"] += 1
                        defensive_flag = True
                    #else:
                        #print(f"{agent_name} ({player_symbol}) ha mancato una difesa!")

                f.write(f"\n--- Turno {step_count} ---\n")
                f.write(f"Giocatore: {agent_name} ({player_symbol})\n")
                f.write(f"Azione scelta (colonna): {action}\n")
                f.write(f"Reward ottenuto: {reward}\n")
                if defensive_flag:
                    f.write(f"** MOSSA DIFENSIVA: {player_symbol} ha bloccato una triple avversaria! **\n")
                f.write("Board:\n")
                f.write(format_board(obs))

            winner = env.get_winner()
            f.write("\n=== Risultato Finale ===\n")
            if winner == 1:
                f.write("Vittoria Player 1 (X)\n")
                results["X"] += 1
            elif winner == -1:
                f.write("Vittoria Player 2 (O)\n")
                results["O"] += 1
            else:
                f.write("Pareggio!\n")
                results["Draw"] += 1

        # Statistiche cumulative
        f.write("\n=== Statistiche Finali ===\n")
        f.write(f"Totale partite giocate: {NUM_GAMES}\n")
        f.write(f"Vittorie {agent1.getName()} (X): {results['X']}\n")
        f.write(f"Vittorie {agent2.getName()} (O): {results['O']}\n")
        f.write(f"Pareggi: {results['Draw']}\n\n")

        f.write("=== Statistiche Difensive Cumulative ===\n")
        for symbol, name in [("X", agent1.getName()), ("O", agent2.getName())]:
            occ = def_stats[symbol]["occasions"]
            succ = def_stats[symbol]["success"]
            miss = occ - succ
            perc = (succ / occ * 100) if occ > 0 else 0
            f.write(
                f"{name} ({symbol}): Occasioni: {occ} | Riuscite: {succ} | "
                f"Mancate: {miss} | Percentuale: {perc:.2f}%\n"
            )

    print(f"Partite completate. Log salvato in {LOG_FILE}")

    plot_match_results(results, agent1.getName(), agent2.getName())
    #plot_defensive_stats(def_stats, agent1.getName(), agent2.getName())
    plot_defense_summary(def_stats, agent1.getName(), agent2.getName())
    show_all_plots()

if __name__ == "__main__":
    main()

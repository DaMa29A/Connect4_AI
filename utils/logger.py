# utils/logger.py

def write_header(f, agent1_name, agent2_name):
    f.write("=== Connect4 Match Log ===\n")
    f.write(f"Player 1 (X): {agent1_name}\n")
    f.write(f"Player 2 (O): {agent2_name}\n\n")

def write_game_start(f, game_num):
    f.write(f"\n=== Partita {game_num} ===\n")

def write_turn_info(f, step_count, agent_name, player_symbol, action, reward):
    f.write(f"\n--- Turno {step_count} ---\n")
    f.write(f"Giocatore: {agent_name} ({player_symbol})\n")
    f.write(f"Azione scelta (colonna): {action}\n")
    f.write(f"Reward ottenuto: {reward}\n")

def write_defensive_success(f, player_symbol):
    f.write(f"** MOSSA DIFENSIVA: {player_symbol} ha bloccato una triple avversaria! **\n")

def write_board(f, board_str):
    f.write("Board:\n")
    f.write(board_str)

def write_game_result(f, winner):
    f.write("\n=== Risultato Finale ===\n")
    if winner == 1:
        f.write("Vittoria Player 1 (X)\n")
    elif winner == -1:
        f.write("Vittoria Player 2 (O)\n")
    else:
        f.write("Pareggio!\n")

def write_final_stats(f, results, def_stats, agent1_name, agent2_name):
    f.write("\n=== Statistiche Finali ===\n")
    total = results["X"] + results["O"] + results["Draw"]
    f.write(f"Totale partite giocate: {total}\n")
    f.write(f"Vittorie {agent1_name} (X): {results['X']}\n")
    f.write(f"Vittorie {agent2_name} (O): {results['O']}\n")
    f.write(f"Pareggi: {results['Draw']}\n\n")

    f.write("=== Statistiche Difensive Cumulative ===\n")
    for symbol, name in [("X", agent1_name), ("O", agent2_name)]:
        occ = def_stats[symbol]["occasions"]
        succ = def_stats[symbol]["success"]
        miss = occ - succ
        perc = (succ / occ * 100) if occ > 0 else 0
        f.write(
            f"{name} ({symbol}): Occasioni: {occ} | Riuscite: {succ} | "
            f"Mancate: {miss} | Percentuale: {perc:.2f}%\n"
        )

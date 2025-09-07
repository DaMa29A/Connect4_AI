def write_header(f, agent1_name, agent2_name):
    f.write("=== Connect4 Match Log ===\n")
    f.write(f"Player 1 (X): {agent1_name}\n")
    f.write(f"Player 2 (O): {agent2_name}\n\n")

def write_game_start(f, game_num):
    f.write(f"\n=== Partita {game_num} ===\n")

def format_board(board):
    symbols = {1: "X", -1: "O", 0: " "}
    rows = []
    for r in range(board.shape[0]):
        row_str = " | ".join(symbols[int(c)] for c in board[r])
        rows.append(row_str)
    return "\n" + "\n".join(rows) + "\n" + "-" * (board.shape[1] * 4 - 1) + "\n"

def write_turn_info(f, step_count, agent_name, player_symbol, action, reward):
    f.write(f"\n--- Turno {step_count} ---\n")
    f.write(f"Giocatore: {agent_name} ({player_symbol})\n")
    f.write(f"Azione scelta (colonna): {action}\n")
    f.write(f"Reward ottenuto: {reward}\n")

def write_defensive_opportunity(f, player_symbol, row, col):
    f.write(f"[DIFESA] Occasione rilevata per {player_symbol} — possibile minaccia da bloccare in posizione ({row}, {col}).\n")

def write_defensive_success(f, player_symbol, row, col):
    f.write(f"** MOSSA DIFENSIVA: {player_symbol} ha bloccato una triple avversaria in posizione ({row}, {col})! **\n")

def write_offensive_opportunity(f, player_symbol, row, col):
    f.write(f"[ATTACCO] Occasione offensiva rilevata per {player_symbol} — possibilità di creare 3 o 4 in fila in posizione ({row}, {col}).\n")

def write_offensive_success(f, player_symbol, row, col):
    f.write(f"[ATTACCO] Successo: {player_symbol} ha creato una tripletta sfruttabile o una quadrupla vincente in posizione ({row}, {col}).\n")

def write_board(f, board):
    f.write("Board:\n")
    f.write(format_board(board))

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

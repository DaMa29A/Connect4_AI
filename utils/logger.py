def write_board(f, board):
    ROWS, COLS = board.shape
    lines = []
    lines.append("Current board:")

    for r in range(ROWS):
        row_str = f"{r} | "
        for c in range(COLS):
            cell = board[r, c]
            if cell == 1:
                row_str += "X | "
            elif cell == -1:
                row_str += "O | "
            else:
                row_str += "  | "
        lines.append(row_str.rstrip())

    lines.append("‾" * (COLS * 4 + 3))
    col_labels = "    " + "   ".join(str(c) for c in range(COLS))
    lines.append(col_labels)

    board_str = "\n".join(lines) + "\n"
    f.write(board_str)


def write_header(f, agent1_name, agent2_name):
    f.write("=== Connect4 Match Log ===\n")
    f.write(f"Player 1 (X): {agent1_name}\n")
    f.write(f"Player 2 (O): {agent2_name}\n\n")


def write_game_start(f, game_num):
    f.write(f"\n=== Partita {game_num} ===\n")


def write_game_result(f, winner):
    f.write("\n=== Risultato Finale ===\n")
    if winner == 1:
        f.write("Vittoria Player 1 (X)\n")
    elif winner == -1:
        f.write("Vittoria Player 2 (O)\n")
    else:
        f.write("Pareggio!\n")


def write_turn_info(f, step_count, agent_name, player_symbol, row, col, reward):
    f.write(f"\n--- Turno {step_count} ---\n")
    f.write(f"Giocatore: {agent_name} ({player_symbol})\n")
    f.write(f"Azione scelta: r{row},c{col}\n")
    f.write(f"Reward ottenuto: {reward}\n")


def write_final_stats(f, results, def_stats, attack_stats, agent1_name, agent2_name):
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
        f.write(f"{name} ({symbol}): Occasioni: {occ} | Riuscite: {succ} | Mancate: {miss} | Percentuale: {perc:.2f}%\n")

    f.write("\n=== Statistiche Offensive Cumulative ===\n")
    for symbol, name in [("X", agent1_name), ("O", agent2_name)]:
        occ = attack_stats[symbol]["occasions"]
        succ = attack_stats[symbol]["success"]
        miss = occ - succ
        perc = (succ / occ * 100) if occ > 0 else 0
        f.write(f"{name} ({symbol}): Occasioni: {occ} | Completate: {succ} | Fallite: {miss} | Percentuale: {perc:.2f}%\n")

def write_opportunity(f, kind, player_symbol, row, col):
    f.write(f"[{kind}] opportunity for {player_symbol} at r{row},c{col}\n")

def write_success(f, kind, player_symbol, row, col):
    f.write(f"[{kind}] SUCCESS by {player_symbol} at r{row},c{col}\n")


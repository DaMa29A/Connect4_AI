from configs.env_config import ROWS_COUNT, COLUMNS_COUNT

def is_playable(board, r, c):
    """Controlla se una cella (r, c) è una mossa valida"""
    if board[r, c] != 0:
        return False
    if r == ROWS_COUNT - 1:
        return True
    if board[r + 1, c] != 0:
        return True
    return False

# ---------------------------------------------------------------------------
# CONTROLLO SEQUENZE
# ---------------------------------------------------------------------------

def is_sequence(board, r, c, current_player, target_count):
    """
    Controlla se la mossa (r, c) appena fatta fa parte di una sequenza
    di 'target_count' pedine, sviluppabile in una fila di 4.
    """
    if board[r, c] != current_player:
        return False

    directions = [
        (0, 1),   # Orizzontale
        (1, 0),   # Verticale
        (1, 1),   # Diagonale ↘
        (1, -1)   # Diagonale ↙
    ]

    for dr, dc in directions:
        # Controlla tutte le "finestre" di 4 celle che includono la mossa (r, c)
        for offset in range(-3, 1):
            cells = []
            for i in range(4):
                rr = r + (offset + i) * dr
                cc = c + (offset + i) * dc
                if 0 <= rr < ROWS_COUNT and 0 <= cc < COLUMNS_COUNT:
                    cells.append((rr, cc))
                else:
                    break
            
            # Se la finestra non è di 4 celle, salta
            if len(cells) != 4:
                continue

            # Analizza il contenuto della finestra
            player_count = 0
            gap_count = 0
            gap_cell = None
            for rr, cc in cells:
                if board[rr, cc] == current_player:
                    player_count += 1
                elif board[rr, cc] == 0:
                    gap_count += 1
                    gap_cell = (rr, cc) # Salva la posizione dell'ultimo gap
                else:
                    # Trovata pedina avversaria, questa finestra è bloccata
                    gap_count = 99 
                    break

            # Valutazione
            if target_count < 4:
                # Cerca minacce (es. 3 pedine e 1 gap giocabile)
                if player_count == target_count and gap_count == 4 - target_count:
                    if gap_cell is not None and is_playable(board, *gap_cell):
                        return True, gap_cell
            else:
                # Cerca vittoria (target_count == 4)
                if player_count == 4:
                    return True, None
                    
    return False, None


# --- Funzioni offensive ---

def is_a_pair(board, r, c, current_player):
    return is_sequence(board, r, c, current_player, target_count=2)

def is_a_triplet(board, r, c, current_player):
    return is_sequence(board, r, c, current_player, target_count=3)

def is_a_quadruplet(board, r, c, current_player):
    return is_sequence(board, r, c, current_player, target_count=4)

# --- Funzioni difensive ---

def is_block_sequence(board, r, c, current_player, target_count=4):
    """
    Funzione base per il blocco: simula la mossa (r,c) come se fosse
    dell'avversario e controlla se LUI avrebbe creato una sequenza.
    """
    opponent = -current_player
    if board[r, c] != current_player:
        return False, None

    simulated_board = board.copy()
    simulated_board[r, c] = opponent  # Simula mossa avversario

    # Controlla se l'avversario ha creato una sequenza
    return is_sequence(simulated_board, r, c, opponent, target_count=target_count)

def is_block_triplet(board, r, c, current_player):
    """
    Controlla se la mossa (r,c) blocca una VITTORIA (4-in-fila) dell'avversario.
    """
    return is_block_sequence(board, r, c, current_player, target_count=4)

def is_block_pair(board, r, c, current_player):
    """
    Controlla se la mossa (r,c) blocca una MINACCIA (3-in-fila) dell'avversario.
    """
    return is_block_sequence(board, r, c, current_player, target_count=3)


# ---------------------------------------------------------------------------
# SCANSIONE DELLA BOARD PER TROVARE SEQUENZE
# ---------------------------------------------------------------------------

def find_sequences(board, current_player, target_count=3):
    """
    Scansiona l'intera board e trova TUTTE le mosse giocabili (r, c)
    che creerebbero una sequenza di 'target_count' per 'current_player'.
    """
    sequences = set()
    for c in range(COLUMNS_COUNT):
        # Trova la prima riga giocabile in quella colonna
        for r in range(ROWS_COUNT - 1, -1, -1):
            if is_playable(board, r, c):
                # Simula la mossa
                temp_board = board.copy()
                temp_board[r, c] = current_player
                
                # Controlla se questa mossa crea la sequenza desiderata
                found, _ = is_sequence(temp_board, r, c, current_player, target_count)
                if found:
                    sequences.add((r, c, current_player))
                
                # Trovata la prima cella giocabile, passa alla colonna successiva
                break  
                
    return sequences

def check_attack_opportunities(board, player_id, target_count=4):
    """
    Trova tutte le mosse d'attacco con un 'target_count' specifico.
    """
    return find_sequences(board, player_id, target_count)

def check_defensive_opportunities(board, player_id, target_count=4):
    """
    Trova tutte le mosse che l'avversario (-player_id) potrebbe fare per creare una sequenza.
    """
    return find_sequences(board, -player_id, target_count)
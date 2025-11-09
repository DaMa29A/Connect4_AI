import pygame
import sys
import time
from colorama import Fore, Style, init
from env.Connect4Env import Connect4Env
from agents.Agent import Agent 
from agents.HumanAgent import HumanAgent
from agents.RandomAgent import RandomAgent
from agents.PPOAgent import PPOAgent
from agents.DQNAgent import DQNAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent 
from agents.RuleBasedL2Agent import RuleBasedL2Agent


# --- CONFIGURAZIONE PRINCIPALE ---
# Modifica questa riga per cambiare modalità: "console" o "gui"
RENDER_MODE = "gui"
# -----------------------------------

def run_console_game(env, players):
    """Esegue il game loop per la modalità console."""
    try:
        obs, info = env.reset(seed=42)
        terminated, truncated = False, False
        
        while not (terminated or truncated):
            current_player_key = env.next_player_to_play
            current_agent = players[current_player_key]
            action_mask = info["action_mask"]
            action = current_agent.choose_action(obs, action_mask)
            obs, reward, terminated, truncated, info = env.step(action)

    except KeyboardInterrupt:
        print("\nPartita interrotta.")
        return None 
    return env.get_winner()

def run_gui_game(env, players):
    """Esegue il game loop per la GUI Pygame."""
    obs, info = env.reset(seed=42)
    game_over = False
    clock = pygame.time.Clock()
    current_hover_col = -1 

    while not game_over:
        
        current_player_key = env.next_player_to_play
        current_agent = players[current_player_key]
        action_mask = info["action_mask"] 

        # --- GESTIONE AGENTE NON UMANO (Bot o IA) ---
        if not isinstance(current_agent, HumanAgent):
            action = current_agent.choose_action(obs, action_mask)
            obs, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                game_over = True
            time.sleep(0.5)
            continue 

        # --- GESTIONE EVENTI UMANI ---
        clicked_action = None 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                continue
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                current_hover_col = env.gui_renderer.get_col_from_mouse(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if isinstance(current_agent, HumanAgent):
                    if 0 <= current_hover_col < 7 and action_mask[current_hover_col]:
                         clicked_action = current_hover_col

        if clicked_action is not None:
            obs, reward, terminated, truncated, info = env.step(clicked_action)
            if terminated or truncated:
                game_over = True

        if not game_over:
            env.gui_renderer.draw_board(obs) 
            is_valid = (0 <= current_hover_col < 7 and action_mask[current_hover_col])
            env.gui_renderer.draw_hover_highlight(current_hover_col, is_valid)

        clock.tick(60) 

    return env.get_winner()

def announce_winner(winner, players):
    """Stampa il messaggio di fine partita sulla console."""
    if winner == 1:
        print(f"🎉 {Fore.GREEN}GIOCO FINITO! Ha vinto {players[1].getName()}!")
    elif winner == -1:
        print(f"🎉 {Fore.GREEN}GIOCO FINITO! Ha vinto {players[-1].getName()}!")
    elif winner == 0:
        print(f"{Fore.YELLOW}GIOCO FINITO! È un pareggio!")

def main():
    init(autoreset=True)
    
    # In modalità gioco, impostiamo 'self_play=True'
    # per forzare l'ambiente in modalità turn-based.
    env = Connect4Env(render_mode=RENDER_MODE, self_play=True)
    
    # --- Configura Giocatori ---
    
    # Giocatore 1 (X)
    agent1 = HumanAgent(
        name="Giocatore 1 (X)", 
        render_mode=RENDER_MODE, 
        player_symbol=1 # <-- MODIFICA AGGIUNTA
    )
    
    # Giocatore 2 (O)
    agent2 = RandomAgent(
        name="Giocatore 2 (O)", 
        player_symbol=-1 # <-- MODIFICA AGGIUNTA
    )
    
    # --- Esempi di altri avversari (decommenta per usarli) ---
    # agent2 = HumanAgent(
    #     name="Giocatore 2 (O)", 
    #     render_mode=RENDER_MODE, 
    #     player_symbol=-1
    # )
    # agent2 = RuleBasedL2Agent(
    #     name="Rule-Based L2", 
    #     player_symbol=-1
    # )
    # agent2 = PPOAgent(
    #     model_path="models/connect4_ppo.zip", 
    #     name="PPO Bot", 
    #     player_symbol=-1
    # )
    
    # Mappa i simboli (1 e -1) agli oggetti Agente
    players = {1: agent1, -1: agent2} 

    print(f"{Fore.GREEN}Benvenuti in Connect4! ({RENDER_MODE} mode)")
    print(f"{players[1].getName()} (Rosso) vs {players[-1].getName()} (Giallo)")

    winner = None
    try:
        if RENDER_MODE == "console":
            winner = run_console_game(env, players)
        elif RENDER_MODE == "gui":
            winner = run_gui_game(env, players)
        else:
            print(f"Errore: RENDER_MODE '{RENDER_MODE}' non supportato.")
            return

    except KeyboardInterrupt:
        print("\nPartita interrotta.")
    except Exception as e:
        print(f"\n{Fore.RED}Si è verificato un errore inaspettato: {e}")
        # Alza l'eccezione per il debug
        raise 
    finally:
        if winner is not None:
            announce_winner(winner, players)
            if RENDER_MODE == "gui":
                env.gui_renderer.draw_winner_text(winner, players)
                print("La finestra si chiuderà tra 3 secondi...")
                time.sleep(3)
        
        env.close()
        if RENDER_MODE == "gui":
            sys.exit()

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
import numpy as np

def plot_win_rates_and_trends(results, agent1_name, agent2_name):
    outcomes = results["game_outcomes"]
    games = np.arange(1, len(outcomes) + 1)

    cumulative_agent1 = np.cumsum([1 if o == 1 else 0 for o in outcomes])
    cumulative_agent2 = np.cumsum([1 if o == -1 else 0 for o in outcomes])
    cumulative_draws = np.cumsum([1 if o == 0 else 0 for o in outcomes])

    win_labels = [f"{agent1_name} (Red)", f"{agent2_name} (Yellow)", "Draws"]
    win_values = [results["agent1_wins"], results["agent2_wins"], results["draws"]]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Grafico 1: Tasso di vittoria
    bars = axs[0].bar(win_labels, win_values, color=["red", "gold", "gray"])
    axs[0].set_title("Tasso di vittoria")
    axs[0].set_ylabel("Numero di vittorie")
    axs[0].grid(axis="y", linestyle="--", alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        axs[0].text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(height),
                    ha='center', va='bottom', fontsize=10)

    # Grafico 2: Andamento delle partite
    axs[1].plot(games, cumulative_agent1, label=f"{agent1_name} wins", color="red")
    axs[1].plot(games, cumulative_agent2, label=f"{agent2_name} wins", color="gold")
    axs[1].plot(games, cumulative_draws, label="Draws", color="gray")
    axs[1].set_title("Andamento delle partite")
    axs[1].set_xlabel("Numero partita")
    axs[1].set_ylabel("Vittorie cumulative")
    axs[1].legend()
    axs[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def plot_defensive_moves(stats, agent1_name, agent2_name):
    """Grafico barre + line plot cumulativo mosse difensive"""
    total_moves_agent1 = stats["agent1_defensive_moves"]
    total_moves_agent2 = stats["agent2_defensive_moves"]

    # --- Barra cumulativa ---
    labels = [f"{agent1_name}", f"{agent2_name}"]
    values = [total_moves_agent1, total_moves_agent2]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    bars = axs[0].bar(labels, values, color=["red", "gold"])
    axs[0].set_title("Mosse difensive cumulative")
    axs[0].set_ylabel("Numero mosse difensive")
    axs[0].grid(axis="y", linestyle="--", alpha=0.7)
    
    for bar in bars:
        height = bar.get_height()
        axs[0].text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(int(height)),
                    ha='center', va='bottom', fontsize=10)

    # --- Line plot cumulativo per partita ---
    outcomes = stats["game_outcomes"]
    defensive_moves_agent1 = stats.get("agent1_def_moves_per_game", [0]*len(outcomes))
    defensive_moves_agent2 = stats.get("agent2_def_moves_per_game", [0]*len(outcomes))

    cumulative_agent1 = np.cumsum(defensive_moves_agent1)
    cumulative_agent2 = np.cumsum(defensive_moves_agent2)
    games = np.arange(1, len(outcomes) + 1)

    axs[1].plot(games, cumulative_agent1, label=f"{agent1_name}", color="red")
    axs[1].plot(games, cumulative_agent2, label=f"{agent2_name}", color="gold")
    axs[1].set_title("Evoluzione mosse difensive (cumulativo)")
    axs[1].set_xlabel("Numero partita")
    axs[1].set_ylabel("Mosse difensive cumulative")
    axs[1].legend()
    axs[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()




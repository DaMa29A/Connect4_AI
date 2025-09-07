import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_match_results(results, agent1_name, agent2_name):
    """
    Visualizza un grafico a barre con le vittorie e i pareggi,
    affiancato da un grafico a torta con le percentuali.
    """
    agent_names = [agent1_name, agent2_name, "Pareggi"]
    win_counts = [results["X"], results["O"], results["Draw"]]
    colors = ["#ff4d4d", "#ffd966", "#cccccc"]

    total = sum(win_counts)
    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])

    # Grafico a barre
    ax_bar = fig.add_subplot(gs[0])
    bars = ax_bar.bar(agent_names, win_counts, color=colors)
    ax_bar.set_title("Risultati Partite")
    ax_bar.bar_label(bars, labels=[str(v) for v in win_counts], padding=3)

    # Grafico a torta
    ax_pie = fig.add_subplot(gs[1])
    if total == 0:
        ax_pie.pie([1], labels=["Nessun dato"], colors=["#d3d3d3"])
    else:
        ax_pie.pie(
            win_counts,
            labels=agent_names,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90
        )
    ax_pie.set_title("Distribuzione % Vittorie/Pareggi")

    plt.tight_layout()
    return fig


def plot_defensive_stats(def_stats, agent1_name, agent2_name):
    """
    Visualizza un grafico a barre con le difese riuscite e mancate.
    """
    labels = [agent1_name, agent2_name]
    success = [def_stats["X"]["success"], def_stats["O"]["success"]]
    fail = [
        def_stats["X"]["occasions"] - def_stats["X"]["success"],
        def_stats["O"]["occasions"] - def_stats["O"]["success"]
    ]
    x = range(len(labels))
    bar_width = 0.4

    fig, ax = plt.subplots(figsize=(6, 5))
    bars_success = ax.bar([i - bar_width/2 for i in x], success, width=bar_width, label="Riuscite", color="#90ee90")
    bars_fail = ax.bar([i + bar_width/2 for i in x], fail, width=bar_width, label="Mancate", color="#ff9999")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Difese Totali")
    ax.legend()
    ax.bar_label(bars_success, labels=[str(v) for v in success], padding=3)
    ax.bar_label(bars_fail, labels=[str(v) for v in fail], padding=3)
    return fig, ax


def plot_defense_summary(def_stats, agent1_name, agent2_name):
    labels = [agent1_name, agent2_name]
    success = [def_stats["X"]["success"], def_stats["O"]["success"]]
    fail = [
        def_stats["X"]["occasions"] - def_stats["X"]["success"],
        def_stats["O"]["occasions"] - def_stats["O"]["success"]
    ]
    bar_width = 0.4
    x = range(len(labels))

    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(2, 3, width_ratios=[2, 0.1, 1])

    # Grafico a barre
    ax_bar = fig.add_subplot(gs[:, 0])
    bars_success = ax_bar.bar([i - bar_width/2 for i in x], success, width=bar_width, label="Riuscite", color="#90ee90")
    bars_fail = ax_bar.bar([i + bar_width/2 for i in x], fail, width=bar_width, label="Mancate", color="#ff9999")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.set_title("Difese Totali")
    ax_bar.legend()
    ax_bar.bar_label(bars_success, labels=[str(v) for v in success], padding=3)
    ax_bar.bar_label(bars_fail, labels=[str(v) for v in fail], padding=3)

    # Grafico a torta per agent1 (in alto a destra)
    ax_pie1 = fig.add_axes([0.72, 0.55, 0.22, 0.35])
    total1 = success[0] + fail[0]
    if total1 == 0:
        ax_pie1.pie([1], labels=["Nessuna occasione"], colors=["#d3d3d3"])
    else:
        ax_pie1.pie(
            [success[0], fail[0]],
            labels=["Riuscite", "Mancate"],
            autopct="%1.1f%%",
            colors=["#90ee90", "#ff9999"],
            startangle=90
        )
    ax_pie1.set_title(f"{agent1_name} - % Difese")

    # Riquadro attorno a pie1
    box1 = patches.FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0.02",
        edgecolor="gray",
        facecolor="none",
        linewidth=1.5,
        transform=ax_pie1.transAxes
    )
    ax_pie1.add_patch(box1)

    # Grafico a torta per agent2 (in basso a destra)
    ax_pie2 = fig.add_axes([0.72, 0.1, 0.22, 0.35])
    total2 = success[1] + fail[1]
    if total2 == 0:
        ax_pie2.pie([1], labels=["Nessuna occasione"], colors=["#d3d3d3"])
    else:
        ax_pie2.pie(
            [success[1], fail[1]],
            labels=["Riuscite", "Mancate"],
            autopct="%1.1f%%",
            colors=["#90ee90", "#ff9999"],
            startangle=90
        )
    ax_pie2.set_title(f"{agent2_name} - % Difese")

    # Riquadro attorno a pie2
    box2 = patches.FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0.02",
        edgecolor="gray",
        facecolor="none",
        linewidth=1.5,
        transform=ax_pie2.transAxes
    )
    ax_pie2.add_patch(box2)

    plt.tight_layout()
    return fig


def plot_offense_summary(off_stats, agent1_name, agent2_name):
    """
    Visualizza grafico con occasioni offensive create e convertite.
    """
    labels = [agent1_name, agent2_name]
    success = [off_stats["X"]["success"], off_stats["O"]["success"]]
    fail = [
        off_stats["X"]["occasions"] - off_stats["X"]["success"],
        off_stats["O"]["occasions"] - off_stats["O"]["success"]
    ]
    bar_width = 0.4
    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(6, 5))
    bars_success = ax.bar([i - bar_width/2 for i in x], success, width=bar_width,
                          label="Occasioni convertite", color="#6495ED")
    bars_fail = ax.bar([i + bar_width/2 for i in x], fail, width=bar_width,
                       label="Occasioni non sfruttate", color="#FFB6C1")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Statistiche Offensive")
    ax.legend()
    ax.bar_label(bars_success, labels=[str(v) for v in success], padding=3)
    ax.bar_label(bars_fail, labels=[str(v) for v in fail], padding=3)

    plt.tight_layout()
    return fig, ax

def show_all_plots():
    """
    Mostra tutti i grafici generati.
    """
    plt.tight_layout()
    plt.show()
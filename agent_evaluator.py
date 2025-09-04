from env.Connect4Env import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.DQNAgent import DQNAgent
from agents.PPOAgent import PPOAgent
from utils.plot_utils import plot_win_rates_and_trends

def run_match(agent1_class, agent2_class, num_games=100):
    stats = {
        "agent1_wins": 0,
        "agent2_wins": 0,
        "draws": 0,
        "game_outcomes": [],  # 1 = agent1 win, -1 = agent2 win, 0 = draw
    }

    for game_index in range(num_games):
        env = Connect4Env(render_mode=None, first_player=1)
        agent1 = agent1_class(env)
        agent2 = agent2_class(env)

        done = False
        while not done:
            current_agent = agent1 if env.next_player_to_play == 1 else agent2
            action = current_agent.choose_action()
            _, _, done, _, _ = env.step(action)

        winner = env.get_winner()
        stats["game_outcomes"].append(winner)

        if winner == 1:
            stats["agent1_wins"] += 1
        elif winner == -1:
            stats["agent2_wins"] += 1
        else:
            stats["draws"] += 1

    return stats, agent1.getName(), agent2.getName()

def main():
    # Sostituisci agenti da testare
    agent1_class = DQNAgent
    #agent2_class = RuleBasedL2Agent
    agent2_class = RandomAgent

    num_games = 200
    stats, agent1_name, agent2_name = run_match(agent1_class, agent2_class, num_games)

    print(f"\nRisultati su {num_games} partite:")
    print(f"{agent1_name} (Red) vittorie: {stats['agent1_wins']}")
    print(f"{agent2_name} (Yellow) vittorie: {stats['agent2_wins']}")
    print(f"Pareggi: {stats['draws']}")

    # Visualizza i grafici
    plot_win_rates_and_trends(stats, agent1_name, agent2_name)

if __name__ == "__main__":
    main()

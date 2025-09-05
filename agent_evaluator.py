from env.Connect4Env2 import Connect4Env
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.DQNAgent2 import DQNAgent
from agents.PPOAgent2 import PPOAgent
from utils.plot_utils import plot_win_rates_and_trends, plot_defensive_moves

def run_match(agent1_class, agent2_class, num_games=100):
    stats = {
        "agent1_wins": 0,
        "agent2_wins": 0,
        "draws": 0,
        "game_outcomes": [],  # 1 = agent1 win, -1 = agent2 win, 0 = draw
        "agent1_defensive_moves": 0,
        "agent2_defensive_moves": 0,
        "agent1_def_moves_per_game": [],
        "agent2_def_moves_per_game": [],
    }

    for game_index in range(num_games):
        env = Connect4Env(render_mode=None, first_player=1)
        agent1 = agent1_class(env)
        agent2 = agent2_class(env)

        done = False
        agent1_defensive_this_game = 0
        agent2_defensive_this_game = 0

        while not done:
            current_agent = agent1 if env.next_player_to_play == 1 else agent2
            action = current_agent.choose_action()
            obs, reward, done, _, _ = env.step(action)

            # Verifica se mossa difensiva
            last_row = env.last_move_row
            last_col = env.last_move_col
            if last_row is not None and last_col is not None:
                if current_agent == agent1 and env.is_defensive_move(last_row, last_col, 1):
                    agent1_defensive_this_game += 1
                elif current_agent == agent2 and env.is_defensive_move(last_row, last_col, -1):
                    agent2_defensive_this_game += 1

        winner = env.get_winner()
        stats["game_outcomes"].append(winner)

        if winner == 1:
            stats["agent1_wins"] += 1
        elif winner == -1:
            stats["agent2_wins"] += 1
        else:
            stats["draws"] += 1

        # Aggiorna mosse difensive totali e per partita
        stats["agent1_defensive_moves"] += agent1_defensive_this_game
        stats["agent2_defensive_moves"] += agent2_defensive_this_game
        stats["agent1_def_moves_per_game"].append(agent1_defensive_this_game)
        stats["agent2_def_moves_per_game"].append(agent2_defensive_this_game)

    return stats, agent1.getName(), agent2.getName()


def main():
    agent1_class = DQNAgent
    #agent2_class = RandomAgent
    #agent2_class = RuleBasedL1Agent
    agent2_class = RuleBasedL2Agent
    num_games = 200

    stats, agent1_name, agent2_name = run_match(agent1_class, agent2_class, num_games)

    print(f"\nRisultati su {num_games} partite:")
    print(f"{agent1_name} (Red) vittorie: {stats['agent1_wins']}")
    print(f"{agent2_name} (Yellow) vittorie: {stats['agent2_wins']}")
    print(f"Pareggi: {stats['draws']}")
    print(f"{agent1_name} mosse difensive: {stats['agent1_defensive_moves']}")
    print(f"{agent2_name} mosse difensive: {stats['agent2_defensive_moves']}")

    # Visualizza grafici
    plot_win_rates_and_trends(stats, agent1_name, agent2_name)
    plot_defensive_moves(stats, agent1_name, agent2_name)


if __name__ == "__main__":
    main()

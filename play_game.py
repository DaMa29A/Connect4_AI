from env.Connect4Env2 import Connect4Env
from agents.HumanAgent import HumanAgent
from agents.RandomAgent import RandomAgent
from agents.RuleBasedL1Agent import RuleBasedL1Agent
from agents.RuleBasedL2Agent import RuleBasedL2Agent
from agents.DQNAgent2 import DQNAgent
from agents.PPOAgent2 import PPOAgent
from gui.gui_rend import start_gui, show_results
from env.env_config import RENDER_MODE


def main():
    env = Connect4Env(render_mode=RENDER_MODE) # render_mode can be "console" or "gui"

    agent1 = HumanAgent(env)            # Player 1 (X)
    agent2 = DQNAgent(env)           # Player 2 (O)

    print("Welcome to Connect4!")
    print(f"Player 1 (X): {agent1.getName()}")
    print(f"Player 2 (O): {agent2.getName()}")
    
    #env.render()
    screen = None
    if env.render_mode == "console":
        env.render()
    elif env.render_mode == "gui":
        screen = start_gui()
        env.render(screen)
        
    done = False

    while not done:
        current_agent = agent1 if env.next_player_to_play == 1 else agent2
        action = current_agent.choose_action()
        obs, reward, done, _, _ = env.step(action)
        
        #env.render()
        if env.render_mode == "console":
            env.render()
        elif env.render_mode == "gui":
            env.render(screen)

        if done:
            winner = env.get_winner()
            if env.render_mode == "console":
                if winner == 1:
                    print("Player 1 wins!")
                elif winner == -1:
                    print("Player 2 wins!")
                else:
                    print("It's a draw!")
                break
            elif env.render_mode == "gui":
                show_results(screen, winner)
                
                
if __name__ == "__main__":
    main()

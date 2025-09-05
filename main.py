import numpy as np
from env.env_config import ROWS_COUNT, COLUMNS_COUNT
from env.Connect4Env2 import Connect4Env




def main():
    env = Connect4Env(render_mode="console")
    
    env.render()
    
    env.step(0) #X
    env.render()
    
    env.step(0)  #O
    env.render()    
    
    env.step(1)  #X
    env.render()
    
    a = env.check_three_effect(env.last_move_row, env.last_move_col, 1)
    print("check_three_effect(5, 2, 1):", a)  
    
    env.step(5)  #O
    env.render()
    
    env.step(2)  #X
    env.render()
    
    a = env.check_three_effect(env.last_move_row, env.last_move_col, 1)
    print("check_three_effect(5, 2, 1):", a)  


if __name__ == "__main__":
    main()

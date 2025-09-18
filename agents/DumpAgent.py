import numpy as np
from .Agent import Agent

class DumpAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.name = "Random"

    def choose_action(self):
        return 6
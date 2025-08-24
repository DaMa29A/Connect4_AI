class Agent:
    def __init__(self, env=None):
        self.name = None
        self.env = env
        
    def choose_action(self):
        raise NotImplementedError("This method must be implemented in the child class")
    
    def getName(self):
        return self.name

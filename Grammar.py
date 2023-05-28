class Grammar: 
    def __init__(self, state):
        self.state = state
    
    def __repr__(self):
        return str(self.state)
    
    def __iter__(self):
        return iter(self.state)

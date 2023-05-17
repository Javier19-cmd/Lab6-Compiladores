class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = set([prod[0] for prod in self.productions])
    
    def get_non_terminals(self):
        non_terminals = set()
        for prod in self.productions:
            non_terminals.add(prod[0])
            for symbol in prod[1]:
                if symbol.isupper():
                    non_terminals.add(symbol)
        return non_terminals
    
    def __str__(self):
        return '\n'.join([str(prod) for prod in self.productions])
    
    def __iter__(self):
        return iter(self.productions)
    
    def __len__(self):
        return len(self.productions)
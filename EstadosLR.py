class Corazon:
    
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
    
    def __str__(self):
        return f"{self.izquierda} -> {self.derecha}"
    
    def __getitem__(self, index):
        if index == 0:
            return self.izquierda
        elif index == 1:
            return self.derecha
        else:
            raise IndexError("Index out of range")
        
    def __eq__(self, other):
        if isinstance(other, Corazon):
            return self.izquierda == other.izquierda and self.derecha == other.derecha
        return False
    
    def __hash__(self):
        return hash((self.izquierda, self.derecha))
        

class Resto:

    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha

    def __str__(self):
        return f"{self.izquierda} -> {self.derecha}"
    
    def __getitem__(self, index):
        if index == 0:
            return self.izquierda
        elif index == 1:
            return self.derecha
        else:
            raise IndexError("Index out of range")
        
    def __eq__(self, other):
        if isinstance(other, Resto):
            return self.izquierda == other.izquierda and self.derecha == other.derecha
        return False
    
    def __hash__(self):
        return hash((self.izquierda, self.derecha))

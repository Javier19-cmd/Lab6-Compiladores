import re

# Clase para detectar errores.
def deteccion2(regex):

    # Verificando que tenga [] balanceados.
    if regex.count('[') != regex.count(']'):
        print("Error: La expresión regular no tiene corchetes consistentes.")
        return "Corchetes", regex
    
    # Verificando que la expresión tenga paréntesis de apertura y cierre.
    if regex.count('(') != regex.count(')'):
        print("Error: La expresión regular no tiene paréntesis consistentes.")
        return "Parent", regex
    
    # Verificando que la expresión tenga letras o números.
    coin = re.match(r"[a-zA-Z0-9ε]*", regex)
    if not coin: 
        print("Error: La expresión regular no tiene letras o números.")
        return False, regex

    # Verificando que la expresión no tenga un * o un + al inicio.
    coincidencia = re.match(r"^(?![*+]).*", regex)

    if not coincidencia:
        print("Error: La expresión regular no puede empezar con un * o un +.")
        return "BB", regex
    
    # Verificando que la expresión no tenga un | hasta el final.
    coincidencia = re.match(r".*(?<!\|)$", regex)

    if not coincidencia:
        print("Error: La expresión regular no puede tener un | suelto.")
        return "OF", regex
    
    return True, regex
from Grammar import *

def cerradura(grammar, items):
    closure = set(items)
    added = True
    while added:
        added = False
        for item in list(closure):
            i = grammar.producciones.index(item)
            prod = grammar.producciones[i]
            if '.' not in prod.derecha:
                continue
            dot_index = prod.derecha.index('.')
            if dot_index == len(prod.derecha) - 1:
                continue
            B = prod.right[dot_index + 1]
            if B in grammar.no_terminales:
                for right in grammar.right_producciones[B]:
                    new_item = Produccion(B, ['.'] + right)
                    if new_item not in closure:
                        closure.add(new_item)
                        added = True
    return closure

def primero(grammar):
    primeros = {}
    # Inicializar los conjuntos primeros para cada símbolo
    for symbol in grammar.no_terminales | grammar.terminales:
        primeros[symbol] = set()
        if symbol in grammar.terminales:
            primeros[symbol].add(symbol)
    # Iterar hasta que no haya cambios en los conjuntos primeros
    while True:
        cambios = False
        for prod in grammar.producciones:
            right_symbols = prod.derecha
            primeros_prod = set()
            i = 0
            while i < len(right_symbols) and '' in primeros[right_symbols[i]]:
                primeros_prod |= primeros[right_symbols[i]] - {''}
                i += 1
            if i == len(right_symbols):
                primeros_prod.add('')
            elif right_symbols[i] in grammar.terminales:
                primeros_prod.add(right_symbols[i])
            else:
                primeros_prod |= primeros[right_symbols[i]] - {''}
            before = len(primeros[prod.izquierda])
            primeros[prod.izquierda] |= primeros_prod
            if len(primeros[prod.izquierda]) > before:
                cambios = True
        if not cambios:
            break
    return primeros

def siguiente(grammar, primeros):
    siguientes = {}
    # Inicializar los conjuntos siguientes para cada símbolo
    for symbol in grammar.no_terminales | grammar.terminales:
        siguientes[symbol] = set()
    # Agregar el símbolo de fin de cadena al conjunto siguiente del símbolo no terminal inicial
    siguientes[grammar.inicial].add('$')
    # Inicializar los conjuntos siguientes con los mismos símbolos que los conjuntos primeros
    siguientes.update(primeros)
    # Iterar hasta que no haya cambios en los conjuntos siguientes
    while True:
        cambios = False
        for prod in grammar.producciones:
            right_symbols = prod.derecha
            for i, symbol in enumerate(right_symbols):
                if symbol in grammar.no_terminales:
                    before = len(siguientes[symbol])
                    # El siguiente del símbolo no terminal de la derecha es el primer
                    # símbolo terminal que sigue en la producción o el conjunto siguiente
                    # del símbolo no terminal de la derecha si todos los símbolos siguientes
                    # derivan en la cadena vacía
                    if i == len(right_symbols) - 1:
                        closure = cerradura(grammar, [prod])
                        siguientes[symbol] |= closure
                    else:
                        siguientes_symbol = primeros[right_symbols[i+1]] - {''}
                        if '' in primeros[right_symbols[i+1]]:
                            siguientes_symbol |= siguientes[right_symbols[i+1]]
                        siguientes[symbol] |= siguientes_symbol
                    if len(siguientes[symbol]) > before:
                        cambios = True
            if '' in primeros[right_symbols[-1]]:
                siguientes[prod.izquierda] |= siguientes[symbol] - {''}
        if not cambios:
            break
    return siguientes

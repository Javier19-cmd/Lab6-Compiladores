import pydot
import ast
from Grammar import *
import json
# gramma = [
#     ["E", "->", "E" ,"+", "T"],
#     ["E", "->", "T"],
#     ["T", "->", "T", "*", "F"],
#     ["T", "->", "F"],
#     ["F", "->", "(", "E", ")"],
#     ["F", "->", "id"]
# ]

def aumentar_gramatica(grammar):
    """
    Aumenta la gramática y quita los símbolos de producción "->".

    Args:
        grammar (list): Gramática original.

    Returns:
        list: Gramática aumentada.
    """
    # Leyendo el primer símbolo de la gramática.
    first_symbol = grammar[0][0]
    
    # Creando la nueva gramática aumentada.
    new_grammar = []
    grammar.insert(0, [first_symbol + "'", "->", first_symbol])

    for production in grammar:
        production.insert(2, ".")
        production.pop(1)

    return grammar

def CLOUSURE(items, dot_grammar):
    """
    Calcula el conjunto de clausura para un conjunto de ítems.

    Args:
        items (list): Conjunto de ítems.
        dot_grammar (list): Gramática con el punto.

    Returns:
        list: Conjunto de clausura.
    """
    reached = []
    stack = []

    for production in items:
        stack.append(production)
        reached.append(production)

    while len(stack) != 0:
        actual_state = stack.pop()

        if actual_state.index(".") == (len(actual_state)-1):
            pass
        else:
            header = actual_state[actual_state.index(".") + 1]

            for production in dot_grammar:
                if header == production[0]:
                    if production not in reached:
                        reached.append(production)
                        stack.append(production)
    
    return reached

def mover_punto(arreglo_punto):
    """
    Mueve el punto dentro de un arreglo.

    Args:
        arreglo_punto (list): Arreglo con el punto.

    Returns:
        list: Arreglo con el punto movido.
    """
    otro = []
    for x in arreglo_punto:
        otro.append(x)

    for i in range(len(otro) - 1):
        if otro[i] == ".":
            otro[i], otro[i+1] = otro[i+1], otro[i]
            return otro
    
    return otro

def GOTO(items, symbol, dot_grammar):
    """
    Calcula el conjunto de GOTO para un conjunto de ítems y un símbolo.

    Args:
        items (list): Conjunto de ítems.
        symbol (str): Símbolo de la producción.
        dot_grammar (list): Gramática con el punto.

    Returns:
        list: Conjunto de GOTO.
    """
    reached_u = []
    stack = []

    for element in items:
        stack.append(element)

    while len(stack) != 0:
        actual_state = stack.pop()

        if actual_state.index(".") == (len(actual_state)-1):
            pass
        else:
            if actual_state[actual_state.index(".") + 1] == symbol:
                if actual_state not in reached_u:
                    reached_u.append(mover_punto(actual_state))

    reached_u = CLOUSURE(reached_u, dot_grammar)

    return reached_u

def crear_alfabeto(grama):
    """
    Crea el alfabeto de la gramática.

    Args:
        grama (list): Gramática.

    Returns:
        list: Alfabeto de la gramática.
    """
    sigma = []
    for production in grama:
        for element in production:
            if element not in sigma:
                sigma.append(element)
    return sigma

def primero(valor, grammar, terminals):
    """
    Calcula el conjunto de primeros para un símbolo de la gramática.

    Args:
        valor (str): Símbolo de la gramática.
        grammar (list): Gramática.
        terminals (list): Lista de símbolos terminales.

    Returns:
        list: Conjunto de primeros.
    """
    final = []
    stack = []
    reached = []

    stack.append(valor)
    reached.append(valor)

    if valor in terminals:
        return stack
    else:
        while len(stack) != 0:
            evaluating = stack.pop(0)
            for production in grammar:
                if production[0] == evaluating:
                    if production[2] in terminals:
                        final.append(production[2])
                    else:
                        if production[2] not in stack and production[2] not in reached:
                            stack.append(production[2])
                            reached.append(production[2])
    
    return final

def siguiente(symbol, grammar, start_symbol, terminals):
    """
    Calcula el conjunto de siguientes para un símbolo de la gramática.

    Args:
        symbol (str): Símbolo de la gramática.
        grammar (list): Gramática.
        start_symbol (str): Símbolo inicial de la gramática.
        terminals (list): Lista de símbolos terminales.

    Returns:
        set: Conjunto de siguientes.
    """
    follow_set = set()

    if symbol == start_symbol:
        follow_set.add('$')

    for production in grammar:
        for i, s in enumerate(production[2:]):
            if s == symbol:
                if i == len(production[2:]) - 1:
                    if production[0] != symbol:
                        follow_set |= siguiente(production[0], grammar, start_symbol, terminals)
                else:
                    next_symbol = production[i+3]
                    if next_symbol in terminals:
                        follow_set.add(next_symbol)
                    else:
                        follow_set |= primero(next_symbol, grammar, terminals)
                        if '' in follow_set:
                            follow_set -= {''}
                            follow_set |= siguiente(production[0], grammar, start_symbol, terminals)
    
    return follow_set

def obtener_terminales(sigma):
    """
    Obtiene los símbolos terminales del alfabeto.

    Args:
        sigma (list): Alfabeto.

    Returns:
        list: Símbolos terminales.
    """
    terminales = []

    for x in sigma:
        if x not in terminales:
            terminales.append(x)
    
    for x in terminales:
        if x.isupper() or x == ".":
            if x == "ID":
                continue
            terminales.remove(x)
    
    return terminales

def obtener_primeros_y_siguientes(gramatica):
    sigma = crear_alfabeto(gramatica)
    terminales = obtener_terminales(sigma)
    primeros = {}
    siguientes = {}

    # Obteniendo el símbolo que tiene el ' en la gramática.
    start_symbol = gramatica[0][0]

    #print("Start symbol: ", start_symbol)

    for produccion in gramatica:
        simbolo = produccion[0]
        primeros[simbolo] = primero(simbolo, gramatica, terminales)
        siguientes[simbolo] = siguiente(simbolo, gramatica, start_symbol, terminales)

    return primeros, siguientes


def crear_automataLR(gramma):
    """
    Crea el autómata LR(0) a partir de una gramática.

    Args:
        gramma (list): Gramática.

    Returns:
        tuple: Delta, estados, terminales, primeros, siguientes.
    """
    sigma = crear_alfabeto(gramma)

    que = []  # Estados
    unmarked = []  # Visitados
    dot_grammar = aumentar_gramatica(gramma)
    a = CLOUSURE([dot_grammar[0]], dot_grammar)
    que.append(CLOUSURE([dot_grammar[0]], dot_grammar))

    delta = {str(state): {} for state in que}
    delta = {x: {letra: [] for letra in sigma} for x in delta}

    unmarked.append(que[0])

    while len(unmarked) != 0:
        actual_state = unmarked.pop()

        for Symbol in sigma:
            U = GOTO(actual_state, Symbol, dot_grammar)

            if U not in que and str(U) != '[]':
                que.append(U)
                delta[str(U)] = {}
                for letra in sigma:
                    delta[str(U)][letra] = []
                unmarked.append(U)
            
            if str(U) != '[]':
                delta[str(actual_state)][Symbol].append(str(U))

    F_identificator = mover_punto(dot_grammar[0])
    F_identificator = str(F_identificator)

    """ Graficar LR(0)"""
    grafo = pydot.Dot('LR(0)', graph_type='digraph')

    def ats(s):
        return s.replace('], [', ']\n[')

    contador = 0
    for x, y in delta.items():
        node = pydot.Node(ats(x), label=f"I{contador}\n\n", shape="circle")
        grafo.add_node(node)
        contador += 1

    for x in delta:
        for y in delta[x]:
            if len(delta[x][y]) != 0:
                for w in delta[x][y]:
                    edge = pydot.Edge(ats(x), ats(w), label=repr(y), arrowhead='vee')
                    grafo.add_edge(edge)

    accept_node = pydot.Node("accept", label="ACCEPT", shape="box", color="white")
    grafo.add_node(accept_node)

    for x in delta:
        if F_identificator in x:
            edge = pydot.Edge(ats(x), "accept", label="$", arrowhead='vee')
            grafo.add_edge(edge)

    render = "GramáticaA1.png"
    grafo.set_rankdir('LR')
    grafo.write_png(render)

    terminals = obtener_terminales(sigma)
    primeros, siguientes = obtener_primeros_y_siguientes(gramma)

    # print("Primeros:")
    # for simbolo, conjunto in primeros.items():
    #     print(f"{simbolo}: {conjunto}")

    # print("Siguientes:")
    # for simbolo, conjunto in siguientes.items():
    #     print(f"{simbolo}: {conjunto}")
    goto = {}

    #print("Delta: ", delta)

    diccionario_lista = {}

    for clave, valor in delta.items():
            clave_lista = ast.literal_eval(clave)
            valor_lista = {}
            for k, v in valor.items():
                if v:
                    v_lista = ast.literal_eval(v[0])
                else:
                    v_lista = []
                
                #print("K: ", k)

                if k == "->": # Haciendo caso omiso del ->.
                    continue

                #print("v_lista: ", v_lista)

                if v_lista == []:
                    continue

                valor_lista[k] = v_lista
            
            clave_lista = Grammar(clave_lista)

            diccionario_lista[clave_lista] = valor_lista

    
    #print(diccionario_lista)

    #print("Delta: ", delta)

    F_identificator = ast.literal_eval(F_identificator)

    action = {}

    # Recorriendo cada elemento de los estados que hay en delta.
    for key, value in diccionario_lista.items():
        for el in key:
            if el[-1] == ".":
                # Realizar la acción de reduce ahora.
                action.setdefault(key, {})  # Verificar si la clave existe en el diccionario
                action[key] = {"reduce": value}

        if F_identificator in key:
            # Colocando la aceptación.
            action.setdefault(key, {})  # Verificar si la clave existe en el diccionario
            action[key]["$"] = "acceptance"

        for symbol in sigma:
            if symbol in value:
                # Colocando el shift en el action.
                action.setdefault(key, {})  # Verificar si la clave existe en el diccionario
                if not isinstance(action[key], dict):
                    action[key] = {}  # Crear un diccionario si action[key] no es un diccionario
                action[key].setdefault(symbol, {})  # Verificar si el símbolo existe en el diccionario
                action[key][symbol] = ("shift", value[symbol])
            else:
                # Colocando el goto en el goto.
                goto[key] = value

    
    print("Action table: ", action)
    print("Goto table: ", goto)
    
    # # Imprimiendo elemento por elemento del action table.
    # for key, value in action.items():
    #     print("Key: ", key, " value: ", value)

        # for ele in value:
        #     print("Elemento: " , ele, ":", value[ele])
    
    #print("Goto table: ", goto)
    #print("")

    # # Ver mejor la impresión del gotoTable.
    # for key, value in goto.items():
    #     print(key)

    #     for ele in value:
    #         print(ele, ":", value[ele])
    

    return delta, que, terminals, primeros, siguientes

#delta, que, terminals, first, follow = crear_automataLR(gramma)

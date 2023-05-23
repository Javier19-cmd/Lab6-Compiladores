import graphviz

gramma = [
    ["E", "->", "E" ,"+", "T"],
    ["E", "->", "T"],
    ["T", "->", "T", "*", "F"],
    ["T", "->", "F"],
    ["F", "->", "(", "E", ")"],
    ["F", "->", "id"]
]


def aumented_grammar(grammar): # Aumentando la gramática y quitando los ->.

    # Leyendo el primer símoblo de la gramática.
    first_symbol = grammar[0][0]
    #print("First simbol: ", first_symbol)

    # Creando la nueva gramática aumentada.
    new_grammar = []
    # Colocando la nueva producción al inicio de la lista.
    grammar.insert(0, [first_symbol+"'", "->", first_symbol])

    # Cambiando el -> por un . en la lista.
    for production in grammar:
        production.insert(2, ".")
        # Quitando el ->.
        production.pop(1)

    #grammar.append(0, [first_symbol+"'", "->", first_symbol])

    #print("New grammar: ", grammar)

    return grammar

dot_grammar = aumented_grammar(gramma)


def CLOUSURE(items, dot_grammar):
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

def MoveDot(arreglo_punto):
    otro = []
    for x in arreglo_punto:
        otro.append(x)

    for i in range(len(otro) -1):
        if otro[i] == ".":
            otro[i], otro[i+1] = otro[i+1], otro[i]
            return otro
    return otro


def GOTO(items, simbol, dot_grammar):

    reached_u = []
    stack = []

    for element in items:
        stack.append(element)

    while len(stack) != 0:
        actual_state = stack.pop()
        if actual_state.index(".") == (len(actual_state)-1):
            pass
        else:
            if actual_state[actual_state.index(".") + 1] == simbol:
                if actual_state not in reached_u:
                    reached_u.append(MoveDot(actual_state))

    # print("Goto I")
    reached_u = CLOUSURE(reached_u, dot_grammar)
    # for x in reached_u:
    #     print(x)
    return reached_u

a = CLOUSURE([dot_grammar[0]], dot_grammar)

#print(a)

def create_sigma(grama):

    sigma = []
    for production in grama:
        for element in production:
            if element not in sigma:
                sigma.append(element)
    return sigma

#sigma = ["E", "T", "(", ")", "id", "F", "*", "+"]

sigma = create_sigma(gramma)

print("Sigma: ", sigma)

que = [] # Estados.

unmarked = [] # Visitados.

que.append(CLOUSURE([dot_grammar[0]], dot_grammar))
delta = {str(state): {} for state in que}
delta = {x: {letra: [] for letra in sigma} for x in delta}

unmarked.append(que[0])

while len(unmarked) != 0:
    actual_state = unmarked.pop()
    for Symbol in sigma:
        U = GOTO(actual_state, Symbol, dot_grammar)

        if U not in que and str(U) != '[]':
            # print(f"type({type(U)})")
            # print(f"str({str(U)})")
            que.append(U)
            delta[str(U)] = {}
            for letra in sigma:
                delta[str(U)][letra] = []
            unmarked.append(U)
        if str(U) != '[]':
            delta[str(actual_state)][Symbol].append(str(U))

F_identificator = MoveDot(dot_grammar[0])
F_identificator = str(F_identificator)

""" Graficar LR(0)"""
grafo = graphviz.Digraph(name="LR(0)")
def ats(s):
    return s.replace('], [', ']\n[')

contador = 0
for x, y in delta.items():
    grafo.node(ats(x), label= f"I{contador}\n\n" , shape = "circle")
    contador += 1

for x in delta:
    for y in delta[x]:
            if len(delta[x][y]) != 0:
                for w in delta[x][y]:
                    grafo.edge(ats(x),ats(w), label = repr(y), arrowhead='vee')

grafo.node("accept", label="ACCEPT", shape="box", color="white")
for x in delta:
    if F_identificator in x:
        grafo.edge(ats(x),"accept",label = "$" ,arrowhead='vee')

render = "./src/LR(0)/"+"LR(0)_"
grafo.render(render, format="png", view="True")

def FIRST(valor, grammar, terminals):
    
    final = []
    stack = []
    reached = []
    stack.append(valor)
    reached.append(valor)

    if valor in terminals:
        return stack
    else:
        while len(stack) != 0:
            evaluando = stack.pop(0)
            for production in grammar:
                if production[0] == evaluando:
                    if production[2] in terminals:
                        final.append(production[2])
                    else:
                        if production[2] not in stack and production[2] not in reached:
                            stack.append(production[2])
                            reached.append(production[2])
    return final


def FOLLOW(symbol, grammar, start_symbol, terminals):
    follow_set = set()
    if symbol == start_symbol:
        follow_set.add('$')
    for production in grammar:
        for i, s in enumerate(production[2:]):
            if s == symbol:
                if i == len(production[2:]) - 1:
                    if production[0] != symbol:
                        follow_set |= FOLLOW(production[0], grammar, start_symbol, terminals)
                else:
                    next_symbol = production[i+3]
                    if next_symbol in terminals:
                        follow_set.add(next_symbol)
                    else:
                        follow_set |= FIRST(next_symbol, grammar, terminals)
                        if '' in follow_set:
                            follow_set -= {''}
                            follow_set |= FOLLOW(production[0], grammar, start_symbol, terminals)
    return follow_set

def obtener_terminales(sigma):
    terminales = []
    for x in sigma:
        if x not in terminales:
            terminales.append(x)

    # Quitar de la lista los elementos en mayúscula, haciendo caso omiso de ID, y el punto también.
    for x in terminales:
        if x.isupper() or x == ".":
            
            if x == "ID":
                continue
            terminales.remove(x)


    return terminales

terminals = obtener_terminales(sigma)

print("Terminales: ", terminals)

first = FIRST("T", gramma, terminals)

print("First: ", first)

follow  = FOLLOW("T", gramma, "E'", terminals)

print("Follow: ", follow)
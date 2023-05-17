from prettytable import PrettyTable
from Grammar import *
from EstadosLR import *
import copy
import pydot
import sys

new_limit = 9000  # Nuevo límite de recursión deseado
sys.setrecursionlimit(new_limit)

tabla = []


def aumentar_gramatica(gramatica): # Aumento de la gramática.
    nuevo_simbolo_inicial = gramatica.productions[0][0] + "'"
    nueva_gramatica = [[nuevo_simbolo_inicial, gramatica.productions[0][0]]]

    for produccion in gramatica.productions:
        nueva_gramatica.append(produccion)

    return nueva_gramatica

def simbolos_gramaticales(lista_producciones): # Obteniendo los símbolos gramaticales.
    simbolos = set()
    for produccion in lista_producciones:
        simbolos.add(produccion[0])
        for simbolo in produccion[1].split():
            if simbolo.isupper():
                simbolos.add(simbolo)
            elif simbolo.islower() or simbolo.isnumeric() or simbolo in ['+', '*', '(', ')', '-', '/']:
                simbolos.add(simbolo)
    return sorted(list(simbolos))

def construir_gramatica_y_conjunto_I(lista_producciones):
    # Obtener todos los no terminales de la gramática
    no_terminales = set([produccion[0] for produccion in lista_producciones])
    for produccion in lista_producciones:
        for simbolo in produccion[1]:
            if simbolo.isupper():
                no_terminales.add(simbolo)

    # Agregar producciones vacías para no terminales sin producción
    for no_terminal in no_terminales:
        if no_terminal not in [produccion[0] for produccion in lista_producciones]:
            lista_producciones.append([no_terminal, ''])

    # Construir gramática y conjunto I0
    gramatica = [[produccion[0], produccion[1]] for produccion in lista_producciones]
    I0 = []
    for produccion in gramatica:
        I0.append([produccion[0], "." + produccion[1]])

    return gramatica, I0


def CERRADURA(I, grammar):
    J = I.copy()


    # for elemet in J:
    #     print("Elementos en I: ", elemet)
    # print("")

    #print("Elementos en CERRADURA: ", J)

    # for eleme in J:
    #     print("Elementos in cerradura: ", eleme)

    estados = {}

    corazones = []

    added = True
    while added:
        added = False
        for item in J:
            simbolo = item[0] # Símbolo
            prod = item[1] # Producción

            # print("Símbolo: ", simbolo)
            # print("Producción: ", prod)

            # Si el símbolo es E' y la producción es E, entonces es un corazón.
            if simbolo == "E'":
                if prod == ".E":

                    corazon = Corazon(simbolo, prod)
                    #print("Corazón a agregar en Cerradura: ", corazon)

                    estados[corazon] = set() # Usamos un conjunto para evitar duplicados.

                    #print(estados[corazon])

            dot_pos = prod.index('.')

            #print("dot_pos: ", dot_pos)


            # Verificando si el punto no está a la izquierda, dado que eso será corazón también.
            if dot_pos > 0:

                # Imprimiendo el corazón a agregar.
                #print("item: ", item, " prod: ", prod, " posición del punto: ", dot_pos)

                #derecha_punto = dot_pos + 1

                # Viendo que hay a la derecha del punto.

                dot_po = item[1].index(".")


                if dot_po + 1 < len(prod):
                    # print("Derecha del punto: ", item[1][dot_pos + 2])

                    # print("Gramática: ", grammar)
                    # print("Viendo que hay después del punto: ", item[1][dot_pos + 2])

                    # # Si lo que hay después del punto está vacío, entonces se imprime lo que está dos espacios después.
                    # if prod[dot_po + 1] == " ":

                    #     print("Imprimiendo lo de dos espacios después: ", prod[dot_po + 2])

                    # else:

                    #     print("Imprimiendo lo de un espacio después: ", prod[dot_po + 1])



                    # Buscando en la derecha de la regla todo lo que empiece con item[1][dot_pos + 2].
                    for rule in grammar.productions:

                        if rule[1][0] == "i":
                           # print("Regla del id: ", rule[1][0:])

                            if item[1][dot_pos + 2] == rule[1][0:]:
                                #print("Regla del id: ", rule[1][0:])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                #print("Nuevo corazón: ", corazon)

                                estados[corazon] = set()

                            else:
                               # print("No hay transición", item[1][dot_pos + 2])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                estados[corazon] = set()

                        else:
                            #print("Regla: ", rule[1][0])

                            if item[1][dot_pos + 2] == rule[1][0]:
                                #print("Regla: ", rule[1][0])

                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])

                                estados[corazon] = set()

                                #print("Corazón en el else de id: ", corazon)

                            else:
                                #print("No hay transición", item[1][dot_pos + 2])
                                corazon = Corazon(simbolo, prod[:dot_pos] + prod[dot_pos:])
                                estados[corazon] = set()

                    # Buscando los restos del corazón que se acaba de hacer.
                    for rule in grammar.productions:
                        #print("Símbolo para hacerle su resto: ", simbolo)

                        # Imprimiendo lo que está a la derecha del punto.
                        #print("Símbolo para hacerle resto: ", prod[dot_pos + 1])

                        if prod[dot_pos + 1] == " ":
                            # Imprimiendo dos espacios después.
                            #print("Símbolo para hacerle resto: ", prod[dot_pos + 2])

                            #print("Regla: ", rule[1][0], " producción: ", prod[dot_pos + 2])

                            if rule[1][0] == prod[dot_pos + 2]:
                                #print("Igualdad: ", " Regla: ", rule[1][0], " producción: ", prod[dot_pos + 2])
                                pass

                            """
                            Si el prod[dot_pos + 2] es igual a rule[1][0], entonces agarrar recursivamente todo lo que empiece con prod[dot_pos + 2]
                            e ir agarrando recursivamente las reglas que empiecen con prod[dot_pos + 2] de esas reglas agarradas.

                            """

                            if rule[1][0] == "i":
                                #print("Regla del id: ", rule[1][0:])

                                if prod[dot_pos + 2] == rule[1][0:]:
                                    #print("Regla del id: ", rule[1][0:])

                                    #print("Regla: ", rule[1][0:])

                                    # Agregando el punto al principio de la regla.
                                    s = rule.copy()
                                    s[1] = "." + s[1]

                                    #print("S: ", s)

                                    # Creando un resto.
                                    res = Resto(s[0], s[1])

                                    #print("Nuevo resto: ", res)

                                    # Agarrando también lo que sea igual a la derecha del punto del nuevo resto.
                                    #print("Derecha del punto del nuevo resto: ", res.derecha[res.derecha.index(".") + 1])

                                    # #print("Derecha del resto: ", res.derecha.index("."))

                                    if res not in estados[corazon]:
                                        # # Guardando en el corazón de la producción los restos.
                                        estados[corazon].add(res)
                            
                            else: 
                                    
                                    if rule[1][0] == prod[dot_pos + 2]:
    
                                        #print("Regla: ", rule[1][0])
    
                                        # Agregando el punto al principio de la regla.
                                        s = rule.copy()
                                        s[1] = "." + s[1]
    
                                        #print("S: ", s)
    
                                        # Creando un resto.
                                        res = Resto(s[0], s[1])

                                        print("Nuevo resto: ", res)

                                        estados[corazon].add(res)

                                        #print("Derecha del punto del nuevo resto: ", res.derecha[res.derecha.index(".") + 1])

                                        # Agarrando de la gramática todas las reglas que empiecen igual a la derecha del nuevo resto.
                                        for rule2 in grammar.productions: 
                                            
                                            # Agarrando el símbolo que esté a la par del punto.
                                            if rule2[0] == res.derecha[res.derecha.index(".") + 1]:

                                                s2 = rule.copy()

                                                # Agregando el punto al principio de la regla.
                                                s2[1] = "." + s2[1]

                                                #print("S2: ", s2)

                                                # Haciendo otro resto.
                                                res2 = Resto(s[0], s[1])

                                                if res2 not in estados[corazon]:


                                                    # Agregando el resto al cuerpo de la producción.
                                                    estados[corazon].add(res2)

                                        #print("Nuevo resto: ", res)
    
                                        # #print("Derecha del resto: ", res.derecha.index("."))
    
                                        # # Guardando en el corazón de la producción los restos.
                                        # estados[corazon].add(res)

                            # Buscando en las reglas todo lo que empiece con prod[dot_pos + 2].
                            if rule[0] == prod[dot_pos + 2]:

                                #print("Regla: ", rule, " prod: ", prod[dot_pos + 2])

                                # Creando una copia de la regla.
                                s = rule.copy()

                                # Agregando el punto al principio de la regla.
                                s[1] = "." + s[1]

                                #print("S: ", s)

                                # Creando un resto.
                                res = Resto(simbolo, s[1])

                                #print("Derecha del resto: ", res.derecha.index("."))

                                if res not in estados[corazon]:

                                    # Guardando en el corazón de la producción los restos.
                                    estados[corazon].add(res)

                                # # Imprimiendo las reglas que empiezan con prod[dot_pos + 2].
                                # print("Regla: ", rule[0])


                        else:

                            print("Símbolo para hacerle resto tomando un espacio: ", prod[dot_pos + 1])

                # else:
                #     print("No hay nada a la derecha del punto.")

                # Imprimiendo el elemento que está a la izquierda del punto.
                #print("Símbolo en dot_pos > 0: ", prod[dot_pos - 1])

            # Si el punto está a la izquierda, entonces es un resto.
            if dot_pos == 0:

                # Imprimiendo lo que hay después del punto.
                #print("Resto: ", prod[dot_pos + 1:])


                if simbolo != "E'" and prod != ".E":
                    resto = Resto(simbolo, prod)

                    # Resto en cerradura.
                    #print("Resto en cerradura: ", resto)

                    # Buscar todas las producciones que empiecen con el elemento que está a la derecha del punto.
                    for rule in grammar.productions:

                        if resto.derecha[1] == "i":
                            # Agarrando el id.
                            #print("id: ", resto.derecha[1:])

                            #print("Resto: ", resto, " posición 1 en resto ", resto.derecha[1:], "Rule en la posición 0 ", rule[0])

                            if rule[1] == resto.derecha[1:]:
                                # print("rule[0]: ", rule[1])
                                # print("Agregando: ", rule[1], "resto ",resto.derecha[1:])
                                #print("Agregando: ", resto.derecha[1:])

                                estados[corazon].add(resto)

                                #added = True

                        else:

                            #print("Resto: ", resto, " posición 1 en resto ", resto.derecha[1], "Rule en la posición 0 ", rule[1][0])

                            if rule[1][0] == "i":
                                #print("id dentro del else: ",rule[1][0:])

                                #print("Agregando el id: ", rule[1][0:])

                                if rule[1][0:] == resto.derecha[1]:
                                    #print("rule[]")
                                    #print("Agregando: ", rule[1][0:], "resto ", resto.derecha[1])
                                    #print()

                                    estados[corazon].add(resto)

                                    #added = True

                            if rule[1][0] == resto.derecha[1]:

                                # print("Agregando: ", rule[0], " resto ",resto)
                                #print("Agregando: ", resto)

                                estados[corazon].add(resto)

                                #added = True
                # else:

                #     print("Otro caso para agregar el resto: ", " símbolo: ", simbolo, " prod: ", prod)

    # Imprimiendo los estados.
    for corazon, resto in estados.items():
        print("Corazón en CERRADURA: ", corazon)

        for r in resto:
            print("Resto en CERRADURA: ", r)

    # print("")

    #print(" J: ", J)
    # for esta in estados:
    #     print("Esta: ", esta)

    return estados



def ir_A(I, X, gramatica):
    """
        I: Conjunto de producciones
        X: Símbolo de gramática
        gramatica: Gramática

        Retorna el conjunto de producciones que resulta de avanzar el punto de
        todas las producciones en I que tienen a X después del punto.
    """
    J = []

    # print("Conjunto: ", I, " símbolo: ", X)

    lista_temp = []

    for corazon, resto in I.items():

        #print("Corazón: ", corazon)
        # print("Resto: ", resto)
        # print("Corazón derecha: ", corazon.derecha)
        # print("Corazón izquierda: ", corazon.izquierda)

        #print(corazon.derecha)

        #print("Corazón: ", corazon)

        # Esto solo es el corazón del estado.

        # Buscar el índice del punto.
        dot_pos = corazon.derecha.index('.')

        #print("Posición del punto: ", dot_pos, "corazón: ", corazon, " símbolo: ", X)

        # Revisando que hay a la derecha del punto para ver lo si hay movimiento.
        if dot_pos < len(corazon.derecha) - 1:

            """

                Verificar si hay espacio vacío y si lo hay revisar los símbolos después de ese.

            """

            #print("corazon.derecha: ", corazon.derecha[dot_pos + 1])

            # Si hay un espacio vacío, revisar si hay elementos después del espacio vacío.
            if corazon.derecha[dot_pos + 1] == ' ':

                #print("corazon.derecha después del espacio: ", corazon.derecha[dot_pos + 2], " X: ", X, " conjunto: ", I)

                # Verificando si el X es igual al corazon.derecha[dot_pos + 2].

                if corazon.derecha[dot_pos + 2] == X:

                    #print("corazon.derecha: ", corazon.derecha[dot_pos + 2], " X: ", X)

                    # Moviendo el punto a la derecha del símbolo.
                    corazon.derecha = corazon.derecha[:dot_pos] + " " + corazon.derecha[dot_pos + 2] + '.' + "" + corazon.derecha[dot_pos + 3:]

                    #print("Nuevo corazón cuando habían dos espacios: ", corazon)

                    cora = [corazon.izquierda, corazon.derecha]

                    #print("Nuevo corazón cuando habían dos espacios: ", cora)

                    if cora not in J:
                        J.append(cora)

                    for rule in gramatica.productions:
                        inicio = rule[1][0]

                        if inicio == "i": # Detectando el id.
                            inicio = rule[1][0:]

                        if inicio == X:
                            # Falta detectar el id.

                            # Obteniendo el índice del punto.
                            dot_pos = rule[1].index(X)

                            #print("Posición de X: ", X)

                            derecha = rule[1][:dot_pos] + rule[1][dot_pos] + '.' + rule[1][dot_pos + 1:]

                            #print("Nuevo corazón lado derecho: ", rule)

                            # Convirtiendo el rule en corazón.
                            corazon = Corazon(rule[0], derecha)

                            cora = [rule[0], derecha]

                            #print("Cora: ", cora)

                            # print("Corazón: ", corazon)

                            if cora not in J: # Guardando el corazón.
                                J.append(cora)


            else:

                # Verificando el símbolo de la derecha del punto. (aún falta detectar el caso de id)
                if corazon.derecha[dot_pos + 1] == X:
                    #print("Sí hay corrimiento. ", corazon.derecha[dot_pos + 1], X)

                    # Mover el punto a la derecha del símbolo.
                    corazon.derecha = corazon.derecha[:dot_pos] + " " + corazon.derecha[dot_pos + 1] + '.' + corazon.derecha[dot_pos + 2:]

                    #print("Corazón antes del for: ", corazon)

                    cora = [corazon.izquierda, corazon.derecha]

                    #print("Nuevo corazón: ", cora)

                    if cora not in J: # Guardando el corazón.
                        J.append(cora)

                    # Buscar en la gramática las partes derechas de las producciones.
                    for rule in gramatica.productions:
                            # Aún falta detectar el caso de id.
                            #print("Regla: ", rule[1])

                            inicio = rule[1][0] # Agarrando el inicio de la regla.

                            # Si el inicio es igual a i, entonces se jala la palabra completa.
                            if inicio == "i":
                                inicio = rule[1][0:]

                            #print("Inicio: ", inicio)

                            if inicio == X: # Si el inicio es igual a X, entonces eso será un corazón.
                                #print("Posible corazón: ", rule, " X: ", X, " inicio: ", inicio)

                                # Falta detectar el id.

                                # Obteniendo el índice del punto.
                                dot_pos = rule[1].index(X)

                                #print("Posición de X: ", X)

                                derecha = rule[1][:dot_pos] + rule[1][dot_pos] + '.' + rule[1][dot_pos + 1:]

                                #print("Nuevo corazón lado derecho: ", rule)

                                # Convirtiendo el rule en corazón.
                                corazon = Corazon(rule[0], derecha)

                                cora = [rule[0], derecha]

                                #print("Cora: ", cora)

                                #print("Corazón: ", corazon)

                                if cora not in J: # Guardando el corazón.
                                    J.append(cora)

                                # # Poniendo el punto a la derecha del símbolo y luego imprimiendo la regla.
                                # rule[1] = rule[1][:dot_pos] + rule[1][dot_pos + 1] + '.' + rule[1][dot_pos + 2:]

                                # print("Regla después de mover el punto: ", rule)


                #print("Corazón después de mover el punto: ", corazon)

        # Leyendo el punto del resto.
        if resto:
            #print("Resto: ", resto)

            for elem in resto:

                #print("Elemento: ", elem, " símbolo: ", X)

                # Buscar el índice del punto.
                dot_poss = elem.derecha.index('.')

                #print("Posición del punto: ", dot_poss, " elemento: ", elem, " símbolo: ", X)

                # Revisando que hay a la derecha del punto para ver lo si hay movimiento.
                if dot_poss < len(elem.derecha) - 1:

                    # Verificando el símbolo de la derecha del punto. (aún falta detectar el caso de id)
                    if elem.derecha[dot_poss + 1] == X:
                        #print("Sí hay corrimiento. ", elem.derecha[dot_poss + 1], X)

                        # Mover el punto a la derecha del símbolo.
                        elem.derecha = elem.derecha[:dot_poss] + elem.derecha[dot_poss + 1] + '.' + elem.derecha[dot_poss + 2:]

                        #print("Corazón antes del for: ", corazon)

                        cora = [elem.izquierda, elem.derecha]

                        #print("Corazón: ", cora)

                        if cora not in J:
                            J.append(cora)

                        #print("J: ", J)

                    if elem.derecha[dot_poss + 1] == "i":
                        # Aquí se detecta el id.
                        #print("Sí hay id. ", elem.derecha[dot_poss + 1:], X)

                        # Verificando si el símbolo es el mismo que X.
                        if elem.derecha[dot_poss + 1:] == X:

                            elem.derecha = elem.derecha[:dot_poss] + elem.derecha[dot_poss + 1:] + '.' + elem.derecha[dot_poss + 3:]

                            #print("Corazón antes del for: ", corazon)

                            cora = [elem.izquierda, elem.derecha]

                            #print("Corazón: ", cora)

                            if cora not in J:
                                J.append(cora)


    # Eliminando repeticiones de J.
    J = list(set(tuple(x) for x in J))

    # Convirtiendo las tuplas de J en listas.
    J = [list(x) for x in J]

    #print("J: ", J)

    # if J:
    #     print("J: ", J)

    #a = CERRADURA(J, gramatica)

    #CERRADURA(J, gramatica)

    return CERRADURA(J, gramatica)



def construir_automata_LR0(grammar): # Construcción de la gramática.
    """
    Construye el autómata de análisis sintáctico LR(0) a partir de una gramática dada.

    Args:
        grammar (List[List[str]]): La gramática en forma de lista de producciones.

    Returns:
        Tuple[List[Set[Tuple[str, int]]], Dict[Tuple[int, str], Tuple[int, str, int, Set[str]]], Dict[Tuple[int, str], Tuple[str, int]]]:
        Una tupla con la lista de conjuntos, el diccionario de transiciones y el diccionario de acciones.
    """
    # Aumentar la gramática
    grammara = aumentar_gramatica(grammar)

    # Obtener los símbolos gramaticales
    simbolos_gram = simbolos_gramaticales(grammara)

    # Construir la gramática y el conjunto I0
    gramatica, I0 = construir_gramatica_y_conjunto_I(grammara)

    gramatica = Grammar(gramatica)

    # print(type(gramatica))

    #print("Grammar: ", gramatica)

    #print(I0)

    # print("Gramática: ", gramatica)
    # print("Gramática aumentada: ", grammara)
    # print("I0: ", I0)

    # # Imprimiendo hacia abajo el I0.
    # for i in I0:
    #     print(i)

    # Crear la lista de conjuntos LR(0), el diccionario de transiciones y el diccionario de acciones
    C = [CERRADURA(I0, gramatica)]


    agregado = True

    while agregado:

        agregado = False

        for conjunto in C:

            for X in simbolos_gram:

                conjunto_copia = copy.deepcopy(conjunto)

                goto = ir_A(conjunto_copia, X, gramatica)

                #print("Conjunto: ", conjunto)

                # print("Conjunto: ", conjunto)
                # for cora, res in conjunto.items():
                #     print("Corazón: ", cora)

                #goto = ir_A(conjunto, X, gramatica)


                if goto and goto not in C:
                    #print("Goto: ", goto)
                    # for corazon, resto in goto.items():
                    #     print("Corazón: ", corazon)

                    #     for r in resto:
                    #         print("Resto: ", r)

                    # print("")

                    #print("Conjunto: ", conjunto, " X: ", X, " resultado ", goto)

                    tabla.append([conjunto, X, goto])

                    C.append(goto)

                    agregado = True

    # for estado in C:
    #     #pass
    #     print("Estado: ", estado)

    #     for corazon, resto in estado.items():
    #         print("Corazón: ", corazon)

    #         for r in resto:
    #             print("Resto: ", r)

    # print("Estados: ", len(C))

    #print("Gramática: ", gramatica)

    # print("len(gramatica): ", len(gramatica))

    # pri_r = []
    # sig_r = []
    
    # Recorriendo la gramática aumentada.
    for produccion in gramatica.productions:
        
        #print("Parte izquierda: ", produccion[0], " Parte derecha: ", produccion[1])

        no_terminal = produccion[0] # Agarrando el símbolo no terminal de la producción.

        #print("No terminal: ", no_terminal, " gramática: ", gramatica.productions)
        
        resultado = primero(no_terminal, gramatica)
        # print("Símbolo: ", no_terminal, " Resultado1: ", resultado)

        # if resultado not in pri_r:
        #     pri_r.append(resultado)

        print("Símbolo: ", no_terminal, " Resultado de primero: ", resultado)

        
    
    for produccion2 in gramatica.productions: 

        no_terminal2 = produccion2[0]

        resultado2 = siguiente(no_terminal2, gramatica)

        print("Símbolo: ", no_terminal, " Resultado2: ", resultado2)

        # if resultado2 not in sig_r:
        #     sig_r.append(resultado2)

        # print("Símbolo: ", no_terminal, " resultado de siguiente: ", resultado2)

    # for estadi in C:
    #     print(estadi)

    # for res1 in pri_r:
    #     print(res1)
    
    # print("")

    # for res2 in sig_r:
    #     print(res2)
    
    # print("")


    return tabla


# Definiendo la función primero.
def primero(no_terminal, gramatica):
    """
        Pasos a seguir para usar esta función.
        1. Recibir el símbolo no terminal que se va a operar y la gramática aumentada.
        2. Recorrer las producciones del símbolo no terminal y por cada producción revisar si el primer símbolo es un símbolo terminal o no. Si el símbolo es terminal, entonces 
           agregarlo al conjunto primero del no terminal actual. Si es un símbolo no terminal, calcular su conjunto "primero" y agregarlo al conjunto primero del no termnal actual. 
           Si la producción tiene un símbolo no terminal que deriva la cadena vacía agregar el conjunto "primero" del siguiente símbolo no terminal en la producción al conjunto 
           "primero" del no terminal actual.
    """

    #print("No terminal: ", no_terminal, " gramática: ", gramatica.productions)

    # Recorriendo las producciones del no terminal.

    no_terminales = []

    primeros = []

    # Guardando los no terminales en una lista. Los no terminales son los que están a la izquierda de la producción.
    for produccions in gramatica.productions:

        if produccions[0] not in no_terminales:

            no_terminales.append(produccions[0])
    
    #print("No terminales: ", no_terminales)

    for produccion in gramatica.productions:
        
        simbolo = produccion[0]
        resto = produccion[1]

        #print("no_terminal: ", no_terminal,  "símbolo: ", simbolo, " resto: ", resto)

        # Revisando el primer símbolo de la producción.
        #print("Primer símbolo: ", resto[0])

        if no_terminal == simbolo:

            psimbolo = resto[0]

            if psimbolo == "i":

                psimbolo = resto[0:]

            #print("Primer símbolo: ", psimbolo)

            # Si el primer símbolo es un símbolo terminal, agregarlo al conjunto primero del no terminal actual.

            if psimbolo not in no_terminales or psimbolo == " ":

                #print("Símbolo no terminal: ", psimbolo)

                primeros.append(psimbolo)

            elif psimbolo in no_terminales: 
                #print("No terminal detectado: ", psimbolo)

                # Recorriendo las producciones del símbolo.
                for produccions in gramatica.productions:
                    
                    # Haciendo el primero nuevamente.

                    si = produccions[0]
                    re = produccions[1]

                    if si == psimbolo:
                        ps = re[0]

                        if ps == "i":
                            ps = re[0:]

                            if ps not in no_terminales or ps == "":
                                primeros.append(ps)
                            
                            else:

                                # Obteniendo el siguiente símbolo.


                                primeros.append("")



                # # Calculando nuevamente la función primero.
                # primer = primero(psimbolo, gramatica)

                #print("Primero nuevamente: ", primer)
            
        
    #print("Símbolo: ", no_terminal, " resultado: ", primeros)

    return primeros

# Método para calcular el siguiente.
def siguiente(no_terminal, gramatica):

    siguientes = []

    if no_terminal == "E": 
        siguientes.append("$")
    
    for production in gramatica.productions: 
        
        simbolo = production[0]
        resto = production[1]

        # Si el símbolo está al final de las producciones, entonces agregar la producción al conjunto siguiente.

        # Reconociendo el último elemento del resto.
        ultimo = resto[-1]

        # Si ultimo es igual a d, entonces se jala toda la palabra.
        if ultimo == "d":
            ultimo = resto[0:]

        #print("Último elemento de la producción: ", ultimo)

        if no_terminal == ultimo:
                
            #print("No terminal: ", no_terminal, " último: ", ultimo)

            # Agregar la producción al conjunto siguiente.
            siguientes.append(production)

            #print("Siguiente: ", siguientes)
        
        # Reconociendo el medio del resto.
        medio = resto[:0] + resto[0:]

        # Obteniendo la mitad de lo anterior.
        medio = medio[1:-1]

        # Si el no terminal está en el medio de la producción, entonces agregar el conjunto primero del siguiente símbolo al conjunto siguiente del no terminal actual.
        if no_terminal in medio:
            
            #print("Medio: ", medio)
            
            sig = primero(no_terminal, gramatica)

            #print("Primero del siguiente: ", sig)

            siguientes.append(sig)
        

        # Si el resto es "", entonces agregar vacío.
        if resto == "":
            siguientes.append("")
        
    #print("Símbolo: ", no_terminal, " siguiente: ", siguientes)

    return siguientes


    
    # print("No terminales: ", no_terminales)

# grammar = Grammar([
#     ["E", "E + T"],
#     ["E", "T"],
#     ["T", "T * F"],
#     ["T", "F"],
#     ["F", "( E )"],
#     ["F", "id"]
# ]) # Gramática a utilizar.

# tabla = construir_automata_LR0(grammar)


# print(tabla)

# graph = pydot.Dot(graph_type='digraph')

# # Creando los nodos.
# nodes = set()
# for lista in tabla:
#     #print(lista)

#         #print(tupla[0])

#     # Convertir cada lista en la posición 0 de la lista a tupla si en caso no lo es.
#     if type(lista[0]) == tuple:
#         #nodes.add(lista[0])
#         pass
#     elif type(lista[0]) == list:
#         tupla_general0 = tuple(tuple(lista) for lista in lista[0])

#         #print(tupla_general0)
#         nodes.add(tupla_general0)

#     # Convertir cada lista en la posición 2 de la lista a tupla si en caso no lo es.
#     if type(lista[2]) == tuple:
#         pass
#     elif type(lista[2]) == list:
#         tupla_general2 = tuple(tuple(lista) for lista in lista[2])

#         #print(tupla_general2)
#         nodes.add(tupla_general2)

# # Agregando los nodos a la estructura de datos.
# for node in nodes:

#     #print("Nodo: ", node)

#     graph.add_node(pydot.Node(str(node)))

# # Haciendo las conexiones.
# for lista in tabla:

#     tupla0 = lista[0]
#     tupla2 = lista[2]
#     etiqueta = lista[1]

#     # print("Tupla0: ", tupla0)
#     # print("Tupla2: ", tupla2)
#     # print("Etiqueta: ", etiqueta)


#     # Conversión de la lista[0] en caso de que sea necesario.
#     if type(lista[0]) == tuple:
#         tupla0 = lista[0]
#     elif type(lista[0]) == list:
#         tupla0 = tuple(tuple(lista) for lista in lista[0])

#     # Conversión de la lista[2] en caso de que sea necesario.
#     if type(lista[2]) == tuple:
#         tupla2 = lista[2]
#     elif type(lista[2]) == list:
#         tupla2 = tuple(tuple(lista) for lista in lista[2])

#     graph.add_edge(pydot.Edge(str(tupla0), str(tupla2), label=str(etiqueta)))

#     # Poniendo el grafo de manera vertical.
#     #graph.set_rankdir("LR")

#     graph.write_png('GramáticaA1.png')
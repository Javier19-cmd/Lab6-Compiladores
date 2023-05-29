from GrammarA import *
import re
from io import StringIO
import pydot


yapar = "slr-2.yalp" # Variable que guarda el nombre del yapar.
yalex = "slr-2.yal" # Variable que guarda el nombre del yalex.

lista_tk = [] # Tokens del yalex.
lista_tkyp = [] # Tokens del yapar.

tabla_general = []

# Abriendo el archivo yalp.
with open(yapar) as y: 

    # Leyendo el archivo yalp.
    yalp = y.read()

    # print("Contenido: \n")
    # print(yalp)

    # Verificando que exista la misma cantidad de /* que de */.
    if yalp.count("/*") != yalp.count("*/"):
        #print("Error: Cantidad de comentarios /* y */ no coinciden.")

        # Buscando la línea que tiene el error.
        for i in range(len(yalp)):
            if yalp[i] == "/" and yalp[i+1] == "*":
                print("Error: Cantidad de comentarios /* y */ no coinciden en la línea " + str(i+1) + ".")
                break
    
    # Verificando que exista la misma cantidad de ; que de :.

    if yalp.count(";") != yalp.count(":"):
        print("Punto y coma o dos puntos incosistentes")
        #print("Error: Cantidad de ; y : no coinciden.")

    tokens = re.findall(r'(?<=\n)%token\s+[^%\s][^\n]*', yalp)

    toke = re.findall(r'(?<=\n)%token\s+[^%\n]+', yalp)

    #print("Toke: ", toke)

    print(" Tokens a tomar en cuenta: ", tokens)

    for token in tokens:

        #print("Token: ", token)

        token_name = token.split()[1]
        tok = token.split()[0]

        #print(token_name)

        # Guardando los tokens en una lista.
        lista_tkyp.append(token_name)

        # if tok != "%token":
        #     print(f"La definición de {token_name} es inválida")
    
    #print("Tokens del yapar: ", lista_tkyp)

    # Lista de tokens válidos
    valid_tokens = ["%token"]

    # Recorrer cada definición de token
    for token in toke:
        token_parts = token.split()
        tok = token_parts[0]
        # Verificar si la definición es válida
        if not tok.startswith("%") or (tok not in valid_tokens and len(token_parts) < 3):
            print(f"La definición de {' '.join(token_parts[1:])} es inválida.")
        else:
            for token_name in token_parts[1:]:
                print(f"La definición de {token_name} es válida.")
                lista_tkyp.append(token_name)
    
    # Quitando repeticiones de la lista lista_tkyp.
    lista_tkyp = list(dict.fromkeys(lista_tkyp))

    ti = re.findall(r'(?<=\n)token\s+[^\s][^\n]*', yalp)

    #print("Ti: ", ti)

    # Si hay una o más definiciones de token sin el %, entonces es un error.
    if len(ti) > 0:
        #print("Error: Definición de token sin el %.")
        
        # Imprimiendo la o las definiciones erróneas.
        for i in range(len(ti)):
            print("Definición errónea: ", ti[i])
    
    #print("Lista sin el token error: ", lista_tkyp)

    # Validando el token dentro del yalex.
    with open(yalex) as y:
        yalex = y.read()

        # Jalando los tokens especiales.
        if "rule tokens =" in yalex:
            # Extrayendo la cadena de texto que contiene los tokens especiales.
            cadena_tokens = yalex[yalex.find("rule tokens ="):]
            # Separando los tokens en una lista.
            lista_tokens = cadena_tokens.split("|")
            # Creando el diccionario para guardar los tokens.
            diccionario_tokens = {}
            # Iterando sobre la lista de tokens y agregándolos al diccionario.
            for token in lista_tokens:
                # Extrayendo el nombre del token y su valor.
                nombre, valor = token.split("return")
                # Agregando el token al diccionario.
                diccionario_tokens[nombre.strip()] = valor.strip().strip("\"")


            # Imprimiendo los tokens.
            #print("Imprimiendo los tokens...")
            for key, value in diccionario_tokens.items():
              #  print(f"{key.strip()} {value.strip()}")
              pass

            # Imprimiendo los valores dentro de las llaves {}.
            #print("Imprimiendo los valores dentro de las llaves {}...")
            for key, value in diccionario_tokens.items():
                token_value = value.strip()

                # Quitando los {} del token value.
                token_value = token_value.replace("{", "").replace("}", "")

                # Quitando los asteriscos y cualquier otro texto dentro de los {}
                token_value = token_value.split("(")[0].strip()
                
                lista_tk.append(token_value.strip())

                #print("Token value: ", token_value.strip())


    #print("Tokens: ", lista_tk)

    # Tokens del yalex: lista_tk.
    # Tokens del yapar: lista_tkyp.

    print("\n")

    # Verificando que los tokens de la lista_tkyp estén en la lista_tk.
    for token in lista_tkyp:
        if token not in lista_tk:
            print("Error: El token " + token + " no está definido en el yalex.")
        else: 
            print("El token " + token + " está definido en el yalex.")
    
    # Buscando en el archivo yapar la palabra IGNORE para quitar las 
    # variables que estén definidas con dicha palabra.
    with open(yapar) as ya:

        # Leyendo el archivo yapar.
        yaparr = ya.read()


        # Buscando la línea que contiene la palabra IGNORE.
        for line in yaparr.split('\n'):
            if "IGNORE" in line:
                print("La palabra IGNORE está en la línea:", line)

                # Extrayendo la cadena de texto que contiene las variables con la palabra IGNORE.
                cadena_ignore = line[line.find("IGNORE")+6:].strip()

                #print("Cadena: ", cadena_ignore)

                # Separando los tokens a ignorar en una lista.
                tokens_a_ignorar = [tok.strip() for tok in cadena_ignore.split(' ')]
                
                # Saliendo del ciclo para no procesar el resto del archivo.
                break
                
        print("Tokens a ignorar: ", tokens_a_ignorar)

        # Quitando esos tokens de la lista lista_tkyp.
        for token in tokens_a_ignorar:
            if token in lista_tkyp:
                lista_tkyp.remove(token)
        
        print("Tokens a operar en la gramática: ", lista_tkyp)


        despues = yaparr[yaparr.find("%%")+2:]

        #print("Después: ", despues)

        producciones = {}
        conjunto = None
        producciones_list = []

        with StringIO(despues) as ss: 
            for line in ss:
                #print("Line: ", line)

                if not line or line.startswith("%%"):
                    continue
                elif ":" in line: 
                    if conjunto is not None:
                        producciones[conjunto] = producciones_list

                    conjunto, producciones_list = line.split(":", 1)
                    conjunto = conjunto.strip()
                    producciones_list = [p.strip() for p in producciones_list.split("|")]

                else: 
                    producciones_list.extend([p.strip() for p in line.split("|")])

        if conjunto is not None:
            producciones[conjunto] = producciones_list

        #print(producciones)

        # Quitando de los valores los "" y los ; sobrantes.
        for key, value in producciones.items():
            for i in range(len(value)):
                value[i] = value[i].replace("\"", "").replace(";", "").strip()
        
        #print(producciones)

        # Eliminar los "" de las listas de los valores.
        for key, value in producciones.items():
            new_value = []
            for item in value:
                if item != "":
                    new_value.append(item)
            producciones[key] = new_value

        #print(producciones)
    
        grammar = []

        for key, value in producciones.items():
            for item in value:
                grammar.append([key, item])
        
        #print(grammar)

        # # Imprimiendo hacia abajo la gramática.
        # for i in grammar:
        #     print(i)

        #print("Grammar: ", grammar)

        # Diccionario para hacer las sustituciones
        replacements = {
            'expression': 'E',
            'term': 'T',
            'factor': 'F',
            'PLUS': '+',
            'MINUS': '-',
            'TIMES': '*',
            'DIV': '/',
            'LPAREN': '(',
            'RPAREN': ')',
            'ID': 'id',
            'NUMBER': 'N',
        }

        # Haciendo un parseo.
        converted_grammar = []

        for production in grammar:
            converted_production = []
            for symbol in production:
                if symbol in replacements:
                    converted_production.append(replacements[symbol])
                else:
                    # Si el símbolo es una cadena de caracteres con varias palabras
                    # se recorre y se buscan las sustituciones
                    words = symbol.split()
                    converted_words = []
                    for word in words:
                        if word in replacements:
                            converted_words.append(replacements[word])
                        else:
                            converted_words.append(word)
                    converted_production.append(' '.join(converted_words))
            converted_grammar.append(converted_production)

        #print("Gramática convertida: ", converted_grammar)

        gramatica_convertida = []

        for produccion in converted_grammar:
            simbolo = produccion[0]
            derivaciones = produccion[1:]
            for derivacion in derivaciones:
                regla = [simbolo, '->'] + derivacion.split()
                gramatica_convertida.append(regla)

        # Conversión final.
        #print("Gramática convertida: ", gramatica_convertida)

        parse_table = crear_automataLR(gramatica_convertida)
        
        # for key, value in delta.items():
        #     print("Key: ", key, "Value: ", value)

        #print("Delta: ", delta)
        #print("Action: ", action)
        #print("Goto: ", goto)

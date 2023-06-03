"""
Nombre: Javier Valle
Carnet: 20159
Clase SimuladorTxt: 
    - Se encarga de abrir el archivo de texto y leerlo
    - Va recorrer cada elemento del archivo y va a simular cada cadena dentro del AFD.

"""

from GrammarA import *
import re 
from io import StringIO



class SimuladorTxT:

    def __init__(self, diccionarios, iniciales, finales, archivo, reservadas=[], operadores_reservados=[], tokens=[], tabla={}):
        self.diccionarios = diccionarios
        self.iniciales = iniciales
        self.finales = finales
        self.archivo = archivo
        self.reservadas = reservadas
        self.operadores_reservados = operadores_reservados
        self.tokens = tokens
        self.tabla = tabla

        # Generar el parse table.
        self.jalar_yapar()

        # Variable para guardar el parse_table.
        self.parse_table = {}
        
        self.diccionario_cadenas = {} # Diccionario para las cadenas.

        self.cadena_strings = [] # Lista para guardar los strings sin comas.

        self.reservadas = ["IF", "FOR", "WHILE", "ELSE"]

        # Quitando las palabras reservadas de los tokens.
        for palabra in self.reservadas:
            if palabra in self.tokens:
                self.tokens.remove(palabra)
        
        for i, token in enumerate(self.tokens):
            self.tokens[i] = token.replace('rule gettoken =\n', '').strip()

        print(self.tokens)
        # Cambiando cosas de la tabla.
        
        # Cambiando el signo negativo.
        new_m = "-"
        for key in self.tabla:
            if "~" in self.tabla[key]:
                value = self.tabla[key].replace("~", new_m)
                self.tabla[key] = value
        
        # Cambiando el signo positivo.
        new_m = "+"
        for key in self.tabla:
            if "@" in self.tabla[key]:
                value = self.tabla[key].replace("@", new_m)
                self.tabla[key] = value
        
        # Cambiando los delimitadores.

        # Espacio en blanco.
        new_m = " "
        for key in self.tabla:
            if "≡" in self.tabla[key]:
                value = self.tabla[key].replace("≡", new_m)
                self.tabla[key] = value
        
        # Tabulador.
        new_m = "\t"
        for key in self.tabla:
            if "¥" in self.tabla[key]:
                value = self.tabla[key].replace("¥", new_m)
                self.tabla[key] = value
        
        # Quiebre de línea.
        new_m = "\n"
        for key in self.tabla:
            if "§" in self.tabla[key]:
                value = self.tabla[key].replace("§", new_m)
                self.tabla[key] = value

        print("Tabla: ", self.tabla)

        # Juntando las listas de reservadas, operadores_reservado y tokens.
        self.lista = []
        self.lista.extend(self.reservadas)
        self.lista.extend(self.operadores_reservados)
        self.lista.extend(self.tokens)

        res_copy = self.reservadas.copy()

        #print("Palabras reservadas: ", self.reservadas)

        
        self.cad_s = [] # Arreglo para las cadenas a simular.
        self.t = []
        self.cads = []


        with open(self.archivo, "r") as archivo:
            for linea in archivo:
                # Si la cadena empieza y termina con "", no se separa.
                if linea[0] == '"' and linea[-1] == '"':
                    self.cad_s.append(linea.strip())
                    self.cads.append(linea.strip())
                else:
                    # Eliminando saltos de línea y separando las cadenas.
                    cadenas = linea.strip().split()
                    # Agregando las cadenas a la lista global cad_s.
                    for cadena in cadenas:
                        if cadena[0] == '"' and cadena[-1] == '"':
                            self.cad_s.append(cadena.strip())
                            self.cads.append(linea.strip())
                        else:
                            self.cad_s.extend(cadena.split())
                            self.cads.append(linea.strip())
                    # Agregando los tokens a la lista global tokens.
                    self.t.extend(cadenas)

                    self.cads.extend(linea.strip())

                    # Regresar las cadenas separadas a self.cad_s.
                    self.cad_s.extend(cadenas)
        
        # print("self.t: ", self.t)
        # print("self.cad_s: ", self.cad_s)

        resultados_txt = self.simular_cadenas(diccionarios, iniciales, finales, resultado=[])

        #self.impresion_txt(resultados_txt) # Imprimiendo los resultados de la simulación de los archivos txt.

        resultados_res = self.simular_res()

        #self.impresion_res(resultados_res)
        
        # Generando el archivo py. 
        self.archivopy = "implmentacion.py"

        print("Tokens: ", self.tokens)
        
        self.generar_py(self.archivopy, self.diccionarios, self.iniciales, self.finales, self.archivo, res_copy, self.operadores_reservados, self.tokens, self.tabla)

    def simular_cadenas(self, diccionarios, iniciales, finales, resultado=[]): # Simulando las cadenas que vienen en el archivo txt.

        if not diccionarios:
            #print("Resultado: ", resultado)
            return resultado
        
        # # Detectando los operadores.
        # if len(caracter_actual) == 1: # Detectando primero su longitud.
        #     if caracter_actual in self.operadores_reservados: # Detectando si es un operador.
        #         print("Operador detectado")
        #         return True, estado_actual


        if len(self.cad_s) == 0:
            # Si ya no quedan más cadenas por simular, se devuelve el resultado.
            #print("Resultado: ", resultado)
            return resultado
        else:

            #print("Cad_s", self.cad_s)

            # Se toma la primera cadena en la lista de cadenas.
            cadena_actual = self.cad_s.pop(0)

            # Sacando una copia de la cadena.
            self.cadena_copy = cadena_actual

            #print("Cadena actual: ", cadena_actual)

            # Si la cadena empieza y termina con comillas dobes, es porque es una cadena entera la que se debe simular.
            if cadena_actual[0] == '"' and cadena_actual[-1] == '"':
                #print("Cadena: ", cadena_actual)

                # Si la cadena empieza y termina con comiilas, entonces se simula todo de un solo, sin dividirlo.
                # Se quitan las comillas.
                cadena_actual = cadena_actual.replace('"', '')

                #print("Cadena actual: ", cadena_actual)

            # Se simula la cadena en cada diccionario en la lista de diccionarios.
            valores_cadena = []
            for i in range(len(diccionarios)):
                diccionario = diccionarios[i]
                estado_ini = iniciales[i]
                estados_acept = finales[i]
                estado_actual = estado_ini[0]
                

                # Detectando los operadores.
                if len(cadena_actual) == 1:
                    if cadena_actual in self.operadores_reservados:

                        #print("Cadena actual: ", cadena_actual)
                        #valores_cadena.append(True)

                        # Verificando que se haya llegado al último diccionario.
                        if i == len(diccionarios) - 1:
                            # Si se llegó al último diccionario, se agrega el valor a la lista de valores de la cadena actual.
                            valores_cadena.append(True)

                    else: 
                        
                        # Verificando que se haya llegado al último diccionario.
                        if i == len(diccionarios) - 1:
                            # Si se llegó al último diccionario, se agrega el valor a la lista de valores de la cadena actual.
                            valores_cadena.append(False)

                # Se simula la cadena en el diccionario actual.
                for j in range(len(cadena_actual) - 1):
                    caracter_actual = cadena_actual[j]
                    caracter_siguiente = cadena_actual[j+1]

                    #print("Estado actual: ", estado_actual)

                    v, estado_actual = self.simular_cadena(diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept)

                    # Si hay un estado igual a {}, entonces regresarlo al inicial.
                    if estado_actual == {}:
                        estado_actual = estado_ini[0]
                        
                    if j == len(cadena_actual) - 2:
                        valores_cadena.append(v)

                    # Verificando si en la tabla está la definición de string.
            if 'string' in self.tabla: 
                
                # Si la cadena actual tenía " al principio y al final, entonces es string.
                if self.cadena_copy[0] == '"' and self.cadena_copy[-1] == '"':
                    
                    #print("Copia: ", self.cadena_copy)
                    self.cadena_strings.append(self.cadena_copy)

                    valores_cadena[-1] = True
                else:
                    valores_cadena[-1] = False
                
                # Si la cantidad de "" no está balanceada, entonces es un error.
                if self.cadena_copy.count('"') % 2 != 0:
                    
                    # Abriendo el archivo y buscando la cadena con error.
                    
                    # Buscando el número de línea en donde se encuentra la cadena actual en el archivo.
                    with open(self.archivo, "r") as archivos:
                        for i, linea in enumerate(archivos):
                            if cadena_actual in linea:
                                print("Error de formato: " + cadena_actual + " line: ", i+1, " la cadena no iene comillas balanceadas")
                    
                    # Cambiando todos sus valores de verdad a falso.
                    for i in range(len(valores_cadena)):
                        valores_cadena[i] = False

            
            # Verificando si hay un endline en la tabla.
            if 'endline' in self.tabla:
                endline = self.tabla['endline']

                # Quitando los paréntesis al endline.
                endline = endline.replace('(', '')
                endline = endline.replace(')', '')

                # 8 y 9.
                if valores_cadena[7] == True and valores_cadena[8] == True:
                    pass
                elif valores_cadena[7] == False and valores_cadena[8] == False:
                    pass
                elif valores_cadena[7] == False and valores_cadena[8] == True:

                    if cadena_actual in self.reservadas: # Si la cadena es reservada, entonces no pasa nada. 
                        pass
                    
                    else:
                        for i in range(len(valores_cadena)):
                            valores_cadena[i] == False
                        # Buscando el número de línea en donde se encuentra la cadena actual en el archivo.
                        with open(self.archivo, "r") as archivos:
                            for i, linea in enumerate(archivos):
                                if cadena_actual in linea:
                                    print("La cadena: " + cadena_actual + " line: ", i+1, " no termina en: ", endline)
            
            # Verificando si hay un number en la especificación del yalex.
            if 'number' in self.tabla:
                # # Obteniendo la posición del number en la tabla.
                # pos_number = self.tabla['number']

                # # Imprimiendo la posición.
                # print("Posición del number: ", pos_number)

                posicion = list(self.tabla.keys()).index('number')
                #print("Posicón del number: ", posicion)

                # Imprimiendo el valor de verdad de lo que sea que haya en sus valores.
                #print("Valores de la cadena: ", valores_cadena[posicion], " cadena: ", cadena_actual)

                # Si la cadena actual (o sea el número con decimal) tiene una coma de más o un signo de más, entonces es un error.
                # Revisando la escritura del número.
                num_comas = cadena_actual.count(',')

                # Si hay más de una coma, entonces es un error.
                if num_comas > 1:
                    # Buscando el número de línea en donde se encuentra la cadena actual en el archivo.
                    with open(self.archivo, "r") as archivos:
                        for i, linea in enumerate(archivos):
                            if cadena_actual in linea:
                                print("Error de formato: " + cadena_actual + " line: ", i+1, " la cadena tiene una coma de más")
                    
                    # Cambiando todos sus valores de verdad a falso.
                    for i in range(len(valores_cadena)):
                        valores_cadena[i] = False
                
                # Contando la cantidad de signos + o - que pueda tener el número.
                num_signos = cadena_actual.count('+') + cadena_actual.count('-')

                # Si hay más de un signo, entonces es un error.
                if num_signos > 1:
                    # Buscando el número de línea en donde se encuentra la cadena actual en el archivo.
                    with open(self.archivo, "r") as archivos:
                        for i, linea in enumerate(archivos):
                            if cadena_actual in linea:
                                print("Error de formato: " + cadena_actual + " line: ", i+1, " la cadena tiene un signo de más")
                    
                    # Cambiando todos sus valores de verdad a falso.
                    for i in range(len(valores_cadena)):
                        valores_cadena[i] = False
            
            # Guardando la cadena y sus resultados en un diccionario.
            self.diccionario_cadenas[cadena_actual] = valores_cadena

            # Se agrega la lista de valores de la cadena actual al resultado.
            resultado.append(valores_cadena)

            #print("Cadena: ", cadena_actual, "resultados: ", valores_cadena)

            # # Verificando si hay un true en la lista de valores cadena.
            # if True in valores_cadena:
            #     pass
            # else:
            #     # Buscando el número de línea en donde se encuentra la cadena actual en el archivo.
            #     with open(self.archivo, "r") as archivos:
            #         for i, linea in enumerate(archivos):
            #             if cadena_actual in linea:
            #                 print("Sintax error: " + cadena_actual + " line: ", i+1)

            # if cadena_actual in self.reservadas:
            #     # Si la cadena actual es una palabra reservada, se agrega a la lista de resultados.
            #     print("Palabra reservada", cadena_actual)
            #     #resultado.append(True)
            #     #print("Cadena: ", cadena_actual, "resultados: ", True)


            # Se llama recursivamente a la función con las listas actualizadas.
            return self.simular_cadenas(diccionarios, iniciales, finales, resultado)
    
    def simular_res(self):
        # Variables de seguimiento.
        ultima_vez_operador = False
        ultima_vez_reservada = False
        ultima_vez_token = {}

        diccionario = {}

        for clave in self.tokens:
            ultima_vez_token[clave] = False
        
        print(self.tokens)

        for clave in self.diccionario_cadenas:
            lista = self.diccionario_cadenas[clave]

            #print("Lista: ", lista, " clave: ", clave)

            # Verificando la forma de la expresión regular, si es un número y fue aceptado alguna vez, entonces se imprime como number.
            
            if len(lista) > 1:
            
                if lista[3] == True and lista[4] == True:

                    # Imprimiendo la clave como number.
                    print("Token: " + clave + " type: number")

            # Detectando los errores.
            if len(lista) == 1:
                if lista[0] == True:
                    # Imprimiendo el operador detectado.
                    print("Operador detectado: ", clave)
                
                elif lista[0] == False:
                    # Abriendo el archivo para buscar el caracter.
                    with open(self.archivo, "r") as ar:
                        for a, linea in enumerate(ar):
                            if clave in linea:
                                print("Lexical error: " + clave + " line: ", a+1)
            
            for i, valor in enumerate(lista):

                # BUscando el token en la tabla de símbolos definida.
                for s, (key, value) in enumerate(self.tabla.items()):

                    if valor == True:

                        if i == s:
                            # En el caso de los tokens encontrados, imprime el último que se encontró de cada uno.
                            if key in self.tokens:
                                if clave in self.reservadas:
                                    # Si la cadena actual es una palabra reservada, se agrega a la lista de resultados.
                                    print("Palabra reservada: ", clave)
                                    ultima_vez_reservada = True
                                    ultima_vez_token[key] = False
                                    ultima_vez_operador = False
                                
                                elif key in self.operadores_reservados:

                                    if not ultima_vez_operador:
                                        print("Operador reservado: ", clave)
                                        ultima_vez_operador = True
                                        ultima_vez_reservada = False
                                        ultima_vez_token[key] = False
                                else: 

                                    ultima_vez_operador = False
                                    ultima_vez_reservada = False
                                    ultima_vez_token[key] = True

                                    diccionario[clave] = key

        #print("Diccionario: ", diccionario)    
        
            #print("Cadena strings: ", self.cadena_strings)

        new_dict =  {}

        for k, v in diccionario.items():
            if not isinstance(v, bool):
                new_dict[k] = v
        
        # Imprimiendo los tokens encontrados.
        for keys, value in new_dict.items():


            if value == "string":
                
                #print("S: ", self.cadena_strings)

                string2 = self.cadena_strings.pop()

                comillas = 0
                palabra = ''
                for c in string2:
                    if c == '"':
                        comillas += 1
                        if comillas == 2:
                            print('"' + palabra.strip() + '"' + " type: " + value)
                            palabra = ''
                            comillas = 0
                    else:
                        palabra += c
                if palabra:
                    print('"' + palabra.strip() + '"')

                #print("Token: \"" + keys + "\" type: " + value)
            else: 
                print("Token: " + keys + " type: " + value)
        
        #print("New_dict: ", new_dict)

        # if len(self.cadena_strings) > 0:

        #     print("Copia: ", self.cadena_strings)

        #     # Sacar antes una copia de lo que hay adentro.
        #     cadena_stringss = self.cadena_strings.copy()

        #     self.cadena_strings = [x.strip('"') for x in self.cadena_strings]
        #     result = ', '.join(self.cadena_strings).split('" ')
        #     print(cadena_stringss)
        #     print(result)

        #     print(result.pop())

        #strs = []

        # keys_to_modify = [key for key, value in new_dict.items() if value == 'string']

        # # Iterar sobre la lista de claves para modificar el diccionario
        # for key in keys_to_modify:
        #     new_dict['"' + key + '"'] = new_dict.pop(key)
            
        # print(new_dict)

            # Imprime los tokens encontrados.
            #print("Tokens encontrados: ", diccionario)

            #print(diccionario)

            # # Imprimiendo el diccionario llave por llave.
            # for keys, value in diccionario.items():

            #     if value == "string":
            #         print("Token: \"" + keys + "\" type: " + value)
            #     else:
            #         print("Token: " + keys + " type: " + value)

    def simular_cadena(self, diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept):

        #print("Caracter: ", caracter_actual)

        #print("Estados de aceptación: ", estados_acept)

        transiciones = diccionario[estado_actual]

        #print("Transiciones; ", transiciones)

        # print("Caracter actual: ", caracter_actual)
    
        if caracter_actual in transiciones:
            estado_siguiente = transiciones[caracter_actual]

            #print("Estado siguiente: ", estado_siguiente)

            if estado_siguiente in estados_acept:
                #print("Cadena aceptada.")
                #print("Cadena aceptada: ", self.cadena_copy)
                #result = self.slr_parse(self.parse_table, self.cadena_copy)

                #print("Result parse: ", result)
                return True, estado_actual
            
            # if estado_actual in estados_acept:
            #     print("Cadena aceptada.")
            #     return True, estado_actual

            if estado_siguiente == {}:

                #print("Falso en caracter actual", estado_siguiente)
                # print("Estado actual: ", estado_actual)
                # print("Estado siguiente: ", estado_siguiente)

                return False, estado_actual
            
            elif estado_siguiente in estados_acept:
                #print("Cadena aceptada.")
                #print("Cadena aceptada: ", self.cadena_copy)
                #result = self.slr_parse(self.parse_table, self.cadena_copy)

                #print("Result parse: ", result)
                return True, estado_actual
        
            else:

                #print("Estado: ",estado_actual, estado_actual in estados_acept)

                # Si el estado siguiente es vacío.
                return True, estado_siguiente
            
        elif caracter_siguiente in transiciones:

            # Si no hay transición para el caracter actual, pero sí para el siguiente.
            estado_siguiente = transiciones[caracter_siguiente]

            if estado_siguiente in estados_acept:
                #print("Cadena aceptada.")

                #print("Cadena aceptada: ", self.cadena_copy)
                #result = self.slr_parse(self.parse_table, self.cadena_copy)

                #print("Result parse: ", result)
                return True, estado_siguiente

            if estado_siguiente == {}:
                
                #print("Falso en caracter siguiente", estado_siguiente)

                # Si el estado siguiente no es vacío.
                return False, estado_siguiente
            
            elif estado_siguiente in estados_acept:
                #print("Cadena aceptada.")
                #print("Cadena aceptada: ", self.cadena_copy)


                # Mandando esto al slr_parse.
                #result = self.slr_parse(self.parse_table, self.cadena_copy)

                #print("Result parse: ", result)

                return True, estado_siguiente
        
            else:
                #print("Estado: ", estado_siguiente)
                #print("Estado: ", estado_siguiente in estados_acept)
                # Si el estado siguiente es vacío.
                return True, estado_siguiente
        
        elif caracter_actual not in transiciones:

            return False, estado_actual
            
        else:
    
            #print("Estado actual: ", estado_actual, transiciones)

            if transiciones != {}:
                # Si no hay transición para el caracter actual ni para el siguiente.
                return True, estado_actual
            
            else: 
            
                # Si no hay transición para el caracter actual ni para el siguiente.
                return False, estado_actual

    def jalar_yapar(self):
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
                if "rule gettoken =" in yalex:
                    # Extrayendo la cadena de texto que contiene los tokens especiales.
                    cadena_tokens = yalex[yalex.find("rule gettoken ="):]
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

                self.parse_table = parse_table

                print("Parse table: ", self.parse_table)


    

    def slr_parse(self, parse_table, input_token):
        
        # Creando una pila para el análisis y agregar el estado inicial a la pila.
        stack = [0]

        # Agregando un índice para el seguimiento de los tokens de entrada.
        input_index = 0

        # Iterando hasta que se complete el análisis o se encuentre un error.
        while True: 

            # Se obtiene el estado actual de la cima de la pila.
            state = stack[-1]

            # Se obtiene el siguiente token de entrada.
            token = input_token[input_index]

            # Se obtiene la acción de la tabla de análisis.
            action = parse_table[state][token]

            # Realizar la acción según el tipo.
            if action[0] == "shift":

                # Se hace un desplazamiento (shift) y se actualiza la pila y el índice.
                stack.append(token)
                input_index += 1

            elif action[0] == "reduce":
                # Realizar una reducción (reduce) y se actualiza la pila.
                reduction = action[1]

                for _ in range(len(reduction)):
                    stack.pop()
                    stack.pop()

                    # Obteniendo el nuevo estado actual y el símbolo no terminal.
                    state = stack[-1]
                    non_terminal = reduction[0]

                    # Obteniendo la acción correspondiente al símbolo no terminal en el estado actual de la tabla de análisis gramatical.
                    goto = parse_table[state][non_terminal]

                    # Realizando el desplazamiento (shift) con el símbolo no terminal y se actualiza la pila.
                    stack.append(non_terminal)
                    stack.append(goto)
            
            elif action[0] == "accept":
                # Se acepta la entrada.
                return True
            
            else: 
                # Se rechaza la entrada.
                return False

    # Generando el archivo .py.
    def generar_py(self, nombre, diccionarios, iniciales, finales, archivo, reservadas, operadores_reservados, tokens, tabla):

        # print(diccionarios)
        # print(iniciales)
        # print(finales)
        # print(archivo)
        # print(reservadas)
        vacio = {}
        diccionario_cadenas = {}
        vacio2 = {}
        cadena_strings = []
    

        datas = f"""
diccionarios = {'{}'}
iniciales = {'{}'}
finales = {'{}'}
archiv = {'{}'}
reservadas = {'{}'}
vacio = {'{}'}
operadores_reservados = {'{}'}
tokens = {'{}'}
tabla = {'{}'}
diccionario_cadenas = {'{}'}
vacio2 = {'{}'}
cadena_strings = {'{}'}
    
def main():
    
    # Juntando la lista de reservadas, operadores_reservados y tokens.
    lista = []
    lista.extend(reservadas)
    lista.extend(operadores_reservados)
    lista.extend(tokens)

    res_copy = reservadas.copy()
    
    cad_s = [] # Arreglo para las cadenas a simular.
    t = []
    cads = []


    with open(archiv, "r") as archivo:
        for linea in archivo:
            # Si la cadena empieza y termina con "", no se separa.
            if linea[0] == '"' and linea[-1] == '"':
                cad_s.append(linea.strip())
                cads.append(linea.strip())
            else:
                # Eliminando saltos de línea y separando las cadenas.
                cadenas = linea.strip().split()
                # Agregando las cadenas a la lista global cad_s.
                for cadena in cadenas:
                    if cadena[0] == '"' and cadena[-1] == '"':
                        cad_s.append(cadena.strip())
                        cads.append(linea.strip())
                    else:
                        cad_s.extend(cadena.split())
                        cads.append(linea.strip())
                # Agregando los tokens a la lista global tokens.
                t.extend(cadenas)

                cads.extend(linea.strip())

                # Regresar las cadenas separadas a self.cad_s.
                cad_s.extend(cadenas)
    
    simular_cadenas(diccionarios, cad_s, iniciales, finales) # Simulando las cadenas del txt.

    simular_res() # Haciendo otras cosas.
    
    #print("Listas: ", cad_s, t, cads)

# Método para simular las cadenas.
def simular_cadenas(diccionarios, cad_s, iniciales, finales, resultado=[]):
    
    if not diccionarios:
        return resultado
    
    if len(cad_s) == 0:
        # Si ya no quedan más cadenas por simular, se devuelve el resultado.
        return resultado
    else: 

        # Se toma la primera cadena en la lista de cadenas.
        cadena_actual = cad_s.pop(0)

        #print("Cadena actual ", cadena_actual)

        # Sacando una copia de la cadena.
        cadena_copy = cadena_actual
        
        # Si la cadena empieza y termina con comillas dobes, es porque es una cadena entera la que se debe simular.
        if cadena_actual[0] == '"' and cadena_actual[-1] == '"':
            # Si la cadena empieza y termina con comiilas, entonces se simula todo de un solo, sin dividirlo.
            # Se quitan las comillas.
            cadena_actual = cadena_actual.replace('"', '')

        
        valores_cadena = []
        for i in range(len(diccionarios)):
            diccionario = diccionarios[i]
            estado_ini = iniciales[i]
            estados_acept = finales[i]
            estado_actual = estado_ini[0]

            if len(cadena_actual) == 1:
                
                # Detectando los operadores.
                if cadena_actual in operadores_reservados:
                    
                    if i == len(diccionarios) - 1:
                        valores_cadena.append(True)
                
                else:

                    # Verificando que se haya llegado al último diccionario.
                    if i == len(diccionarios) - 1:
                        valores_cadena.append(False)
            
            # Se simula la cadena en el diccionario actual.
            for j in range(len(cadena_actual) - 1):
                caracter_actual = cadena_actual[j]
                caracter_siguiente = cadena_actual[j+1]

                v, estado_actual = simular_cadena(diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept)
                
                #print("v: ", v, "estado_actual: ", estado_actual)
                #print(valores_cadena)

                # Si hay un estado igual a vacío, entonces regresarlo al inicial.
                if estado_actual == vacio:
                    estado_actual = estado_ini[0]
                
                if j == len(cadena_actual) - 2:
                    valores_cadena.append(v)
        
        # Verificando si en la tabla está la definición de string.
        if 'string' in tabla: 
            
            # Si la cadena actual tenía " al principio y al final, entonces es string.
            if cadena_copy[0] == '"' and cadena_copy[-1] == '"':
                
                cadena_strings.append(cadena_copy)

                valores_cadena[-1] = True
            else:
                valores_cadena[-1] = False
        
        # Verificando si hay un endline en la tabla.
        if 'endline' in tabla:
            endline = tabla['endline']

            # Quitando los paréntesis al endline.
            endline = endline.replace('(', '')
            endline = endline.replace(')', '')

            # 8 y 9.
            if valores_cadena[7] == True and valores_cadena[8] == True:
                pass
            elif valores_cadena[7] == False and valores_cadena[8] == False:
                pass
            elif valores_cadena[7] == False and valores_cadena[8] == True:

                if cadena_actual in reservadas: # Si la cadena es reservada, entonces no pasa nada. 
                    pass
                
                else:
                    for i in range(len(valores_cadena)):
                        valores_cadena[i] == False
                    # Buscando el número de línea en donde se encuentra la cadena actual en el archivo.
                    with open(archiv, "r") as archivos:
                        for i, linea in enumerate(archivos):
                            if cadena_actual in linea:
                                print("Sintax error: " + cadena_actual + " line: ", i+1)
        
        # Guardando la cadena y sus resultados en un diccionario.
        diccionario_cadenas[cadena_actual] = valores_cadena

        # Se agrega la lista de valores de la cadena actual al resultado.
        resultado.append(valores_cadena)

        # Verificando si hay un true en la lista de valores cadena.
        if True in valores_cadena:
            pass
        else: 
            with open(archiv, "r") as ar:
                for a, linea in enumerate(ar):
                    if cadena_actual in linea:
                        print("Sintax error: " + cadena_actual + " line: ", a+1)


    #print("Resultado: ", diccionario_cadenas)
    return simular_cadenas(diccionarios, cad_s, iniciales, finales, resultado) # Recursión.


def simular_cadena(diccionario, estado_actual, caracter_actual, caracter_siguiente, estados_acept):
    #print("Estados de aceptación: ", estados_acept)

    transiciones = diccionario[estado_actual]

    #print("Transiciones; ", transiciones)

    # print("Caracter actual: ", caracter_actual)

    if caracter_actual in transiciones:
        estado_siguiente = transiciones[caracter_actual]

        #print("Estado siguiente: ", estado_siguiente)

        if estado_siguiente in estados_acept:
            #print("Cadena aceptada.")
            return True, estado_actual
        
        # if estado_actual in estados_acept:
        #     print("Cadena aceptada.")
        #     return True, estado_actual

        if estado_siguiente == vacio:

            #print("Falso en caracter actual", estado_siguiente)
            # print("Estado actual: ", estado_actual)
            # print("Estado siguiente: ", estado_siguiente)

            return False, estado_actual
        
        elif estado_siguiente in estados_acept:
            #print("Cadena aceptada.")
            return True, estado_actual
    
        else:

            #print("Estado: ",estado_actual, estado_actual in estados_acept)

            # Si el estado siguiente es vacío.
            return True, estado_siguiente
        
    elif caracter_siguiente in transiciones:

        # Si no hay transición para el caracter actual, pero sí para el siguiente.
        estado_siguiente = transiciones[caracter_siguiente]

        if estado_siguiente in estados_acept:
            #print("Cadena aceptada.")
            return True, estado_siguiente

        if estado_siguiente == vacio:
            
            #print("Falso en caracter siguiente", estado_siguiente)

            # Si el estado siguiente no es vacío.
            return False, estado_siguiente
        
        elif estado_siguiente in estados_acept:
            #print("Cadena aceptada.")
            return True, estado_siguiente
    
        else:
            #print("Estado: ", estado_siguiente)
            #print("Estado: ", estado_siguiente in estados_acept)
            # Si el estado siguiente es vacío.
            return True, estado_siguiente
    
    elif caracter_actual not in transiciones:

        return False, estado_actual
        
    else:

        #print("Estado actual: ", estado_actual, transiciones)

        if transiciones != vacio:
            # Si no hay transición para el caracter actual ni para el siguiente.
            return True, estado_actual
        
        else: 
        
            # Si no hay transición para el caracter actual ni para el siguiente.
            return False, estado_actual

def simular_res(): # Simulando otras cosas.

    # Variables de seguimiento.
    ultima_vez_operador = False
    ultima_vez_reservada = False
    ultima_vez_token = vacio

    diccionario = vacio

    for clave in tokens:
        ultima_vez_token[clave] = False
    
    print(diccionario_cadenas)

    for clave in diccionario_cadenas:
        lista = diccionario_cadenas[clave]

        # Detectando los errores.
        if len(lista) == 1:
            if lista[0] == True:
                print("Operador detectado")
            
            elif lista[0] == False:
                # Abriendo el archivo para buscar el caracter.
                with open(archiv, "r") as ar:
                    for a, linea in enumerate(ar):
                        if clave in linea:
                            print("Sintax error: " + clave + " line: ", a+1)
        
        for i, valor in enumerate(lista):

            # BUscando el token en la tabla de símbolos definida.
            for s, (key, value) in enumerate(tabla.items()):

                if valor == True:

                    if i == s:
                        # En el caso de los tokens encontrados, imprime el último que se encontró de cada uno.
                        if key in tokens:
                            if clave in reservadas:
                                # Si la cadena actual es una palabra reservada, se agrega a la lista de resultados.
                                print("Palabra reservada: ", clave)
                                ultima_vez_reservada = True
                                ultima_vez_token[key] = False
                                ultima_vez_operador = False
                            
                            elif key in operadores_reservados:

                                if not ultima_vez_operador:
                                    print("Operador reservado: ", clave)
                                    ultima_vez_operador = True
                                    ultima_vez_reservada = False
                                    ultima_vez_token[key] = False
                            else: 

                                ultima_vez_operador = False
                                ultima_vez_reservada = False
                                ultima_vez_token[key] = True

                                diccionario[clave] = key

    print("Diccionario: ", diccionario)    
    
    new_dict =  vacio2

    for k, v in diccionario.items():
        if not isinstance(v, bool):
            new_dict[k] = v
    
    print("Diccionario: ", new_dict)
    
    # Imprimiendo los tokens encontrados.
    for keys, value in new_dict.items():


        if value == "string":
            #print("Token: "" + keys + "" type: " + value)

            string2 = cadena_strings.pop()

            comillas = 0
            palabra = ''
            for c in string2:
                if c == '"':
                    comillas += 1
                    if comillas == 2:
                        print('"' + palabra.strip() + '"' + " type: " + value)
                        palabra = ''
                        comillas = 0
                else:
                    palabra += c
            if palabra:
                print('"' + palabra.strip() + '"')

        else: 
            print("Token: " + keys + " type: " + value)
                

if __name__ == "__main__":
    main()

""".format(diccionarios, iniciales, finales, str('"{}"'.format(archivo)), reservadas, vacio, operadores_reservados, tokens, tabla, diccionario_cadenas, vacio2, cadena_strings)
        
        with open(nombre, 'w', encoding='utf-8') as f:
            f.write(datas)
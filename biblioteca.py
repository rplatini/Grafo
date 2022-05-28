import math
from cola import Cola
from pila import Pila
import collections
import random
import sys 
sys.setrecursionlimit(4000000)

MAX_LINKS = 20
CANTIDAD_ITERACIONES = 15

'''
pre: -
post: imprime por pantalla las operaciones que se pueden utilizar
'''
def listar_operaciones():
    operaciones = ["camino", "conectados", "ciclo", "rango", "diametro", "comunidad", "navegacion", "lectura"]
    for operacion in operaciones: 
        print(operacion)


# Funciones implementadas

# pre: el camino esta inicializado
# post: imprime el camino pasado por parametro y el costo de este, si se paso por parametro
def imprimir_camino(camino, costo = None):
    print(' -> '.join(camino))
    if costo is not None:
        print(f'Costo: {costo}')

# pre: el resultado esta inicializado
# post: imprime el resultado pasado por parametro
def imprimir_salida(resultado): 
    print(', '.join(resultado))

# pre:- la pagina esta dentro de una sublista
#     - devuelve la sublista en la que se encuentra la pagina pasada por parametro

def buscar_comunidad_pagina(comunidades, pagina):
    for c in comunidades:
        if pagina in comunidades[c]:
            return comunidades[c]


def buscar_conexion_pagina(conexiones, pagina):
    for cfc in conexiones:
        if pagina in cfc:
            return cfc


#funcion interna
# pre: origen y destino estan creados, padres esta inicializado
# post: devuelve el camino que hay entre origen y destino 
def reconstruir_camino(padres, origen, destino):
    camino = []
    actual = destino
    while actual != origen:
        camino.append(actual)
        actual = padres[actual]
    camino.append(origen)
    camino.reverse()
    return camino


# funcion interna
# pre: el grafo esta creado, origen pertenece al grafo
# post: devuelve un diccionario de los padres de cada vertice y otro de las distancias de cada vertice al vertice de origen 
def camino_minimo(grafo, origen):
    visitados, padres, distancia = {}, {}, {}

    for v in grafo.obtener_vertices():
        distancia[v] = math.inf
    
    padres[origen] = None
    distancia[origen] = 0
    visitados[origen] = True
    
    q = Cola()
    q.encolar(origen)

    while not q.esta_vacia():
        v = q.desencolar()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                distancia[w] = distancia[v] + 1
                visitados[w] = True
                padres[w] = v
                q.encolar(w)

    return padres, distancia


# pre: el grafo fue creado, origen y destino pertenecen al grafo
# post: devuelve una tupla con el camino mas corto desde el vertice de origen al de destino, y su costo
def camino_mas_corto(grafo, origen, destino):
    padres, distancia = camino_minimo(grafo, origen)
    costo = distancia[destino]

    if distancia[destino] == math.inf: return None

    camino = reconstruir_camino(padres, origen, destino)
    return (camino, costo)
    
# funcion interna
# pre: el grafo fue creado, el diccionario label esta inicializado
# post: devuelve un diccionario de listas que contienen las labels de todos los vertices que tienen como adyacente al vertice que es clave del diccionario
def calcular_entradas(grafo, label):
    grado_entrada = {}
    for v in grafo.obtener_vertices():
        grado_entrada[v] = []

    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
                grado_entrada[w].append(label[v])
    return grado_entrada

# funcion interna
# pre: entradas y adyacentes son listas inicializadas que contienen vertices
# post: devuelve la label que aparece mas frecuentemente entre la lista de adyacentes pasada por parametro
def max_freq(entradas, adyacentes):
    max_frecuencia = 0
    max_label = 0

    for label in entradas:
        freq = adyacentes.count(label)
        if freq > max_frecuencia:
            max_frecuencia = freq
            max_label = label
    
    return max_label

#funcion interna
# pre: label es un diccionario inicializado
# post: agrega al diccionario de comunidades listas con las comunidades halladas
def agregar_comunidades(label, comunidades):
    for v in label.values():
        if v not in comunidades:
            comunidades[v] = []
    
    for v in label:
        comunidades[label[v]].append(v)
    

# pre: el grafo esta creado
# post: agrega todas las comunidades de un grafo al diccionario de comunidades pasado por parametro
def buscar_comunidades(grafo, comunidades):
    label = {}
    vertices = grafo.obtener_vertices()
    adyacentes = {}

    for v in vertices:
        label[v] = v

    random.shuffle(vertices) 
    entradas = calcular_entradas(grafo, label) 

    for i in range(0, CANTIDAD_ITERACIONES):
        for v in vertices:
            label[v] = max_freq(entradas[v], grafo.adyacentes(v))
    
    agregar_comunidades(label, comunidades)



def _ciclo(grafo, actual, origen, n, visitados, ciclo_n): 
    visitados.add(actual)
    ciclo_n.append(actual)
    
    if len(ciclo_n) == n:
        if origen in grafo.adyacentes(actual):
            ciclo_n.append(origen) 
            return ciclo_n
        return None

    for w in grafo.adyacentes(actual):
        if w in visitados: continue 
        resultado = _ciclo(grafo, w, origen, n, visitados, ciclo_n)
        if resultado != None: 
            return resultado
        ciclo_n.pop()

    visitados.remove(actual)
    return None

# pre: el grafo esta inicializado, la pagina pertenece al grafo y n es el largo del ciclo que se quiere buscar
# post: devuelve un ciclo de largo n empezando por la pagina pasada por parametro, si no existe devuelve None
def ciclo(grafo, pagina, n):
    visitados = set()
    ciclo_n = []
    return _ciclo(grafo, pagina, pagina, n, visitados, ciclo_n)



def buscar_cfc(grafo, v, apilados, pila, visitados, orden, mb, contador, cfc):
    visitados.add(v)
    pila.apilar(v)
    apilados.add(v)
    orden[v] = contador 
    mb[v] = contador

    for w in grafo.adyacentes(v):
        if w not in visitados:
            buscar_cfc(grafo, w, apilados, pila, visitados, orden, mb, contador+1, cfc)
            
        if w in apilados and mb[w] < mb[v]:
            mb[v] = mb[w]

    if mb[v] == orden[v] and len(apilados) > 0: # si el orden de v es igual a su mb luego de recorrer todos los ady --> CFC
        nueva_cfc = []
        while True:
            p = pila.desapilar()
            apilados.remove(p)
            nueva_cfc.append(p)
            if v == p:
                break
        cfc.append(nueva_cfc)

# pre: el grafo esta creado 
# post: devuelve todas las componentes fuertemente conexas del grafo
def conectividad(grafo, conexiones):
    apilados = set()
    pila = Pila()
    visitados = set()
    orden = {}
    mb = {}
    contador = 0
    
    for v in grafo.obtener_vertices(): # recorro todos los vertices
        if v not in visitados:
            buscar_cfc(grafo, v, apilados, pila, visitados, orden, mb, contador, conexiones)


# pre: el grafo esta creado
# post: devuelve el diametro del grafo, que es el camino minimo mas largo, y su costo
def calcular_diametro(grafo, diametro):
    distancia_max = 0
    padres_camino_max = {}
    origen, destino = None, None

    for v in grafo.obtener_vertices(): 
        padres, distancias = camino_minimo(grafo, v)

        for w in distancias:
            if distancias[w] > distancia_max and distancias[w] != math.inf:
                distancia_max = distancias[w]
                padres_camino_max = padres
                origen = v
                destino = w
            
    camino = reconstruir_camino(padres_camino_max, origen, destino)
    diametro.append(camino)
    diametro.append(distancia_max)


# pre: el grafo fue creado, las paginas pertenecen al grafo
# post: devuelve un diccionario con los grados de entrada de cada vertice
def gr_entrada(grafo, paginas):
    grado_entrada = {}
    for p in paginas:
        grado_entrada[p] = 0

    for p in paginas:
        for w in grafo.adyacentes(p):
            if w in paginas:
                grado_entrada[w] += 1
    return grado_entrada

# pre: el grafo fue creado, las paginas pertenecen al grafo
# post: devuelve un orden posible en el que pueden ser leidas las paginas. Si no existe un orden, devuelve None
def orden_lectura(grafo, paginas):
    orden = []
    grado_entrada = gr_entrada(grafo, paginas)
    q = Cola()

    for p in paginas:
        if grado_entrada[p] == 0:
            q.encolar(p)

    while not q.esta_vacia():
        p = q.desencolar()
        orden.append(p)
        for w in grafo.adyacentes(p):
            if w in paginas:
                grado_entrada[w] -= 1
                if grado_entrada[w] == 0:
                    q.encolar(w)

    if len(orden) != len(paginas): # para detectar si no se puede obtener un orden (si hay un ciclo)
        return None
    return orden

# pre: el grafo fue creado, la pagina pertenece al grafo y n es el costo del camino
# post: devuelve la cantidad de paginas que se encuentran a rango n de la pagina pasada por parametro
def rango(grafo, pagina, n):
    rango_n = 0
    padres, distancia = camino_minimo(grafo, pagina)
    for w in distancia.values():
        if w == n:
            rango_n += 1

    return rango_n
    


def _navegacion_primer_link(grafo, v_actual, cant_links, navegacion):
    if cant_links == MAX_LINKS or len(grafo.adyacentes(v_actual)) == 0:
        return
    
    primer_link = grafo.adyacentes(v_actual)[0]
    navegacion.append(primer_link)
    _navegacion_primer_link(grafo, primer_link, cant_links + 1, navegacion)

# pre: el grafo fue creado, origen pertenece al grafo
# post: devuelve una lista con las paginas a las que se pudo acceder navegando por el primer link de cada pagina
def navegacion_primer_link(grafo, origen):
    cant_links = 0
    navegacion = []
    navegacion.append(origen)
    _navegacion_primer_link(grafo, origen, cant_links, navegacion)
    
    return navegacion
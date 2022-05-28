import random

#grafo implementado con diccionario de diccionarios

class Grafo:
    def __init__(self, dirigido, pesado, lista_vertices = None):
        self.dirigido = dirigido # booleano
        self.pesado = pesado  # booleano
        self.diccionario = {}

        # inicializamos los vertices iniciales, si los hay
        if lista_vertices:
            for vertice in lista_vertices:
                self.diccionario[vertice] = {}


    # pre: -
    # post: agrega un vertice al grafo 
    def agregar_vertice(self, vertice):
        if not vertice in self.diccionario:
            self.diccionario[vertice] = {}


    # pre: -
    # post: elimina un vertice del grafo y todas las conexiones entre el mismo
    def borrar_vertice(self, vertice):
        if not vertice in self.diccionario: return

        for v in self.diccionario.keys():
            if v != vertice and vertice in self.diccionario[v]:
                (self.diccionario[v]).pop(vertice)
        
        self.diccionario.pop(vertice)


    # pre: -
    # post: agrega una arista entre el vertice1 y el vertice2. Si el grafo es no dirigido agrega la arista de vuelta, y si es pesado agrega el peso
    def agregar_arista(self, vertice1, vertice2, peso = 1):
        if not vertice1 in self.diccionario: return
        if not vertice2 in self.diccionario: return

        self.diccionario[vertice1][vertice2] = (vertice1, vertice2, peso)   
        if not self.dirigido:
            self.diccionario[vertice2][vertice1] = (vertice2, vertice1, peso)


    # pre: -
    # post: elimina la arista entre vertice1 y vertice2. Si el grafo no es dirigido, tambien elimina la arista de vuelta 
    def borrar_arista(self, vertice1, vertice2):
        if not vertice1 in self.diccionario: return
        if not vertice2 in self.diccionario: return

        if vertice2 in self.diccionario[vertice1]:
            if not self.dirigido:
                self.diccionario[vertice2].pop(vertice1)

            return self.diccionario[vertice1].pop(vertice2)
        
        
    # pre: -
    # post: retorna true si vertice1 y vertice2 estan conectados por una arista, false en caso contrario
    def son_adyacentes(self, vertice1, vertice2):
        if vertice1 not in self.diccionario: return False
        return vertice2 in self.diccionario[vertice1]
        
    
    # pre: -
    # post: retorna una lista con todos los vertices del grafo
    def obtener_vertices(self):
        lista = []
        for v in self.diccionario:
            lista.append(v)
        return lista

    # pre: -
    # post: devuelve un vertice aleatorio del grafo
    def vertice_aleatorio(self):
        return random.choice(list(self.diccionario.keys()))

    # pre: -
    # post: retorna una lista con todos los vertices que son adyacentes al vertice pasado por parametro
    def adyacentes(self, vertice):
        lista = []
        for ady in self.diccionario[vertice].keys():
            lista.append(ady)
        return lista

    # pre: -
    # post: retorna el peso de la arista entre vertice1 y vertice2
    def peso_arista(self, vertice1, vertice2):
        if not self.son_adyacentes(vertice1, vertice2):
            return None
        return self.diccionario[vertice1][vertice2][2]
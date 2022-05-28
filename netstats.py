#!/usr/bin/python3
from biblioteca import *
from grafo import Grafo
import sys

LISTAR_OPERACIONES = 'listar_operaciones'
CAMINO = 'camino'
COMUNIDAD = 'comunidad'
NAVEGACION = 'navegacion'
DIAMETRO = "diametro" 
CICLO = 'ciclo'
RANGO = 'rango'
CONECTADOS = 'conectados'
LECTURA = 'lectura'

CANT_PARAMETROS = 2
ERROR_COMANDO = "Error: comando inexistente"
ERROR_PARAMETROS = "Error: cantidad erronea de parametros"
ERROR_CAMINO = "No se encontro recorrido"
ERROR_LECTURA = "No existe forma de leer las paginas en orden"
ERROR_PAGINA_INEXISTENTE = 'Error: pagina ingresada inexistente'
ERROR_CICLO = "No se encontro recorrido"


def file_manager(ruta_archivo):
    with open(ruta_archivo, "r", encoding ='UTF-8') as archivo:
        grafo = Grafo(True, False, None)

        for l in archivo:
            linea = l.strip()
            vertices = linea.split('\t')
            grafo.agregar_vertice(vertices[0])
                
            for v in vertices[1:]:
                grafo.agregar_vertice(v)
                grafo.agregar_arista(vertices[0], v)

    return grafo


def validar_paginas(grafo, paginas):
    for i in paginas:
        if not i in grafo.obtener_vertices(): # si alguno de los parametros no existe
            return False
    return True


def validar_parametros(parametros, cant_parametros = None):
    if parametros == None and cant_parametros != None:
        return False
    
    if parametros != None and cant_parametros == None:
        return False

    if parametros != None and len(parametros) != cant_parametros:
        return False
    return True


def separar_entrada(entrada):
    parametros = entrada.split(',')

    primera_pos = parametros[0].split()
    comando = primera_pos[0]
    parametro_1 = ' '.join(primera_pos[1:])
    parametros.remove(parametros[0])
    parametros.insert(0, parametro_1)

    if parametros[0] == '':
        return comando, None
    return comando, parametros


def ejecutar_comandos(grafo, entrada, diametro, conexiones, comunidades, prueba):
    comando, parametros = separar_entrada(entrada.strip())
    
    if comando == LISTAR_OPERACIONES:
        if not validar_parametros(parametros, None):
            print(ERROR_PARAMETROS)
            return
        listar_operaciones()


    elif comando == CAMINO:
        if not validar_parametros(parametros, 2):
            print(ERROR_PARAMETROS) 
            return
        if not validar_paginas(grafo, parametros):
            print(ERROR_PAGINA_INEXISTENTE)
            return

        resultado = camino_mas_corto(grafo, parametros[0], parametros[1])
        if resultado == None:
            print(ERROR_CAMINO)
        else: imprimir_camino(resultado[0], resultado[1])


    elif comando == COMUNIDAD:
        if not validar_parametros(parametros, 1):
            print(ERROR_PARAMETROS) 
            return
        if not validar_paginas(grafo, parametros):
            print(ERROR_PAGINA_INEXISTENTE)
            return

        if len(comunidades) == 0:
            buscar_comunidades(grafo, comunidades)
        comunidad = buscar_comunidad_pagina(comunidades, parametros[0])
        imprimir_salida(comunidad)


    elif comando == CICLO:
        if not validar_parametros(parametros, 2):
            print(ERROR_PARAMETROS)
            return
        if not validar_paginas(grafo, parametros[:-1]):
            print(ERROR_PAGINA_INEXISTENTE)
            return

        ciclo_n = ciclo(grafo, parametros[0], int(parametros[1]))
        if ciclo_n == None:
            print(ERROR_CICLO)
            return
        imprimir_camino(ciclo_n, None)


    elif comando == DIAMETRO:
        if not validar_parametros(parametros, None):
            print(ERROR_PARAMETROS)
            return

        if len(diametro) == 0: 
            calcular_diametro(grafo, diametro)
        imprimir_camino(diametro[0], diametro[1])


    elif comando == CONECTADOS:
        if not validar_parametros(parametros, 1):
            print(ERROR_PARAMETROS) 
            return 
        if not validar_paginas(grafo, parametros):
            print(ERROR_PAGINA_INEXISTENTE)
            return

        if len(conexiones) == 0:
            conectividad(grafo, conexiones)

        conexion = buscar_conexion_pagina(conexiones, parametros[0])
        imprimir_salida(conexion)


    elif comando == RANGO:
        if not validar_parametros(parametros, 2):
            print(ERROR_PARAMETROS) 
            return 
        if not validar_paginas(grafo, parametros[:-1]):
            print(ERROR_PAGINA_INEXISTENTE)
            return
        rango_n = rango(grafo, parametros[0], int(parametros[1]))
        print(rango_n)


    elif comando == NAVEGACION:
        if not validar_parametros(parametros, 1):
            print(ERROR_PARAMETROS)
            return
        if parametros[0] not in grafo.obtener_vertices():
            print(ERROR_PAGINA_INEXISTENTE)
            return 
        navegacion = navegacion_primer_link(grafo, parametros[0])
        imprimir_camino(navegacion, None)


    elif comando == LECTURA:
        if not validar_paginas(grafo, parametros):
            print(ERROR_PAGINA_INEXISTENTE)

        orden = orden_lectura(grafo, parametros)
        if orden == None:
            print(ERROR_LECTURA)
            return
        imprimir_salida(orden)

    else: print(ERROR_COMANDO)


def main():
    if __name__ == "__main__": 
        if len(sys.argv) < CANT_PARAMETROS:
            print(ERROR_PARAMETROS)
            return

        archivo = sys.argv[1]
        grafo = file_manager(archivo)

        diametro = []
        prueba = []
        conexiones, comunidades = [], {}

        
        for line in sys.stdin:
            ejecutar_comandos(grafo, line, diametro, conexiones, comunidades, prueba)
        #print(grafo.adyacentes('Nueva Inglaterra'))
main()
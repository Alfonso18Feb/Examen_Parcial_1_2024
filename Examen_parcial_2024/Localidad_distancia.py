import tracemalloc
from timeit import timeit
import networkx as nx
from collections import deque
import random
import matplotlib as plt
localidades = { 
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)], 
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)], 
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)], 
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)], 
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)], 
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)], 
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)], 
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)], 
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)], 
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)] 
} 

entrada=str(input('localidad de entrada: ').title())

salida=str(input('localida que quieres salir: ').title())
tracemalloc.start()

def Ruta_mas_corta(localidades,entrada,salida):
    G=nx.Graph()
    for localidad, conexiones in localidades.items():
        for destino, peso in conexiones:
            G.add_edge(localidad, destino, weight=peso)
    pos = nx.spring_layout(G, seed=42)
    queue = deque([entrada]) #creamos una lista de los nodos que vamos cojiendo
    visited = {entrada: None} #creamos un dictionario visited donde se pondran gurdar los vecinos de cada nodo
    distancias = {entrada: 0}#almacen distancia
    while queue:# cuando a queue este llena
        current_node = queue.popleft() #llamamos a current_node el primer nodo de la lista queue
        '''
        Este bucle for recorre todas las vecindades (neighbors) para cada neighbor:
        luego vemos si NO esta vecindad(hijo de current_node) esta en el dictionario visited
        Entonces si no esta en visited añadimos a visited un dictionario:
        ((el nodo del vecino), (el nodo que estamos))
        El nodo del vecino lo añadimos a la lista queue
        
        '''
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                visited[neighbor] = current_node 
                distancias[neighbor] = distancias[current_node] + G[current_node][neighbor]['weight'] 
                queue.append(neighbor)

        if current_node == salida:#si coencide que el current nodo estamos en el nodo salida
           
            camino = []#una lista vacia donde pondremos el camino mas corto para resolver el laberinto
            '''
            En otras palabras, el bucle while va ha retroceder del dicionario visited hasta llegar al Key NONE
            Primer añadimos el current_node que seria la salida
            luego cojemos el key de la salida para ver que nodo esta conectado a la salida
            Que estos estan escritos en el dictionario visited
            Entonces vemos si esta llave Key es NONO Si not NONE
            reetimos el bucle hasta llegar a la salida
            '''
            while current_node is not None:# haces este bucle hasta llgar a la key NONE que seria la entrada.
                camino.append(current_node)#añadimos el nodo a los caminos
                current_node = visited[current_node]
            camino.reverse()  # Invertir el camino para que sea de entrada a salida
            distancia_total = distancias[salida]#la distancia total
            return camino, distancia_total

camino, distancia =Ruta_mas_corta(localidades,entrada,salida)

print(f"EL camino mas corto de {entrada} a {salida} es de {distancia} km.\nRuta mas corta es {camino}")
time_ruta_corta=timeit(Ruta_mas_corta(localidades,entrada,salida),n=10)
current, peak = tracemalloc.get_traced_memory()

print(f" \nMemoria {current} B, el pico: {peak} B")
tracemalloc.stop()


tracemalloc.start()

def Conexiones_cortas(localidades):
    conexiones_cortas = []

    # Recorrer el diccionario de localidades
    for localidad, conexiones in localidades.items():
        for destino, peso in conexiones:
            if peso <= 15:
                # Añadir la conexión si el peso es <= 15
                conexiones_cortas.append((localidad, destino, peso))

    return conexiones_cortas
print("lista de localidades cortas:\n",Conexiones_cortas(localidades))

time_Conexiones_cortas=timeit(Conexiones_cortas(localidades),n=10)
current, peak = tracemalloc.get_traced_memory()

print(f" \nMemoria {current} B, el pico: {peak} B")
tracemalloc.stop()
tracemalloc.start()


def conexion(localidades):
        # Crear un grafo vacío
    G = nx.Graph()

    # Añadir nodos y aristas con pesos al grafo
    for localidad, conexiones in localidades.items():
        for destino, peso in conexiones:
            G.add_edge(localidad, destino, weight=peso)
    if nx.is_connected(G):
        return("El grafo es conexo.")
    else:
        return("El grafo NO es conexo.")

print("¿El grafo es conexo?\n",conexion(localidades))

time_Conexiones=timeit(conexion(localidades),n=10)
current, peak = tracemalloc.get_traced_memory()
print(f"time{time_Conexiones}")
print(f" \nMemoria {current} B, el pico: {peak} B")
tracemalloc.stop()
tracemalloc.start()

def Alternativaa_rutas(localidaes,entrada, salida):
    G = nx.Graph()

    # Añadir nodos y aristas con pesos al grafo
    for localidad, conexiones in localidades.items():
        for destino, peso in conexiones:
            G.add_edge(localidad, destino, weight=peso)
    stack = [[entrada]]  # Cada elemento es una ruta parcial
    rutas_posibles = []

    while stack:
        ruta = stack.pop()  # Extraer la ruta actual de la pila
        nodo_actual = ruta[-1]  # Último nodo de la ruta

        # Si llegamos al nodo de salida, añadimos la ruta completa
        if nodo_actual == salida:
            rutas_posibles.append(ruta)
            continue

        # Explorar vecinos no visitados
        for vecino in G.neighbors(nodo_actual):
            if vecino not in ruta:  # Evitamos ciclos
                stack.append(ruta + [vecino])#añadimos el vecino a el stack 

    return rutas_posibles
print("las rutas posibles son las siguientes",Alternativaa_rutas(localidades,entrada,salida))
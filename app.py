import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import random
import pandas as pd
from IPython.display import display


def draw_graph(n, m):
    '''
    Una funcion que dibuja un grafo con n nodos y m arista.

    Parametros
    ----------
    n: int
        Numero de nodos del grafo.
    m: int
        Numero de arista del grafo.

    Retorna
    -------
    G: Grafo
        Grafo generado.
    '''

    # definir atributos de gráfico
    maximum_edges = n*(n-1)
    minimum_edges = n

    # Inicializando nuestro gráfico dirigido
    G = nx.DiGraph()

    # Agregando nodos uno tras otro de acuerdo con la entrada del usuario
    for i in range(1, n+1):
        G.add_node(i)

    # barajando nuestros nodos para que generemos los bordes aleatorios mínimos entre ellos para obtener un gráfico conectado
    random_nodes = list(random.choice(
        list(G.nodes), size=G.number_of_nodes(), replace=False))
    for i in range(len(random_nodes)):
        if random_nodes[i] != random_nodes[-1]:
            G.add_edge(random_nodes[i], random_nodes[i+1])
        else:
            G.add_edge(random_nodes[i], random_nodes[0])

    # agregando el resto de bordes aleatoriamente hasta que alcancemos el número requerido de bordes por el usuario
    while m != G.number_of_edges():
        u, v = random.choice(list(G.nodes), size=2, replace=False)
        G.add_edge(u, v)

    # matriz de distancia de impresión
    matrix = np.zeros(shape=(n, n))
    for i in range(G.number_of_nodes()):
        for j in range(G.number_of_nodes()):
            matrix[i, j] = int(nx.shortest_path_length(G, i+1, j+1))
            df = pd.DataFrame(matrix, index=range(
                1, G.number_of_nodes()+1), columns=range(1, G.number_of_nodes()+1))
    print('Distance matrix equals:')
    display(df)

    # número de impresión de bordes
    print('Number of edges equals: ', G.number_of_edges(), '\n')

    # excentricidad de impresión
    for k, v in nx.eccentricity(G).items():
        print(f'Eccentricity of node {k} equals: {v} \n')

    # diámetro de impresión
    print('Diameter of the net equals: ', nx.diameter(G), '\n')

    # suma de todas las distancias (costo de transporte)
    print('Transportation cost equals: ', np.sum(matrix), '\n')

    # Mostrando el gráfico
    plt.figure(figsize=(8, 6))
    nx.draw(G, node_size=1000, with_labels=True)
    plt.show()

    print(100*'-', '\n')
    print('Results after applying our strategy to reduce diameter and distance:\n')

    # disminución de la distancia total (agregamos nuevos bordes entre los nodos de mayor excentricidad)
    for i in list(zip(np.where(matrix == nx.diameter(G))[0], np.where(matrix == nx.diameter(G))[1])):
        G.add_edge(i[0]+1, i[1]+1)
        matrix[i] = 1

    # número de impresión de bordes
    print('Number of edges equals: ', G.number_of_edges(), '\n')

    # excentricidad de impresión
    for k, v in nx.eccentricity(G).items():
        print(f'Eccentricity of node {k} equals: {v} \n')

    # diámetro de impresión
    print('Diameter of the net equals: ', nx.diameter(G), '\n')

    # Impresión del costo de transporte después de aplicar nuestra estrategia.
    print('Transportation cost equals: ', np.sum(matrix), '\n')

    # Mostrando el gráfico
    plt.figure(figsize=(8, 6))
    nx.draw(G, node_size=1000, with_labels=True)
    plt.show()


nodes = input("Ingrese el número de nodos como un número entero: >>> ")
while not nodes.isnumeric():
    nodes = input("Ingrese el número de nodos como un número entero: >>> ")
nodes = int(nodes)

edges = input(
    f"Introduzca el número de aristas como un número entero entre {nodes} y {nodes*(nodes-1)}:>>> ")
while not edges.isnumeric() or not int(edges) in range(nodes, (nodes*(nodes-1))+1):
    edges = input(
        f"Introduzca el número de aristas como un número entero entre {nodes} and {nodes*(nodes-1)}:>>> ")

edges = int(edges)
draw_graph(nodes, edges)

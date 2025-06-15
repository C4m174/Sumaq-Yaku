import pandas as pd
import networkx as nx
from geopy.distance import geodesic

def cargar_datos():
    embalses = pd.read_csv('data/embalses_arequipa.csv')
    puntos_criticos = pd.read_csv('data/puntos_criticos_arequipa.csv')
    return embalses, puntos_criticos

def construir_grafo(embalses, puntos_criticos):
    G = nx.DiGraph()
    # Agregar nodos de embalses
    for _, row in embalses.iterrows():
        G.add_node(row['Nombre'], pos=(row['Latitud'], row['Longitud']), tipo='embalse', capacidad=row['Volumen_Almacenado_m3'])
    # Agregar nodos de puntos críticos
    for _, row in puntos_criticos.iterrows():
        G.add_node(row['Nombre'], pos=(row['Latitud'], row['Longitud']), tipo='punto_critico')
    # Agregar aristas con pesos basados en la distancia geográfica
    for embalse in embalses.itertuples():
        for punto in puntos_criticos.itertuples():
            distancia = geodesic((embalse.Latitud, embalse.Longitud), (punto.Latitud, punto.Longitud)).kilometers
            G.add_edge(embalse.Nombre, punto.Nombre, weight=distancia, capacity=embalse.Volumen_Almacenado_m3)
    return G

def ejecutar_algoritmos(region):
    embalses, puntos_criticos = cargar_datos()
    G = construir_grafo(embalses, puntos_criticos)
    rutas_optimas = {}
    flujos_maximos = {}
    for punto in puntos_criticos['Nombre']:
        try:
            ruta = nx.dijkstra_path(G, source=embalses['Nombre'][0], target=punto, weight='weight')
            rutas_optimas[punto] = ruta
        except nx.NetworkXNoPath:
            rutas_optimas[punto] = None
        try:
            flujo = nx.maximum_flow_value(G, embalses['Nombre'][0], punto, capacity='capacity')
            flujos_maximos[punto] = flujo
        except nx.NetworkXError:
            flujos_maximos[punto] = 0
    return {
    "rutas_optimas": rutas_optimas,
    "flujos_maximos": flujos_maximos
}


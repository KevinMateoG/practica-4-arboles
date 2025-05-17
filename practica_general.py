import random
from arbol_general import *
libre = "."
bloqueo = "X"
salida = "🏁"
trampa = "T"
retraso = "R"
class Laberinto:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.laberinto = self.crear_laberinto(tamaño)
        self.salida = (2,2)
        self.laberinto[self.salida[0]][self.salida[1]] = salida
        self.trampa = []
        self.bloqueo = []
        self.retraso = []
        
    def crear_laberinto(self, tamaño):
        lista = []
        for i in range(tamaño):
            lista.append([])
            for _ in range(tamaño):
                lista[i].append(libre)
        return lista
    
    def poner_elementos(self, tipo):
        print(self.posiciones_libres())
        fila = int(input())
        columna = int(input())

        if tipo == trampa:
            self.laberinto[fila][columna] = trampa
            self.trampa.append((fila,columna))
        
        if tipo == bloqueo:
            self.laberinto[fila][columna] = bloqueo
            self.bloqueo.append((fila,columna))

        if tipo == retraso:
            self.laberinto[fila][columna] = retraso
            self.retraso.append((fila,columna))
    
    def posiciones_libres(self):
        lab = self.laberinto
        libres = []
        for i in range(len(lab)):
            for j in range(len(lab)):
                if lab[i][j] == libre:
                    libres.append((i,j))
        return libres

    def __repr__(self):
        repr = ""
        for i in self.laberinto:
            repr = repr + str(i) + "\n"
        return repr

class Persona:
    def __init__(self, laberinto: Laberinto):
        self.laberinto = laberinto
        while True:
            x = random.randint(0, laberinto.tamaño-1)
            y = random.randint(0, laberinto.tamaño-1)
            if (x, y) != laberinto.salida and laberinto.laberinto[x][y] == libre:
                self.laberinto.laberinto[x][y] = "😀"
                self.posicion_inicial = (x, y)
                break
        self.perdio_direcciones = []
        self.retrasado = False
        self.historial_movimientos = GeneralTree()
        self.historial_movimientos.root = Node(self.posicion_inicial)
    
    def bfs_camino(self):
        inicio = self.posicion_inicial
        meta = self.laberinto.salida
        lab = self.laberinto.laberinto
        tamaño = self.laberinto.tamaño

        movimientos = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]

        # Eliminar movimientos perdidos por trampas
        movimientos_validos = [
            m for i, m in enumerate(movimientos)
            if i not in self.perdio_direcciones
        ]

        visitado = set()
        cola = []
        cola.append((inicio, [inicio]))  # (posición, camino)
        visitado.add(inicio)

        while cola:
            actual, camino = cola[0]
            cola = cola[1:]  # Simula popleft

            if actual == meta:
                return camino  # ruta encontrada

            for dx, dy in movimientos_validos:
                nx, ny = actual[0] + dx, actual[1] + dy

                if 0 <= nx < tamaño and 0 <= ny < tamaño:
                    if (nx, ny) not in visitado and lab[nx][ny] != "X":
                        visitado.add((nx, ny))
                        cola.append(((nx, ny), camino + [(nx, ny)]))

        return None  # no hay ruta

    def bfs_con_arbol(self):
        inicio = self.posicion_inicial
        meta = self.laberinto.salida
        lab = self.laberinto.laberinto
        tamaño = self.laberinto.tamaño

        movimientos = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        movimientos_validos = [
            m for i, m in enumerate(movimientos)
            if i not in self.perdio_direcciones
        ]

        # Creamos el árbol de rutas
        arbol = GeneralTree()
        arbol.root = Node(inicio)

        # Diccionario para relacionar posiciones con nodos
        nodos = {inicio: arbol.root}

        visitado = set()
        cola = [(inicio, [])]
        visitado.add(inicio)

        while cola:
            actual, _ = cola.pop(0)

            for dx, dy in movimientos_validos:
                nx, ny = actual[0] + dx, actual[1] + dy
                nuevo = (nx, ny)

                if 0 <= nx < tamaño and 0 <= ny < tamaño:
                    if nuevo not in visitado and lab[nx][ny] != "X":
                        visitado.add(nuevo)
                        nodo_padre = nodos[actual]
                        nodo_hijo = Node(nuevo)
                        nodo_padre.children.append(nodo_hijo)
                        nodos[nuevo] = nodo_hijo
                        cola.append((nuevo, []))
        return arbol
    
    def encontrar_camino_en_arbol(self,nodo, meta, camino_actual=[]):
        camino_actual = camino_actual + [nodo.value]

        if nodo.value == meta:
            return camino_actual

        for hijo in nodo.children:
            resultado = self.encontrar_camino_en_arbol(hijo, meta, camino_actual)
            if resultado:
                return resultado
        
        return None

lab = Laberinto(3)
lab.poner_elementos("X")
per = Persona(lab)
print(lab)
inicio = per.bfs_con_arbol()
print(per.encontrar_camino_en_arbol(inicio.root, per.laberinto.salida))
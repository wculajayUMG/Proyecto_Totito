import copy
import sys
import pygame
import random
import numpy as np
from graphviz import Digraph

# Configuración de la pantalla
ANCHO = 600
ALTO = 600

FILAS = 3
COLUMNAS = 3
TAM_CASILLA = ANCHO // COLUMNAS

GROSOR_LINEA = 15
GROSOR_CIRCULO = 15
GROSOR_CRUZ = 20

RADIO = TAM_CASILLA // 4

OFFSET = 50
COLOR_FONDO = (0, 150, 100)
COLOR_LINEA = (50, 50, 50)
COLOR_CIRCULO = (50, 50, 50)
COLOR_CRUZ = (250, 230, 250)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Juego de Tic Tac Toe')
pantalla.fill(COLOR_FONDO)

# Clases

class PrintNames:
    def __init__(self, nombres, ancho=700, alto=600):
        self.nombres = nombres
        self.ancho = ancho
        self.alto = alto
        self.titulo = "Nombres de Colaboradores del proyecto"

        pygame.init()

        self.ventana = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption('Lista de Nombres')

        self.fuente_titulo = pygame.font.SysFont('Arial', 40)
        self.fuente_nombres = pygame.font.SysFont('Arial', 30)

        self.color_fondo = (255, 255, 255)
        self.color_texto = (0, 0, 0)

    def ejecutar(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        corriendo = False

            self.ventana.fill(self.color_fondo)

            texto_titulo = self.fuente_titulo.render(self.titulo, True, self.color_texto)
            self.ventana.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 20))

            for i, nombre in enumerate(self.nombres):
                texto_nombre = self.fuente_nombres.render(nombre, True, self.color_texto)
                self.ventana.blit(texto_nombre, (50, 100 + i * 40))

            pygame.display.flip()

        pygame.quit()


class Tablero:
    def __init__(self):
        self.casillas = np.zeros((FILAS, COLUMNAS))
        self.casillas_vacias = self.casillas
        self.casillas_marcadas = 0

    def estado_final(self, mostrar=False):
        '''
        @devuelve 0 si es empate
        @devuelve 1 si jugador 1 es el ganador
        @devuelve 2 si jugador 2 es el ganador
        '''

        # Victoria vertical
        for col in range(COLUMNAS):
            if self.casillas[0][col] == self.casillas[1][col] == self.casillas[2][col] != 0:
                if mostrar:
                    color = COLOR_CIRCULO if self.casillas[0][col] == 2 else COLOR_CRUZ
                    pos_inicial = (col * TAM_CASILLA + TAM_CASILLA // 2, 20)
                    pos_final = (col * TAM_CASILLA + TAM_CASILLA // 2, ALTO - 20)
                    pygame.draw.line(pantalla, color, pos_inicial, pos_final, GROSOR_LINEA)
                return self.casillas[0][col]

        # Victoria horizontal
        for fila in range(FILAS):
            if self.casillas[fila][0] == self.casillas[fila][1] == self.casillas[fila][2] != 0:
                if mostrar:
                    color = COLOR_CIRCULO if self.casillas[fila][0] == 2 else COLOR_CRUZ
                    pos_inicial = (20, fila * TAM_CASILLA + TAM_CASILLA // 2)
                    pos_final = (ANCHO - 20, fila * TAM_CASILLA + TAM_CASILLA // 2)
                    pygame.draw.line(pantalla, color, pos_inicial, pos_final, GROSOR_LINEA)
                return self.casillas[fila][0]

        # Diagonal descendente
        if self.casillas[0][0] == self.casillas[1][1] == self.casillas[2][2] != 0:
            if mostrar:
                color = COLOR_CIRCULO if self.casillas[1][1] == 2 else COLOR_CRUZ
                pos_inicial = (20, 20)
                pos_final = (ANCHO - 20, ALTO - 20)
                pygame.draw.line(pantalla, color, pos_inicial, pos_final, GROSOR_CRUZ)
            return self.casillas[1][1]

        # Diagonal ascendente
        if self.casillas[2][0] == self.casillas[1][1] == self.casillas[0][2] != 0:
            if mostrar:
                color = COLOR_CIRCULO if self.casillas[1][1] == 2 else COLOR_CRUZ
                pos_inicial = (20, ALTO - 20)
                pos_final = (ANCHO - 20, 20)
                pygame.draw.line(pantalla, color, pos_inicial, pos_final, GROSOR_CRUZ)
            return self.casillas[1][1]

        # Empate
        return 0

    def marcar_casilla(self, fila, col, jugador):
        self.casillas[fila][col] = jugador
        self.casillas_marcadas += 1

    def casilla_vacia(self, fila, col):
        return self.casillas[fila][col] == 0

    def obtener_casillas_vacias(self):
        casillas_vacias = []
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                if self.casilla_vacia(fila, col):
                    casillas_vacias.append((fila, col))
        return casillas_vacias

    def esta_lleno(self):
        return self.casillas_marcadas == 9

    def esta_vacio(self):
        return self.casillas_marcadas == 0

class Maquina:
    def __init__(self, nivel=1, jugador=2):
        self.nivel = nivel
        self.jugador = jugador

    def aleatorio(self, tablero):
        casillas_vacias = tablero.obtener_casillas_vacias()
        idx = random.randrange(0, len(casillas_vacias))
        return casillas_vacias[idx]

    def minimax(self, tablero, maximizando):
        estado = tablero.estado_final()

        if estado == 1:
            return 1, None
        if estado == 2:
            return -1, None
        if tablero.esta_lleno():
            return 0, None

        if maximizando:
            max_eval = -100
            mejor_movimiento = None
            casillas_vacias = tablero.obtener_casillas_vacias()

            for (fila, col) in casillas_vacias:
                tablero_temporal = copy.deepcopy(tablero)
                tablero_temporal.marcar_casilla(fila, col, 1)
                evaluacion = self.minimax(tablero_temporal, False)[0]
                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_movimiento = (fila, col)

            return max_eval, mejor_movimiento

        else:
            min_eval = 100
            mejor_movimiento = None
            casillas_vacias = tablero.obtener_casillas_vacias()

            for (fila, col) in casillas_vacias:
                tablero_temporal = copy.deepcopy(tablero)
                tablero_temporal.marcar_casilla(fila, col, self.jugador)
                evaluacion = self.minimax(tablero_temporal, True)[0]
                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_movimiento = (fila, col)

            return min_eval, mejor_movimiento

    def evaluar(self, tablero_principal):
        if self.nivel == 0:
            evaluacion = 'aleatorio'
            movimiento = self.aleatorio(tablero_principal)
        else:
            evaluacion, movimiento = self.minimax(tablero_principal, False)

        print(f'La máquina ha elegido marcar el cuadro en la posición {movimiento} con una evaluación de: {evaluacion}')
        return movimiento

class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.maquina = Maquina()
        self.jugador = 1
        self.modo_juego = 'maquina'
        self.en_juego = True
        self.mostrar_lineas()
        self.arbol = Digraph(comment='Jugadas de Tic Tac Toe')
        self.arbol.graph_attr['ranksep'] = '1.5'
        self.arbol.graph_attr['nodesep'] = '0.5'
        self.arbol.graph_attr['splines'] = 'true'
        self.estado_actual = str(self.tablero.casillas)
        self.arbol.node(self.estado_actual, self.estado_actual)

    def mostrar_lineas(self):
        pantalla.fill(COLOR_FONDO)
        pygame.draw.line(pantalla, COLOR_LINEA, (TAM_CASILLA, 0), (TAM_CASILLA, ALTO), GROSOR_LINEA)
        pygame.draw.line(pantalla, COLOR_LINEA, (ANCHO - TAM_CASILLA, 0), (ANCHO - TAM_CASILLA, ALTO), GROSOR_LINEA)
        pygame.draw.line(pantalla, COLOR_LINEA, (0, TAM_CASILLA), (ANCHO, TAM_CASILLA), GROSOR_LINEA)
        pygame.draw.line(pantalla, COLOR_LINEA, (0, ALTO - TAM_CASILLA), (ANCHO, ALTO - TAM_CASILLA), GROSOR_LINEA)

    def dibujar_figura(self, fila, col):
        if self.jugador == 1:
            inicio_desc = (col * TAM_CASILLA + OFFSET, fila * TAM_CASILLA + OFFSET)
            fin_desc = (col * TAM_CASILLA + TAM_CASILLA - OFFSET, fila * TAM_CASILLA + TAM_CASILLA - OFFSET)
            pygame.draw.line(pantalla, COLOR_CRUZ, inicio_desc, fin_desc, GROSOR_CRUZ)

            inicio_asc = (col * TAM_CASILLA + OFFSET, fila * TAM_CASILLA + TAM_CASILLA - OFFSET)
            fin_asc = (col * TAM_CASILLA + TAM_CASILLA - OFFSET, fila * TAM_CASILLA + OFFSET)
            pygame.draw.line(pantalla, COLOR_CRUZ, inicio_asc, fin_asc, GROSOR_CRUZ)
        elif self.jugador == 2:
            centro = (col * TAM_CASILLA + TAM_CASILLA // 2, fila * TAM_CASILLA + TAM_CASILLA // 2)
            pygame.draw.circle(pantalla, COLOR_CIRCULO, centro, RADIO, GROSOR_CIRCULO)

    def hacer_movimiento(self, fila, col):
        self.tablero.marcar_casilla(fila, col, self.jugador)
        self.dibujar_figura(fila, col)
        self.actualizar_arbol(fila, col)
        self.siguiente_turno()

    def siguiente_turno(self):
        self.jugador = self.jugador % 2 + 1

    def cambiar_modo_juego(self):
        self.modo_juego = 'maquina' if self.modo_juego == 'persona' else 'persona'

    def terminado(self):
        return self.tablero.estado_final(mostrar=True) != 0 or self.tablero.esta_lleno()

    def reiniciar(self):
        self.__init__()

    def actualizar_arbol(self, fila, col):
        nuevo_estado = str(self.tablero.casillas)
        movimiento = f"({fila},{col})"
        self.arbol.node(nuevo_estado, nuevo_estado)
        self.arbol.edge(self.estado_actual, nuevo_estado, label=movimiento)
        self.estado_actual = nuevo_estado

        # Agregar todas las jugadas posibles para la máquina en el próximo turno
        if self.jugador == self.maquina.jugador:
            posibles_movimientos = self.tablero.obtener_casillas_vacias()
            for mov in posibles_movimientos:
                tablero_temporal = copy.deepcopy(self.tablero)
                tablero_temporal.marcar_casilla(mov[0], mov[1], self.jugador)
                estado_futuro = str(tablero_temporal.casillas)
                movimiento = f"({mov[0]},{mov[1]})"
                self.arbol.node(estado_futuro, estado_futuro)
                self.arbol.edge(nuevo_estado, estado_futuro, label=movimiento)

def main():
    nombres = ['9490-22-1157 Josue Sebastian Mancilla González', '9490-22-958  Anthony Fabian Ramires Orellana', '9490-22-4974 Oscar José Cojulún Mendoza', '9490-22-3432 Willy Estuardo Culajay Asturias']
    juego = Juego()
    tablero = juego.tablero
    maquina = juego.maquina

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_g:
                    juego.cambiar_modo_juego()
                if evento.key == pygame.K_r:
                    juego.arbol.render('arbol_de_juego', view=True, format='svg', cleanup=True)
                    juego.reiniciar()
                    tablero = juego.tablero
                    maquina = juego.maquina
                if evento.key == pygame.K_0:
                    maquina.nivel = 0
                if evento.key == pygame.K_1:
                    maquina.nivel = 1
                if evento.key == pygame.K_n:
                    PrintNames(nombres).ejecutar()


            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = evento.pos
                fila = pos[1] // TAM_CASILLA
                col = pos[0] // TAM_CASILLA

                if tablero.casilla_vacia(fila, col) and juego.en_juego:
                    juego.hacer_movimiento(fila, col)
                    if juego.terminado():
                        juego.en_juego = False

        if juego.modo_juego == 'maquina' and juego.jugador == maquina.jugador and juego.en_juego:
            pygame.display.update()
            fila, col = maquina.evaluar(tablero)
            juego.hacer_movimiento(fila, col)
            if juego.terminado():
                juego.en_juego = False

        pygame.display.update()

main()
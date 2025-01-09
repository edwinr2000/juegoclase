import pygame
import random
import sys

# Inicializar PyGame
pygame.init()

# Configuración básica
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Atacando enemigos by Edwin Torres Rincón")
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

reloj = pygame.time.Clock()

# Variables globales
frecuencia_enemigos = 120
nombre_jugador = ""

# Función para mostrar texto en pantalla
def mostrar_texto(texto, tamaño, x, y, color=BLANCO, centrado=True):
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(x, y)) if centrado else superficie_texto.get_rect(topleft=(x, y))
    pantalla.blit(superficie_texto, rect_texto)

# Menú inicial
def menu_inicio():
    global frecuencia_enemigos, nombre_jugador
    ejecutando_menu = True
    entrada = ""
    dificultad_seleccionada = "Fácil"

    botones_dificultad = {
        "Fácil": pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 100, 100, 50),
        "Medio": pygame.Rect(ANCHO // 2, ALTO // 2 + 100, 100, 50),
        "Difícil": pygame.Rect(ANCHO // 2 + 150, ALTO // 2 + 100, 100, 50),
    }

    while ejecutando_menu:
        pantalla.fill(NEGRO)

        mostrar_texto("Bienvenido al juego", 74, ANCHO // 2, ALTO // 4)
        mostrar_texto("Ingresa tu nombre:", 36, ANCHO // 2, ALTO // 2 - 50)
        mostrar_texto(entrada, 36, ANCHO // 2, ALTO // 2)

        for nivel, rect in botones_dificultad.items():
            color = AZUL if nivel == dificultad_seleccionada else BLANCO
            pygame.draw.rect(pantalla, color, rect, 2)
            mostrar_texto(nivel, 24, rect.centerx, rect.centery, color)

        mostrar_texto("Presiona Enter para iniciar", 36, ANCHO // 2, ALTO // 2 + 200)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and entrada.strip():
                    nombre_jugador = entrada
                    ejecutando_menu = False
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                elif evento.unicode.isalnum():
                    entrada += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                for nivel, rect in botones_dificultad.items():
                    if rect.collidepoint(pos_mouse):
                        dificultad_seleccionada = nivel
                        if nivel == "Fácil":
                            frecuencia_enemigos = 120
                        elif nivel == "Medio":
                            frecuencia_enemigos = 60
                        elif nivel == "Difícil":
                            frecuencia_enemigos = 30

        pygame.display.flip()
        reloj.tick(30)

# Juego principal
def juego():
    global frecuencia_enemigos
    posicion_jugador = [ANCHO // 2, ALTO - 100]
    velocidad_jugador = 7
    tamaño_nave = 50
    balas = []
    enemigos = []
    velocidad_bala = 5
    velocidad_enemigos = 2
    vidas = 5
    puntaje = 0

    contador_frames = 0
    corriendo = True

    while corriendo:
        pantalla.fill(NEGRO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                balas.append([posicion_jugador[0], posicion_jugador[1]])

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and posicion_jugador[0] > 0:
            posicion_jugador[0] -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and posicion_jugador[0] < ANCHO:
            posicion_jugador[0] += velocidad_jugador

        contador_frames += 1
        if contador_frames >= frecuencia_enemigos:
            enemigos.append([random.randint(0, ANCHO - 50), 0])
            contador_frames = 0

        for bala in balas[:]:
            bala[1] -= velocidad_bala
            if bala[1] < 0:
                balas.remove(bala)

        for enemigo in enemigos[:]:
            enemigo[1] += velocidad_enemigos
            if enemigo[1] > ALTO:
                enemigos.remove(enemigo)
                vidas -= 1

        # Verificar colisiones entre balas y enemigos
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if (
                    enemigo[0] < bala[0] < enemigo[0] + 50
                    and enemigo[1] < bala[1] < enemigo[1] + 50
                ):
                    balas.remove(bala)
                    enemigos.remove(enemigo)
                    puntaje += 10

        # Verificar colisión entre enemigos y jugador
        for enemigo in enemigos[:]:
            if (
                enemigo[0] < posicion_jugador[0] + tamaño_nave // 2
                and enemigo[0] + 50 > posicion_jugador[0] - tamaño_nave // 2
                and enemigo[1] < posicion_jugador[1] + tamaño_nave
                and enemigo[1] + 50 > posicion_jugador[1]
            ):
                enemigos.remove(enemigo)
                vidas -= 1

        for bala in balas:
            pygame.draw.rect(pantalla, AZUL, (*bala, 10, 20))
        for enemigo in enemigos:
            pygame.draw.rect(pantalla, ROJO, (*enemigo, 50, 50))
        pygame.draw.polygon(
            pantalla,
            BLANCO,
            [
                (posicion_jugador[0], posicion_jugador[1]),
                (posicion_jugador[0] - tamaño_nave // 2, posicion_jugador[1] + tamaño_nave),
                (posicion_jugador[0] + tamaño_nave // 2, posicion_jugador[1] + tamaño_nave),
            ],
        )

        mostrar_texto(f"Jugador: {nombre_jugador}", 36, 10, 10, centrado=False)
        mostrar_texto(f"Vidas: {vidas}", 36, 10, 50, centrado=False)
        mostrar_texto(f"Puntaje: {puntaje}", 36, 10, 90, centrado=False)

        if vidas <= 0:
            pantalla.fill(NEGRO)
            mostrar_texto("GAME OVER", 74, ANCHO // 2, ALTO // 2 - 50)
            mostrar_texto("Haz clic para reiniciar", 36, ANCHO // 2, ALTO // 2 + 50)
            pygame.display.flip()
            esperar_reinicio()
            return

        pygame.display.flip()
        reloj.tick(60)

def esperar_reinicio():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                return

while True:
    menu_inicio()
    juego()

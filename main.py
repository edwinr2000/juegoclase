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

# Variables del juego
posicion_jugador = [ANCHO // 2, ALTO - 100]
velocidad_jugador = 7
tamaño_nave = 100  # Este es el tamaño definido para la nave del jugador
balas = []
enemigos = []
velocidad_bala = 5
velocidad_enemigos = 2 
frecuencia_enemigos = 60  # Un enemigo nuevo cada segundo
vidas = 3  # Vidas del jugador, cuando lleguen a cero el juego terminó
puntaje = 0  # Puntaje del jugador

# Funciones
def disparar_bala():
    """Crear una bala en la posición del jugador."""
    balas.append([posicion_jugador[0] + tamaño_nave // 2 - 5, posicion_jugador[1]])

def generar_enemigo():
    """Generar un enemigo en una posición aleatoria en la parte superior."""
    x_aleatoria = random.randint(0, ANCHO - 50)
    enemigos.append([x_aleatoria, 0])

# Bucle principal
contador_frames = 0
while True:
    pantalla.fill(NEGRO)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            disparar_bala()

    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and posicion_jugador[0] > 0:
        posicion_jugador[0] -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and posicion_jugador[0] < ANCHO - tamaño_nave:
        posicion_jugador[0] += velocidad_jugador

    # Generar enemigos
    contador_frames += 1
    if contador_frames >= frecuencia_enemigos:
        generar_enemigo()
        contador_frames = 0

    # Mover balas
    for bala in balas[:]:
        bala[1] -= velocidad_bala
        if bala[1] < 0:
            balas.remove(bala)

    # Mover enemigos
    for enemigo in enemigos[:]:
        enemigo[1] += velocidad_enemigos
        if enemigo[1] > ALTO:
            enemigos.remove(enemigo)
            vidas -= 1  # Perder una vida si un enemigo llega al final
        elif (
            enemigo[0] < posicion_jugador[0] + tamaño_nave
            and enemigo[0] + 50 > posicion_jugador[0]
            and enemigo[1] < posicion_jugador[1] + 50
            and enemigo[1] + 50 > posicion_jugador[1]
        ):
            enemigos.remove(enemigo)  # Colisión con el jugador
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

    # Dibujar jugador, balas y enemigos
    pygame.draw.rect(pantalla, BLANCO, (*posicion_jugador, tamaño_nave, 50))
    for bala in balas:
        pygame.draw.rect(pantalla, AZUL, (*bala, 10, 20))
    for enemigo in enemigos:
        pygame.draw.rect(pantalla, ROJO, (*enemigo, 50, 50))

    # Mostrar puntaje y vidas
    fuente = pygame.font.Font(None, 36)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntaje, (10, 50))

    # Verificar si el juego terminó
    if vidas <= 0:
        pantalla.fill(NEGRO)
        fuente_grande = pygame.font.Font(None, 74)
        texto = fuente_grande.render("¡Lo siento, el juego ha terminado!", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - 200, ALTO // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

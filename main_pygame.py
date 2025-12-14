import pygame
import sys
import time
import math
import os

from states import *
from flight_game import FlightGame

# -------------------------
# CONFIGURACIÓN GENERAL
# -------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

PULSOS_POR_CREDITO = 5

OBJETIVO_SEGUNDOS = 10
DIFICULTAD = "MEDIA"   # FACIL | MEDIA | DIFICIL

# -------------------------
# INIT PYGAME
# -------------------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mantén la Altura")
clock = pygame.time.Clock()

# -------------------------
# RUTAS DE SONIDO
# -------------------------
BASE_DIR = os.path.dirname(__file__)
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

def load_sound(name):
    path = os.path.join(SOUND_DIR, name)
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None

# Sonidos
sound_coin = load_sound("coin.wav")
sound_win = load_sound("win.wav")
sound_lose = load_sound("lose.wav")

# Música
music_path = os.path.join(SOUND_DIR, "music.wav")

# -------------------------
# FUENTES
# -------------------------
font_big = pygame.font.SysFont(None, 96)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)

# -------------------------
# COLORES
# -------------------------
BG_COLOR = (15, 15, 20)
SHIP_COLOR = (240, 240, 240)
OBSTACLE_COLOR = (200, 80, 80)
SAFE_COLOR = (80, 200, 120)
TEXT_COLOR = (230, 230, 230)
HIGHLIGHT = (240, 220, 120)

# -------------------------
# ESTADO
# -------------------------
estado = ESPERANDO
juego = None

# -------------------------
# CRÉDITOS
# -------------------------
pulsos = 0
credito_disponible = False

# -------------------------
# TIEMPO
# -------------------------
ultimo_tiempo = time.time()

# -------------------------
# ANIMACIONES
# -------------------------
pulse_timer = 0.0
float_timer = 0.0
win_timer = 0.0
lose_timer = 0.0

# Flags para evitar repetir sonidos
sonido_win_played = False
sonido_lose_played = False
musica_activa = False

# -------------------------
# MODO SERVICIO
# -------------------------
service_index = 0
service_items = ["TIEMPO", "DIFICULTAD", "SALIR"]
tiempos = [5, 10, 15]
dificultades = ["FACIL", "MEDIA", "DIFICIL"]

# -------------------------
# FUNCIONES AUX
# -------------------------
def aplicar_dificultad(juego):
    if DIFICULTAD == "FACIL":
        juego.gravedad = 0.35
        juego.hueco_altura = 240
    elif DIFICULTAD == "MEDIA":
        juego.gravedad = 0.45
        juego.hueco_altura = 200
    elif DIFICULTAD == "DIFICIL":
        juego.gravedad = 0.55
        juego.hueco_altura = 160

def iniciar_musica():
    global musica_activa
    if not musica_activa and os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        musica_activa = True

def detener_musica():
    global musica_activa
    if musica_activa:
        pygame.mixer.music.stop()
        musica_activa = False

# -------------------------
# LOOP PRINCIPAL
# -------------------------
running = True
while running:
    clock.tick(FPS)
    ahora = time.time()
    dt = ahora - ultimo_tiempo
    ultimo_tiempo = ahora

    pulse_timer += dt * 2.5
    float_timer += dt

    # Música según estado
    if estado in (ESPERANDO, SERVICIO):
        iniciar_musica()
    else:
        detener_musica()

    # -------------------------
    # EVENTOS
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # -------- ESPERANDO CRÉDITO --------
            if estado == ESPERANDO:

                # Pulso moneda
                if event.key == pygame.K_c:
                    if not credito_disponible:
                        pulsos += 1
                        if sound_coin:
                            sound_coin.play()

                        if pulsos >= PULSOS_POR_CREDITO:
                            credito_disponible = True
                            pulsos = PULSOS_POR_CREDITO

                elif event.key == pygame.K_s:
                    estado = SERVICIO

                elif event.key == pygame.K_SPACE and credito_disponible:
                    credito_disponible = False
                    pulsos = 0
                    sonido_win_played = False
                    sonido_lose_played = False

                    juego = FlightGame(OBJETIVO_SEGUNDOS)
                    aplicar_dificultad(juego)
                    estado = JUGANDO

            # -------- SERVICIO --------
            elif estado == SERVICIO:
                if event.key == pygame.K_DOWN:
                    service_index = (service_index + 1) % len(service_items)
                elif event.key == pygame.K_UP:
                    service_index = (service_index - 1) % len(service_items)
                elif event.key == pygame.K_RETURN:
                    item = service_items[service_index]

                    if item == "TIEMPO":
                        i = tiempos.index(OBJETIVO_SEGUNDOS)
                        OBJETIVO_SEGUNDOS = tiempos[(i + 1) % len(tiempos)]

                    elif item == "DIFICULTAD":
                        i = dificultades.index(DIFICULTAD)
                        DIFICULTAD = dificultades[(i + 1) % len(dificultades)]

                    elif item == "SALIR":
                        estado = ESPERANDO

    boton = pygame.key.get_pressed()[pygame.K_SPACE]

    # -------------------------
    # LÓGICA DE JUEGO
    # -------------------------
    if estado == JUGANDO:
        juego.actualizar(boton, dt)

        if not juego.vivo:
            estado = PERDISTE
            lose_timer = 0.0
            if sound_lose and not sonido_lose_played:
                sound_lose.play()
                sonido_lose_played = True

        elif juego.gano():
            estado = GANASTE
            win_timer = 0.0
            if sound_win and not sonido_win_played:
                sound_win.play()
                sonido_win_played = True

    if estado == GANASTE:
        win_timer += dt
        if win_timer > 1.5:
            estado = ESPERANDO
            juego = None

    elif estado == PERDISTE:
        lose_timer += dt
        if lose_timer > 1.2:
            estado = ESPERANDO
            juego = None

    # -------------------------
    # DIBUJO
    # -------------------------
    screen.fill(BG_COLOR)

    if estado == ESPERANDO:
        alpha = int((math.sin(pulse_timer) * 0.5 + 0.5) * 255)
        offset = int(math.sin(float_timer) * 8)

        titulo = font_medium.render("MANTÉN LA ALTURA", True, TEXT_COLOR)
        screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, 220 + offset)))

        if credito_disponible:
            texto = font_small.render("PRESIONA ESPACIO", True, SAFE_COLOR)
        else:
            texto = font_small.render(
                f"INSERTA CRÉDITO ({pulsos}/{PULSOS_POR_CREDITO})",
                True,
                TEXT_COLOR
            )

        texto.set_alpha(alpha)
        screen.blit(texto, texto.get_rect(center=(WIDTH//2, 310)))

        pygame.draw.circle(screen, SAFE_COLOR, (WIDTH//2, 360), 18, 2)

        info = font_small.render("C = MONEDA   S = SERVICIO", True, TEXT_COLOR)
        screen.blit(info, info.get_rect(center=(WIDTH//2, 420)))

    elif estado == SERVICIO:
        screen.blit(font_medium.render("MODO SERVICIO", True, TEXT_COLOR), (WIDTH//2 - 150, 120))

        for i, item in enumerate(service_items):
            color = HIGHLIGHT if i == service_index else TEXT_COLOR
            texto = item

            if item == "TIEMPO":
                texto += f": {OBJETIVO_SEGUNDOS}s"
            elif item == "DIFICULTAD":
                texto += f": {DIFICULTAD}"

            screen.blit(font_small.render(texto, True, color), (WIDTH//2 - 120, 220 + i * 50))

        screen.blit(font_small.render("↑ ↓ navegar | ENTER cambiar", True, TEXT_COLOR), (WIDTH//2 - 180, 450))

    elif estado == JUGANDO:
        hueco_top = int(juego.hueco_centro - juego.hueco_altura / 2)
        hueco_bottom = int(juego.hueco_centro + juego.hueco_altura / 2)

        pygame.draw.rect(screen, OBSTACLE_COLOR, (0, 0, WIDTH, hueco_top))
        pygame.draw.rect(screen, OBSTACLE_COLOR, (0, hueco_bottom, WIDTH, HEIGHT))

        pygame.draw.circle(screen, SHIP_COLOR, (WIDTH//2, int(juego.y)), 12)

        tiempo = font_small.render(
            f"{juego.tiempo_vivo:04.1f}s / {OBJETIVO_SEGUNDOS}s",
            True, TEXT_COLOR
        )
        screen.blit(tiempo, (20, 20))

    elif estado == GANASTE:
        scale = min(1.4, 0.8 + win_timer * 1.2)
        pulse = math.sin(win_timer * 6) * 8

        texto = font_big.render("🏆 GANASTE", True, SAFE_COLOR)
        texto = pygame.transform.scale(
            texto,
            (int(texto.get_width() * scale), int(texto.get_height() * scale))
        )
        screen.blit(texto, texto.get_rect(center=(WIDTH//2, 240 + pulse)))

    elif estado == PERDISTE:
        shake = int(math.sin(lose_timer * 40) * 12 * max(0, 1 - lose_timer * 2))
        texto = font_big.render("❌ PERDISTE", True, OBSTACLE_COLOR)
        screen.blit(texto, texto.get_rect(center=(WIDTH//2 + shake, 240)))

    pygame.display.flip()

pygame.quit()
sys.exit()


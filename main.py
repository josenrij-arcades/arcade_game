from coin import CoinAcceptor
from game import DodgeGame
from states import *

# -------------------------
# CONFIGURACIÓN GENERAL
# -------------------------
PULSOS_POR_CREDITO = 5
MODO_TEST = True   # 🔧 CAMBIA A False PARA JUEGO REAL

coin = CoinAcceptor(pulses_per_credit=PULSOS_POR_CREDITO)
estado = ESPERANDO
juego = None

print("🎮 Máquina Arcade (modo software)")
print(f"Pulsos por crédito: {PULSOS_POR_CREDITO}")
print(f"Modo test: {'ACTIVO' if MODO_TEST else 'DESACTIVADO'}")
print("Presiona 'c' para insertar moneda")
print("Ctrl + C para salir\n")

try:
    while True:

        # -------------------------
        # ESPERANDO MONEDAS
        # -------------------------
        if estado == ESPERANDO:
            tecla = input("> ").lower()

            if tecla == "c":
                if coin.pulse():
                    juego = DodgeGame(modo_test=MODO_TEST)
                    estado = JUGANDO
                    print("\n🎮 JUEGO INICIADO\n")

        # -------------------------
        # JUGANDO
        # -------------------------
        elif estado == JUGANDO:
            if not juego.jugar_ronda():
                print("\n❌ PERDISTE – FIN DEL JUEGO\n")
                estado = ESPERANDO
                juego = None
                continue

            if juego.aciertos >= juego.objetivo:
                estado = GANASTE

        # -------------------------
        # GANASTE
        # -------------------------
        elif estado == GANASTE:
            print("\n🏆 GANASTE EL PREMIO 🎁\n")
            estado = ESPERANDO
            juego = None

except KeyboardInterrupt:
    print("\nSaliendo del sistema arcade...")


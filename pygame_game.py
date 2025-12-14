import time
import random

class PygameRound:
    def __init__(self, game):
        self.game = game
        self.numero = random.randint(1, 9)
        self.inicio = time.time()
        self.tiempo_limite = game.tiempo_actual()

        self.finalizada = False
        self.resultado = None          # True / False
        self.timeout_flag = False      # diferencia timeout vs error

        # Feedback visual
        self.feedback_time = 0.3       # segundos
        self.feedback_start = None

    def tiempo_restante(self):
        restante = self.tiempo_limite - (time.time() - self.inicio)
        return max(0, restante)

    def procesar_tecla(self, tecla):
        if self.finalizada:
            return

        # 🔒 Lock inmediato (evita doble input)
        self.finalizada = True
        self.feedback_start = time.time()

        if str(tecla) == str(self.numero):
            self.game.aciertos += 1
            self.resultado = True
        else:
            self.resultado = False

    def timeout(self):
        if self.finalizada:
            return False

        if self.tiempo_restante() <= 0:
            self.finalizada = True
            self.resultado = False
            self.timeout_flag = True
            self.feedback_start = time.time()
            return True

        return False


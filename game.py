import time
import random
import sys
import select

class DodgeGame:
    def __init__(self, objetivo=15, modo_test=False):
        self.aciertos = 0
        self.objetivo = objetivo
        self.modo_test = modo_test

        if self.modo_test:
            # ===== MODO TEST (MUY LENTO Y AMIGABLE) =====
            self.tiempos_nivel = [
                5.0,  # exageradamente lento
                4.0,
                3.0,
                2.5,
                2.0,
                1.5
            ]
            self.cada_n = 5  # sube de nivel muy lento

        else:
            # ===== MODO NORMAL (ARCADE REAL) =====
            self.tiempos_nivel = [
                1.70,
                1.35,
                1.10,
                0.90,
                0.75,
                0.60
            ]
            self.cada_n = 3

    def tiempo_actual(self):
        nivel = self.aciertos // self.cada_n
        nivel = min(nivel, len(self.tiempos_nivel) - 1)
        return self.tiempos_nivel[nivel]

    def jugar_ronda(self):
        numero_objetivo = random.randint(1, 9)
        tiempo_limite = self.tiempo_actual()

        print(f"\n🎯 Presiona el número: {numero_objetivo}")
        print(f"⏱️  Tiempo máximo: {tiempo_limite:.2f} segundos")

        inicio = time.time()

        while True:
            if time.time() - inicio > tiempo_limite:
                print("💥 Muy lento")
                return False

            if self._input_disponible():
                tecla = input().strip()

                if tecla == str(numero_objetivo):
                    self.aciertos += 1
                    print(f"✅ Correcto ({self.aciertos}/{self.objetivo})")
                    return True
                else:
                    print(f"❌ Incorrecto (era {numero_objetivo})")
                    return False

            time.sleep(0.005)

    def _input_disponible(self):
        return select.select([sys.stdin], [], [], 0)[0]


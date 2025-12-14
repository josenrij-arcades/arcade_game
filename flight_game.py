import random

class FlightGame:
    def __init__(self, objetivo_segundos=25):
        # Nave
        self.y = 300
        self.velocidad = 0.0

        # Física
        self.gravedad = 0.45
        self.empuje = -0.9

        # Hueco
        self.hueco_centro = 300
        self.hueco_altura = 200
        self.hueco_velocidad = 25  # px por segundo

        # Límites
        self.top = 80
        self.bottom = 520

        # Estado
        self.vivo = True
        self.tiempo_vivo = 0.0
        self.objetivo = objetivo_segundos

        self._direccion_hueco = random.choice([-1, 1])

    def actualizar(self, boton_presionado, dt):
        if not self.vivo:
            return

        # ---- Dificultad progresiva ----
        self.gravedad += 0.002 * dt
        self.hueco_altura = max(90, self.hueco_altura - 3 * dt)

        # ---- Movimiento hueco ----
        self.hueco_centro += self._direccion_hueco * self.hueco_velocidad * dt
        if self.hueco_centro < self.top + self.hueco_altura / 2:
            self._direccion_hueco = 1
        elif self.hueco_centro > self.bottom - self.hueco_altura / 2:
            self._direccion_hueco = -1

        # ---- Física nave ----
        self.velocidad += self.gravedad
        if boton_presionado:
            self.velocidad += self.empuje

        self.y += self.velocidad

        # ---- Colisiones ----
        hueco_top = self.hueco_centro - self.hueco_altura / 2
        hueco_bottom = self.hueco_centro + self.hueco_altura / 2

        if self.y < hueco_top or self.y > hueco_bottom:
            self.vivo = False

        # ---- Tiempo ----
        if self.vivo:
            self.tiempo_vivo += dt

    def gano(self):
        return self.tiempo_vivo >= self.objetivo


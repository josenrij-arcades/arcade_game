class ServiceMenu:
    def __init__(self, objetivo=15, modo_test=True):
        self.objetivo = objetivo
        self.modo_test = modo_test
        self.opcion = 0

        self.opciones = [
            "Objetivo",
            "Modo Test",
            "Salir"
        ]

    def siguiente(self):
        self.opcion = (self.opcion + 1) % len(self.opciones)

    def anterior(self):
        self.opcion = (self.opcion - 1) % len(self.opciones)

    def seleccionar(self):
        opcion = self.opciones[self.opcion]

        if opcion == "Objetivo":
            self.objetivo += 1
            if self.objetivo > 20:
                self.objetivo = 10

        elif opcion == "Modo Test":
            self.modo_test = not self.modo_test

        elif opcion == "Salir":
            return "SALIR"

        return None


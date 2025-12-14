class RewardSystem:
    def __init__(self):
        self.total_juegos = 0
        self.premios_entregados = 0

    def evaluar(self, aciertos, objetivo):
        self.total_juegos += 1

        if aciertos >= objetivo:
            self.premios_entregados += 1
            return True   # GANÓ PREMIO

        return False      # NO GANÓ


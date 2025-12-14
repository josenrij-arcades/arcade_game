class CoinAcceptor:
    def __init__(self, pulses_per_credit=5):
        self.pulses = 0
        self.pulses_per_credit = pulses_per_credit

    def pulse(self):
        self.pulses += 1
        print(f"Pulso detectado ({self.pulses}/{self.pulses_per_credit})")

        if self.pulses >= self.pulses_per_credit:
            self.pulses = 0
            print("💰 CRÉDITO LISTO")
            return True

        return False


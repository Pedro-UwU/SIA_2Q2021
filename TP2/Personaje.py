import math
from dataclasses import dataclass, field

from armamentos.Bota import Bota
from armamentos.Guante import Guante
from armamentos.Pechera import Pechera
from armamentos.Casco import Casco
from armamentos.Arma import Arma

from clases.Clase import Clase


@dataclass(frozen=True)
class Personaje():
    clase: Clase = field()
    altura: float = field()
    bota: Bota = field()
    casco: Casco = field()
    guante: Guante = field()
    pechera: Pechera = field()
    arma: Arma = field()

    def atm(self):
        base = 3 * self.altura - 5
        return 0.7 - math.pow(base, 4) + math.pow(base, 2) + (self.altura / 4)

    def dem(self):
        base = 2.5 * self.altura - 4.16
        return 1.9 + math.pow(base, 4) - math.pow(base, 2) - ((3 * self.altura) / 10)

    def ataque(self):
        return (self.agilidad() + self.pericia()) * self.fuerza() * self.atm()

    def defensa(self):
        return (self.resistencia() + self.pericia()) * self.vida() * self.dem()

    def fuerza(self):
        return 100 * math.tanh(0.01 * (self.bota.fuerza + self.casco.fuerza + self.guante.fuerza + self.pechera.fuerza + self.arma.fuerza))

    def agilidad(self):
        return math.tanh(0.01 * (self.bota.agilidad + self.casco.agilidad + self.guante.agilidad + self.pechera.agilidad + self.arma.agilidad))

    def pericia(self):
        return 0.6 * math.tanh(0.01 * (self.bota.pericia + self.casco.pericia + self.guante.pericia + self.pechera.pericia + self.arma.pericia))

    def resistencia(self):
        return math.tanh(0.01 * (self.bota.resistencia + self.casco.resistencia + self.guante.resistencia + self.pechera.resistencia + self.arma.resistencia))

    def vida(self):
        return 100 * math.tanh(0.01 * (self.bota.vida + self.casco.vida + self.guante.vida + self.pechera.vida + self.arma.vida))
from dataclasses import dataclass, field

from clases.Clase import Clase

@dataclass(frozen=True)
class Guerrero(Clase):
    attack_constant: float = 0.6
    defense_constant: float = 0.6


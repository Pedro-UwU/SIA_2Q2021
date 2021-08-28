from dataclasses import dataclass, field

from clases.Clase import Clase

@dataclass(frozen=True)
class Arquero(Clase):
    attack_constant: float = 0.9
    defense_constant: float = 0.1


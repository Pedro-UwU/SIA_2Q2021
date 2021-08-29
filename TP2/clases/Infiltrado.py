from dataclasses import dataclass, field

from clases.Clase import Clase

@dataclass(frozen=True)
class Infiltrado(Clase):
    attack_constant: float = 0.8
    defense_constant: float = 0.3


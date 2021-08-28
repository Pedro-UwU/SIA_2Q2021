from dataclasses import dataclass, field

from clases.Clase import Clase


@dataclass(frozen=True)
class Defensor(Clase):
    attack_constant: float = 0.3
    defense_constant: float = 0.8

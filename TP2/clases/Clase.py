from dataclasses import dataclass, field

@dataclass(frozen=True)
class Clase:
    attack_constant: float = field()
    defense_constant: float = field()
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Armamento:
    fuerza: float = field()
    agilidad: float = field()
    pericia: float = field()
    resistencia: float = field()
    vida: float = field()

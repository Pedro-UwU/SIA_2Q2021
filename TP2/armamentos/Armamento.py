from dataclasses import dataclass, field


@dataclass(frozen=True)
class Armamento:
    id: int = field()
    tipo: str = field()
    fuerza: float = field()
    agilidad: float = field()
    pericia: float = field()
    resistencia: float = field()
    vida: float = field()

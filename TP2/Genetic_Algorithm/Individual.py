from dataclasses import dataclass, field

from Personaje import Personaje


@dataclass(frozen=False)
class Individual:
    player: Personaje = field()
    fitness: float = field(default=0, init=False)

    def calc_fitness(self) -> None:
        a = self.player.clase.attack_constant
        b = self.player.clase.defense_constant
        atq = self.player.ataque()
        df = self.player.defensa()
        self.fitness = a * atq + b * df

    @property
    def fitness(self) -> float:
        return self.fitness

    def get_genes(self) -> list:
        genes = list()
        genes.append(self.player.altura)
        genes.append(self.player.bota.id)
        genes.append(self.player.casco.id)
        genes.append(self.player.guante.id)
        genes.append(self.player.pechera.id)
        genes.append(self.player.arma.id)
        return genes

    @fitness.setter
    def fitness(self, value):
        self.fitness = value

    @classmethod
    def create_from_genes(cls, genes, p_class):
        ind = Individual(Personaje(p_class, genes[0], genes[1], genes[2], genes[3], genes[4], genes[5]))
        return ind

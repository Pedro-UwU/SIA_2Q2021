import math
from dataclasses import dataclass, field

from DataReader import DataReader
from clases.Clase import Clase


class Personaje:
    clase: Clase
    altura: float
    equipment: list[int]
    # 0 -> weapon
    # 1 -> boots
    # 2 -> helmet
    # 3 -> gloves
    # 4 -> chest plate


    def __init__(self, clase: Clase, height: float, weapon_id: int, boots_id: int, helmet_id: int, gloves_id: int,
                 chestplate_id: int):
        self.clase = clase
        self.altura = height
        self.equipment = [weapon_id, boots_id, helmet_id, gloves_id, chestplate_id]
        self.fitness = None
        self.pseudo_fitness = None

    def __eq__(self, obj):
        return isinstance(obj, Personaje) and \
               obj.altura == self.altura and \
               obj.equipment[0] == self.equipment[0] and \
               obj.equipment[1] == self.equipment[1] and \
               obj.equipment[2] == self.equipment[2] and \
               obj.equipment[3] == self.equipment[3] and \
               obj.equipment[4] == self.equipment[4]

    def __hash__(self):
        return hash((self.altura, self.equipment[0], self.equipment[1], self.equipment[2], self.equipment[3], self.equipment[4]))

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
        return 100 * math.tanh(0.01 * self._sum_fuerza())

    def agilidad(self):
        return math.tanh(0.01 * self._sum_agilidad())

    def pericia(self):
        return 0.6 * math.tanh(0.01 * self._sum_pericia())

    def resistencia(self):
        return math.tanh(0.01 * self._sum_resistencia())

    def vida(self):
        return 100 * math.tanh(0.01 * self._sum_vida())

    def _sum_vida(self):
        if DataReader.reader is None:
            raise Exception('DataReader must be initialized')
        boots = DataReader.reader.get('boots', self.equipment[1]).vida
        helmet = DataReader.reader.get('helmet', self.equipment[2]).vida
        gloves = DataReader.reader.get('gloves', self.equipment[3]).vida
        chestplate = DataReader.reader.get('chestplate', self.equipment[4]).vida
        weapon = DataReader.reader.get('weapon', self.equipment[0]).vida
        return boots + helmet + gloves + chestplate + weapon

    def _sum_resistencia(self):
        if DataReader.reader is None:
            raise Exception('DataReader must be initialized')
        boots = DataReader.reader.get('boots', self.equipment[1]).resistencia
        helmet = DataReader.reader.get('helmet', self.equipment[2]).resistencia
        gloves = DataReader.reader.get('gloves', self.equipment[3]).resistencia
        chestplate = DataReader.reader.get('chestplate', self.equipment[4]).resistencia
        weapon = DataReader.reader.get('weapon', self.equipment[0]).resistencia
        return boots + helmet + gloves + chestplate + weapon

    def _sum_pericia(self):
        if DataReader.reader is None:
            raise Exception('DataReader must be initialized')
        boots = DataReader.reader.get('boots', self.equipment[1]).pericia
        helmet = DataReader.reader.get('helmet', self.equipment[2]).pericia
        gloves = DataReader.reader.get('gloves', self.equipment[3]).pericia
        chestplate = DataReader.reader.get('chestplate', self.equipment[4]).pericia
        weapon = DataReader.reader.get('weapon', self.equipment[0]).pericia
        return boots + helmet + gloves + chestplate + weapon

    def _sum_agilidad(self):
        if DataReader.reader is None:
            raise Exception('DataReader must be initialized')
        boots = DataReader.reader.get('boots', self.equipment[1]).agilidad
        helmet = DataReader.reader.get('helmet', self.equipment[2]).agilidad
        gloves = DataReader.reader.get('gloves', self.equipment[3]).agilidad
        chestplate = DataReader.reader.get('chestplate', self.equipment[4]).agilidad
        weapon = DataReader.reader.get('weapon', self.equipment[0]).agilidad
        return boots + helmet + gloves + chestplate + weapon

    def _sum_fuerza(self):
        if DataReader.reader is None:
            raise Exception('DataReader must be initialized')
        boots = DataReader.reader.get('boots', self.equipment[1]).fuerza
        helmet = DataReader.reader.get('helmet', self.equipment[2]).fuerza
        gloves = DataReader.reader.get('gloves', self.equipment[3]).fuerza
        chestplate = DataReader.reader.get('chestplate', self.equipment[4]).fuerza
        weapon = DataReader.reader.get('weapon', self.equipment[0]).fuerza
        return boots + helmet + gloves + chestplate + weapon

    def calc_fitness(self):
        if self.fitness is None:
            self.fitness = self.clase.attack_constant * self.ataque() + self.clase.defense_constant * self.defensa()
            self.pseudo_fitness = self.fitness
        return self.fitness

    def __repr__(self):
        return f'Clase: {type(self.clase).__name__}, Altura: {self.altura}, Armamento: {self.equipment}, Fitness: {self.fitness}'

    def clone(self):
        new_p = Personaje(self.clase, self.altura, self.equipment[0], self.equipment[1], self.equipment[2], self.equipment[3], self.equipment[4])
        new_p.fitness = self.fitness
        new_p.pseudo_fitness = self.pseudo_fitness
        return new_p

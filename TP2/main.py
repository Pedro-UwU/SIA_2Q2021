import configparser
import os

from DataReader import DataReader
from Personaje import Personaje
from clases.Guerrero import Guerrero
from clases.Defensor import Defensor
from clases.Arquero import Arquero
from clases.Infiltrado import Infiltrado

from armamentos.Arma import Arma
from armamentos.Bota import Bota
from armamentos.Guante import Guante
from armamentos.Pechera import Pechera
from armamentos.Casco import Casco
if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')


    # guerrero = Guerrero()
    # defensor = Defensor()
    # arquero = Arquero()
    # infiltrado = Infiltrado()
    # print(guerrero)
    # print(defensor)
    # print(arquero)
    # print(infiltrado)
    #
    # bota = Bota(2.49, 2.90, 0.43, 0.32, 1.84)
    # guante = Guante(1.39, 0.188, 3.13, 0.80, 2.60)
    # pechera = Pechera(9.50, 2.66, 12.33, 1.24, 8.62)
    # casco = Casco(2.88, 12.1066, 2.4106, 8.68, 0.058)
    # arma = Arma(10.29, 6.55, 13.60, 11.41, 3.47)
    #
    # bota2 = Bota(1.23, 1.80, 0.90, 0.60, 1.30)
    # guante2 = Guante(2.88, 12.1066, 2.4106, 8.68, 0.058)
    # pechera2 = Pechera(10.29, 6.55, 13.60, 11.41, 3.47)
    # casco2 = Casco(1.39, 0.188, 3.13, 0.80, 2.60)
    # arma2 = Arma(9.50, 2.66, 12.33, 1.24, 8.62)
    #
    # print(bota)
    # print(guante)
    # print(pechera)
    # print(casco)
    #
    # # clase: Clase = field()
    # # altura: float = field()
    # # bota: Bota = field()
    # # casco: Casco = field()
    # # guante: Guante = field()
    # # pechera: Pechera = field()
    #
    # personaje = Personaje(defensor, 1.80, bota, casco, guante, pechera, arma)
    # personaje2 = Personaje(arquero, 1.80, bota2, casco2, guante2, pechera2, arma2)
    #
    # print(personaje)
    # print(personaje2)
    #
    # print(personaje.ataque())
    # print(personaje.defensa())
    #
    # print(personaje.atm())
    # print(personaje.dem())
    #
    # print(personaje.fuerza())
    # print(personaje.agilidad())
    # print(personaje.pericia())
    # print(personaje.resistencia())
    # print(personaje.vida())
    parser = configparser.ConfigParser()
    parser.read(configPath)

    data_dir = os.path.join(dirname, parser.get('config', 'DATA_DIR'))
    total_weapons = parser.getint('config', 'TOTAL_WEAPONS')
    total_boots = parser.getint('config', 'TOTAL_BOOTS')
    total_helmets = parser.getint('config', 'TOTAL_HELMETS')
    total_gloves = parser.getint('config', 'TOTAL_GLOVES')
    total_chestplates = parser.getint('config', 'TOTAL_CHESTPLATES')

    reader = DataReader.init_reader(data_dir, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates)
    # armas = reader.get_all('weapon')
    # print(len(armas))
    player = Personaje(Guerrero(), 1.5, 0, 0, 0, 0, 0)
    print(player.resistencia())


import configparser
import os

from DataReader import DataReader
from Genetic_Algorithm.Genetic import Genetic
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
    Genetic.genetic_algorithm(100, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates)


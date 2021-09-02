import configparser
import os

from Config import Config
from Selection_Algorithm.Selection import Selection
from DataReader import DataReader
from Genetic_Algorithm.Genetic import Genetic
from Personaje import Personaje
from clases.Arquero import Arquero

from clases.Guerrero import Guerrero
from clases.Defensor import Defensor
from clases.Infiltrado import Infiltrado

from armamentos.Arma import Arma
from armamentos.Bota import Bota
from armamentos.Guante import Guante
from armamentos.Pechera import Pechera
from armamentos.Casco import Casco

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')
    Config.init_config(configPath)
    parser = configparser.ConfigParser()
    parser.read(configPath)

    data_dir = os.path.join(dirname, parser.get('config', 'DATA_DIR'))
    total_weapons = parser.getint('config', 'TOTAL_WEAPONS')
    total_boots = parser.getint('config', 'TOTAL_BOOTS')
    total_helmets = parser.getint('config', 'TOTAL_HELMETS')
    total_gloves = parser.getint('config', 'TOTAL_GLOVES')
    total_chestplates = parser.getint('config', 'TOTAL_CHESTPLATES')

    # constant_a = parser.getfloat('config', 'A')
    # constant_b = parser.getfloat('config', 'B')
    # constant_k = parser.getfloat('config', 'K')

    # selection = Selection(constant_a, constant_b, constant_k)

    # reader = DataReader(data_dir, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates)
    # armas = reader.get_all('weapon')
    # print(len(armas))
    DataReader.init_reader(Config.config.data_dir, Config.config.total_weapons, Config.config.total_boots, Config.config.total_helmets, Config.config.total_gloves, Config.config.total_chestplates)
    Genetic.genetic_algorithm('Archer')

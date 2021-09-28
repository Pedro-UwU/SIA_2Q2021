import configparser
import os

from ej2.SimpleLinearPerceptron import SimpleLinearPerceptron
from ej2.SimpleNonLinearPerceptron import SimpleNonLinearPerceptron

from ej3.ej3_3 import ej3_3
from ej3.ej3_2 import ej3_2
from ej3.ej3_1 import ej3_1
from ej1.SimplePerceptron import SimplePerceptron
# from ej2.SimpleLinearPerceptron import SimpleLinearPerceptron
# from ej2.SimpleNonLinearPerceptron import SimpleNonLinearPerceptron

from Config import Config

if __name__ == '__main__':

    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')
    Config.init_config(configPath)
    parser = configparser.ConfigParser()
    parser.read(configPath)

    if Config.config.exercise == "1":
        SimplePerceptron.initialize()
        SimplePerceptron.run()
    elif Config.config.exercise == "2":
        if Config.config.is_linear == "True":
            SimpleLinearPerceptron.initialize()
            SimpleLinearPerceptron.run()
        else:
            SimpleNonLinearPerceptron.initialize()
            SimpleNonLinearPerceptron.run()
    elif Config.config.exercise == "3_1":
        ej3_1()
    elif Config.config.exercise == "3_2":
        ej3_2()
    elif Config.config.exercise == "3_3":
        ej3_3()

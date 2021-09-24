import configparser
import os

from ej1.SimplePerceptron import SimplePerceptron
from ej2.SimpleLinearPerceptron import SimpleLinearPerceptron
from ej2.SimpleNonLinearPerceptron import SimpleNonLinearPerceptron

from Config import Config

if __name__ == '__main__':

    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')
    Config.init_config(configPath)
    parser = configparser.ConfigParser()
    parser.read(configPath)

    if Config.config.exercise == 1:
        SimplePerceptron.initialize()
        SimplePerceptron.run()
    elif Config.config.excercise == 2:
        pass

import configparser
import time
import os

from Board import Board
from SokobanSolver import SokobanSolver

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')

    configuration_parser = configparser.ConfigParser()
    configuration_parser.read(configPath)
    filePath = os.path.join(dirname, configuration_parser.get('config', 'BOARD_FILE_PATH'))
    search_function = configuration_parser.get('config', 'SEARCH_FUNCTION')
    board = Board(filePath)
    print("ESTADO ACTUAL:")
    print(board)
    start = time.perf_counter()
    path = SokobanSolver.dls_search(board, 1500)
    end = time.perf_counter()
    print('RESOLUCION:')
    for step in path:
        print(step)
        print('-----------')

    print('Pasos: ', len(path))
    print('Tiempo: ', round((end - start)*100)/100, ' seconds')

    input('\n\nPresiona ENTER para salir')

# TODO

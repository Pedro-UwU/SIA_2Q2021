import configparser
import time
import os
import math
from Board import Board
from SokobanSolver import SokobanSolver

def heu_distance(board):
    player_position = board.get_player_position()
    boxes_positions = board.get_boxes_positions()
    goals_positions = board.get_goals_positions()
    if SokobanSolver.check_dead_lock(board):
        return math.inf
    total_distance = 0
    for box in boxes_positions:
        min_distance = math.inf
        for goal in goals_positions:
            new_distance = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
            if new_distance < min_distance:
                min_distance = new_distance
        total_distance += min_distance
    return total_distance

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
    print('Heursitica: ', heu_distance(board))

    # start = time.perf_counter()
    # path = SokobanSolver.dls_search(board, 1500)
    # end = time.perf_counter()
    # print('RESOLUCION:')
    # for step in path:
    #     print(step)
    #     print('-----------')
    #
    # print('Pasos: ', len(path))
    # print('Tiempo: ', round((end - start)*100)/100, ' seconds')

    input('\n\nPresiona ENTER para salir')

# TODO

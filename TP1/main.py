import configparser
import time
import os
import math
from collections import deque

from Board import Board
from SokobanSolver import SokobanSolver
from Tree import Tree


def heu_distance(board):
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


def get_box_neighbors(box, board):
    neighbors = [(box[0] - 1, box[1]), (box[0] + 1, box[1]),
                 (box[0], box[1] - 1), (box[0], box[1] + 1)]
    return neighbors


def can_move(box, goal, board):
    diff = (goal[0] - box[0], goal[1] - box[1])
    opposite = board.get_static(box[0] + diff[0], box[1] + diff[1])
    return opposite != '#'


def calculate_steps(box, goal, board):
    fr = deque()
    explored = set()
    tree = Tree()
    fr.append(box)
    explored.add(box)
    tree.set_root(box)
    while len(fr) > 0:
        current = fr.popleft()
        if current[0] == goal[0] and current[1] == goal[1]:
            return len(tree.get_path(current)) - 1  # -1 porque estamos tomando el estado inicial como paso
        neighbors = get_box_neighbors(current, board)
        for n in neighbors:
            if n in explored:
                continue
            explored.add(n)
            value = board.get_static(n[0], n[1])
            if value == '#':
                continue
            if (value == ' ' or value == '.') and can_move(box, n, board):
                fr.append(n)
                tree.add_child(current, n)

    return math.inf


def heu_steps_distance(board):
    boxes = board.get_boxes_positions()
    goals = board.get_goals_positions()
    if SokobanSolver.check_dead_lock(board):
        return math.inf
    total_distance = 0
    for box in boxes:
        min_distance = math.inf
        for goal in goals:
            steps = calculate_steps(box, goal, board)
            if steps < min_distance:
                min_distance = steps
        total_distance += min_distance
    return total_distance


def min_distance(boxes, goals, index, used, weights):
    min_dist = math.inf
    b = boxes[index]
    min_g = None
    for g in goals:
        if g in used:
            continue
        used.add(g)
        dist = weights[b][g]
        if index < (len(boxes) - 1):
            dist += min_distance(boxes, goals, index + 1, used, weights)
        used.remove(g)
        if dist < min_dist:
            min_dist = dist

    return min_dist


def heu_minmatching(board):
    boxes = board.get_boxes_positions()
    goals = board.get_goals_positions()
    if SokobanSolver.check_dead_lock(board):
        return math.inf
    weights = {}
    for box in boxes:
        weights[box] = {}
        for goal in goals:
            steps = calculate_steps(box, goal, board)
            weights[box][goal] = steps
    dist = min_distance(boxes, goals, 0, set(), weights)
    return dist


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')

    configuration_parser = configparser.ConfigParser()
    configuration_parser.read(configPath)
    filePath = os.path.join(dirname, configuration_parser.get('config', 'BOARD_FILE_PATH'))
    search_function = configuration_parser.get('config', 'SEARCH_FUNCTION')
    board = Board(filePath)
    deadlock_flag = configuration_parser.getboolean('config', 'CHECK_DEADLOCKS_WITH_UNINFORMED')
    output_file_name = configuration_parser.get('config', 'OUTPUT_FILE_NAME')
    heuristic_name = configuration_parser.get('config', 'HEURISTIC')
    optimized_uninformed = configuration_parser.getboolean('config', 'CHECK_DEADLOCKS_WITH_UNINFORMED')
    print_solution = configuration_parser.getboolean('config', 'PRINT_ON_TERMINAL')
    print_with_colors = configuration_parser.getboolean('config', 'PRINT_WITH_COLORS')

    search = None
    informed = False
    if search_function == 'BFS':
        search = SokobanSolver.bfs_search
    elif search_function == 'DFS':
        search = SokobanSolver.dfs_search
    elif search_function == 'IDDFS':
        search = SokobanSolver.iddfs_search
    elif search_function == 'Greedy':
        search = SokobanSolver.greedy_search
        informed = True
    elif search_function == 'A Star':
        search = SokobanSolver.a_star
        informed = True
    elif search_function == 'IDA Star':
        search = SokobanSolver.ida_star
        informed = True
    else:
        print("INVALID SEARCH FUNCTION")
        exit(-1)

    heuristic = None
    if informed:
        if heuristic_name == 'Distance':
            heuristic = heu_distance
        elif heuristic_name == 'Steps':
            heuristic = heu_steps_distance
        elif heuristic_name == 'Minmatching':
            heuristic = heu_minmatching
        else:
            print('INVALID HEURISTIC FUNCTION')
            exit(-1)

    start = time.perf_counter()
    print('Searching for a solution to ', filePath, '...')
    if not informed:
        path, explored_nodes, frontier = search(board, optimized_uninformed)
    else:
        path, explored_nodes, frontier = search(board, heuristic)
    end = time.perf_counter()

    output = open('./' + output_file_name, 'w+', encoding='utf-8')
    output.write('Función: ' + search_function + '\n')
    output.write(('Resultado de la busqueda: ' + ('ENCONTRADO' if len(path) > 0 else 'NO ENCONTRADO') + '\n'))
    output.write(('Nodos Expandidos: ' + str(explored_nodes) + '\n'))
    output.write(('Nodos en la frontera: ' + str(frontier) + '\n'))
    output.write(('Profundidad de solucion: ' + str(len(path) - 1) + '\n'))
    output.write(('Tiempo de procesamiento: ' + str(round((end - start) * 1000) / 1000) + ' segundos' + '\n'))
    if informed:
        output.write(str('Heuristica: ' + heuristic_name + '\n'))
    else:
        output.write(str('Check de deadlocks: ' + str(optimized_uninformed) + '\n'))
    output.write('\nSOLUCION:\n')
    for step in path:
        output.write(step.__str__())
        output.write('-------------------------------\n')
    output.close()

    if print_solution:
        for s in path:
            s.print_board(print_with_colors)
            print('-------------------------------\n')

    print(search.__name__)

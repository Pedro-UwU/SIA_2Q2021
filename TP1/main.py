import configparser
import time

from collections import deque
from Board import Board
from Tree import Tree
import os




def bfs_search(initial_state):
    fr = deque()
    explored = set()
    tree = Tree()
    tree.set_root(initial_state)

    fr.append((initial_state, 1))
    explored.add(initial_state)
    while len(fr) > 0:
        current_state, depth = fr.popleft()
        if current_state.is_goal():
            return tree.get_path(current_state)
        states = current_state.get_possible_states()
        for s in states:
            if s not in explored:
                tree.add_child(current_state, s)
                fr.append((s, depth+1))
                # lo agrego a explored asi si llego al mismo estado desde otro, no se agrega dos veces a fr
                explored.add(s)
    print('NO HAY SOLUCION')
    return []

def dfs_search(initial_state):
    fr = deque()
    explored = set()
    tree = Tree()
    tree.set_root(initial_state)

    fr.append(initial_state)
    while len(fr) > 0:
        current_state = fr.pop()
        if current_state.is_goal():
            return tree.get_path(current_state)
        states = current_state.get_possible_states()
        for s in states:
            if s not in explored:
                tree.add_child(current_state, s)
                fr.append(s)
        explored.add(current_state)
    print('NO HAY SOLUCION')
    return []


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    configPath = os.path.join(dirname, 'config.conf')

    configuration_parser = configparser.ConfigParser()
    configuration_parser.read(configPath)
    filePath = os.path.join(dirname, configuration_parser.get('config', 'BOARD_FILE_PATH'))
    board = Board(filePath)
    print("ESTADO ACTUAL:")
    search_function = bfs_search
    board.print_board()
    start = time.perf_counter()
    path = search_function(board)
    end = time.perf_counter()
    print('RESOLUCION:')
    for step in path:
        step.print_board()
        print('-----------')

    print('Funcion de busqueda: ', search_function.__name__)
    print('Pasos: ', len(path))
    print('Tiempo: ', round((end - start)*100)/100, ' seconds')

# TODO

import math
import time

from Tree2 import *
from collections import deque

from Tree import Tree


class SokobanSolver:
    @staticmethod
    def bfs_search(initial_state, optimized):
        fr = deque()
        explored = set()
        explored.add(initial_state)
        tree = Tree()
        tree.set_root(initial_state)

        fr.append((initial_state, 1))
        explored.add(initial_state)
        while len(fr) > 0:
            current_state, depth = fr.popleft()
            if current_state.is_goal():
                return tree.get_path(current_state), len(explored), len(fr)
            states = current_state.get_possible_states()
            for s in states:
                if s not in explored:
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s) and optimized:
                        continue
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))
                    # lo agrego a explored asi si llego al mismo estado desde otro, no se agrega dos veces a fr
        return [], len(explored), len(fr)

    @staticmethod
    def dfs_search(initial_state, optimized):
        fr = deque()
        explored = set()
        explored.add(initial_state)
        tree = Tree()
        tree.set_root(initial_state)

        fr.append((initial_state, 1))
        while len(fr) > 0:
            current_state, depth = fr.pop()
            if current_state.is_goal():
                return tree.get_path(current_state), len(explored), len(fr)
            states = current_state.get_possible_states()
            for s in states:
                if s not in explored:
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s) and optimized:
                        continue
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))
        return [], len(explored), len(fr)

    @staticmethod
    def iddfs_search(board, optimized):
        # return result, explored, frontier
        lim = 0
        tree = Tree2()
        tree.set_root(board)
        root = tree.root
        explored = set()
        fr = deque()
        next_iter = deque()
        depths = {root.value: root.depth}

        explored.add(root.value)
        fr.append(root)
        while len(fr) > 0 or len(next_iter) > 0:
            if len(fr) == 0:
                fr = next_iter
                next_iter = deque()
                lim += 1
            current = fr.pop()

            if current.value.is_goal():
                path = current.get_path()
                path.reverse()
                return path, len(explored), len(fr) + len(next_iter)

            states = current.value.get_possible_states()
            for s in states:
                new_node = Node(s, current.depth + 1, current)
                if s in explored:
                    if depths[s] <= new_node.depth:
                        continue
                depths[s] = new_node.depth
                explored.add(s)
                if SokobanSolver.check_dead_lock(s) and optimized:
                    continue

                if new_node.depth > lim:
                    next_iter.append(new_node)
                else:
                    fr.append(new_node)
        return [], len(explored), len(fr) + len(next_iter)

    # True si se puede mover o hay un goal en el camino
    @staticmethod
    def __check_box_movement(board, box_coords, direction, look_up_direction):
        tile = board.get_static(box_coords[0], box_coords[1])
        neighbor = board.get_static(box_coords[0] + look_up_direction[0], box_coords[1] + look_up_direction[1])
        if tile == '#':
            return False
        if tile == '.':
            return True
        if neighbor == '#':
            new_coords = (box_coords[0] + direction[0], box_coords[1] + direction[1])
            return SokobanSolver.__check_box_movement(board, new_coords, direction, look_up_direction)
        return True

    @staticmethod
    def check_dead_lock(board):
        # get the position of all boxes
        y, x = 0, 0
        coords = []
        for row in board.dynamic_board:
            x = 0
            for col in board.dynamic_board[y]:
                if board.dynamic_board[y][x] == '$':
                    coords.append((y, x))
                x += 1
            y += 1

        # for each box check:
        # 1) if it is in a corner
        # 2) if it is in a cluster of 4 boxes
        # 3) if it is in a wall, check if it the wall opens up or if there is a goal in the row or column

        for coord in coords:

            i = coord[0]
            j = coord[1]
            if board.get_static(i, j) == '.':
                continue

            static_neighbors = []
            dynamic_neighbors = []
            for a in range(3):
                static_neighbors.append([])
                dynamic_neighbors.append([])
                for b in range(3):
                    static_neighbors[a].append(0)
                    dynamic_neighbors[a].append(0)

            static_neighbors[0][0] = board.get_static(i - 1, j - 1)
            static_neighbors[0][1] = board.get_static(i - 1, j)
            static_neighbors[0][2] = board.get_static(i - 1, j + 1)
            static_neighbors[1][0] = board.get_static(i, j - 1)
            static_neighbors[1][1] = board.get_static(i, j)
            static_neighbors[1][2] = board.get_static(i, j + 1)
            static_neighbors[2][0] = board.get_static(i + 1, j - 1)
            static_neighbors[2][1] = board.get_static(i + 1, j)
            static_neighbors[2][2] = board.get_static(i + 1, j + 1)

            dynamic_neighbors[0][0] = board.get_dynamic(i - 1, j - 1)
            dynamic_neighbors[0][1] = board.get_dynamic(i - 1, j)
            dynamic_neighbors[0][2] = board.get_dynamic(i - 1, j + 1)
            dynamic_neighbors[1][0] = board.get_dynamic(i, j - 1)
            dynamic_neighbors[1][1] = board.get_dynamic(i, j)
            dynamic_neighbors[1][2] = board.get_dynamic(i, j + 1)
            dynamic_neighbors[2][0] = board.get_dynamic(i + 1, j - 1)
            dynamic_neighbors[2][1] = board.get_dynamic(i + 1, j)
            dynamic_neighbors[2][2] = board.get_dynamic(i + 1, j + 1)

            # 1)
            if static_neighbors[2][1] == '#' and static_neighbors[1][2] == '#':
                return True
            if static_neighbors[1][2] == '#' and static_neighbors[0][1] == '#':
                return True
            if static_neighbors[0][1] == '#' and static_neighbors[1][0] == '#':
                return True
            if static_neighbors[1][0] == '#' and static_neighbors[2][1] == '#':
                return True

            # 2)
            if (static_neighbors[0][0] == '#' or dynamic_neighbors[0][0] == '$') and (
                    static_neighbors[0][1] == '#' or dynamic_neighbors[0][1] == '$') and (
                    static_neighbors[1][0] == '#' or dynamic_neighbors[1][0] == '$'):
                return True
            if (static_neighbors[0][1] == '#' or dynamic_neighbors[0][1] == '$') and (
                    static_neighbors[0][2] == '#' or dynamic_neighbors[0][2] == '$') and (
                    static_neighbors[1][2] == '#' or dynamic_neighbors[1][2] == '$'):
                return True
            if (static_neighbors[1][2] == '#' or dynamic_neighbors[1][2] == '$') and (
                    static_neighbors[2][2] == '#' or dynamic_neighbors[2][2] == '$') and (
                    static_neighbors[2][1] == '#' or dynamic_neighbors[2][1] == '$'):
                return True
            if (static_neighbors[2][1] == '#' or dynamic_neighbors[2][1] == '$') and (
                    static_neighbors[2][0] == '#' or dynamic_neighbors[2][0] == '$') and (
                    static_neighbors[1][0] == '#' or dynamic_neighbors[1][0] == '$'):
                return True

            # 3)
            if static_neighbors[1][0] == '#':
                return not (SokobanSolver.__check_box_movement(board, coord, (-1, 0),
                                                               (0, -1)) or SokobanSolver.__check_box_movement(board,
                                                                                                              coord,
                                                                                                              (1, 0),
                                                                                                              (0, -1)))
            if static_neighbors[0][1] == '#':
                return not (SokobanSolver.__check_box_movement(board, coord, (0, -1),
                                                               (-1, 0)) or SokobanSolver.__check_box_movement(board,
                                                                                                              coord,
                                                                                                              (0, 1),
                                                                                                              (-1, 0)))
            if static_neighbors[1][2] == '#':
                return not (SokobanSolver.__check_box_movement(board, coord, (-1, 0),
                                                               (0, 1)) or SokobanSolver.__check_box_movement(board,
                                                                                                             coord,
                                                                                                             (1, 0),
                                                                                                             (0, 1)))
            if static_neighbors[2][1] == '#':
                return not (SokobanSolver.__check_box_movement(board, coord, (0, -1),
                                                               (1, 0)) or SokobanSolver.__check_box_movement(board,
                                                                                                             coord,
                                                                                                             (0, 1),
                                                                                                             (1, 0)))
        return False

    @staticmethod
    def greedy_search(board, heuristic):
        fr = []
        explored = set()
        explored.add(board)
        tree = Tree()
        tree.set_root(board)

        fr.append((board, 1, heuristic(board)))
        while len(fr) > 0:
            current_state, depth, current_h = fr.pop(0)
            if current_state.is_goal():
                return tree.get_path(current_state), len(explored), len(fr)
            states = current_state.get_possible_states()
            for s in states:
                if s not in explored:
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s):
                        continue
                    tree.add_child(current_state, s)
                    h = heuristic(s)
                    fr.append((s, depth + 1, h))
                    # lo agrego a explored asi si llego al mismo estado desde otro, no se agrega dos veces a fr
            fr.sort(key=lambda x: x[2])
        return [], len(explored), len(fr)

    @staticmethod
    def a_star(board, heuristic):
        fr = []
        explored = set()
        explored.add(board)
        tree = Tree()
        tree.set_root(board)

        fr.append((board, 1, 0, heuristic(board)))
        while len(fr) > 0:
            current_state, depth, f_n, h_n = fr.pop(0)
            if current_state.is_goal():
                return tree.get_path(current_state), len(explored), len(fr)
            states = current_state.get_possible_states()
            for s in states:
                if s not in explored:
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s):
                        continue
                    tree.add_child(current_state, s)
                    h = heuristic(s)
                    f = depth + 1 + h
                    fr.append((s, depth + 1, h, f))
                    # lo agrego a explored asi si llego al mismo estado desde otro, no se agrega dos veces a fr
            fr.sort(key=lambda x: f)
        return [], len(explored), len(fr)

    @staticmethod
    def ida_star(board, heuristic):
        tree = Tree2()
        tree.set_root(board)
        root = tree.root

        explored = set()
        fr = deque()
        next_iter = deque()
        depths = {root.value: 0}

        explored.add(root.value)
        fr.append((root, heuristic(root.value)))

        lim = heuristic(root.value)
        min_f = math.inf
        while len(fr) > 0 or len(next_iter) > 0:
            if len(fr) == 0:
                fr = next_iter
                next_iter = deque()
                lim = min_f
                min_f = math.inf
            current, current_f = fr.pop()
            if current.value.is_goal():
                path = current.get_path()
                path.reverse()
                return path, len(explored), len(fr) + len(next_iter)
            states = current.value.get_possible_states()
            for s in states:
                new_node = Node(s, current.depth + 1, current)
                if s in explored:
                    if depths[s] <= new_node.depth:
                        continue
                depths[s] = new_node.depth
                explored.add(s)
                h = heuristic(s)
                if h == math.inf:
                    continue
                f = new_node.depth + h
                if f > lim:
                    next_iter.append((new_node, f))
                    if f < min_f:
                        min_f = f
                else:
                    fr.append((new_node, f))
        return [], len(explored), len(fr) + len(next_iter)
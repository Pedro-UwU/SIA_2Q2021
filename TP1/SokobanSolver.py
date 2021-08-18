from collections import deque

from Tree import Tree


class SokobanSolver:
    @staticmethod
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
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s):
                        continue
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))
                    # lo agrego a explored asi si llego al mismo estado desde otro, no se agrega dos veces a fr
            print(depth)

        print('NO HAY SOLUCION')
        return []

    @staticmethod
    def dfs_search(initial_state):
        fr = deque()
        explored = set()
        tree = Tree()
        tree.set_root(initial_state)

        fr.append((initial_state, 1))
        while len(fr) > 0:
            current_state, depth = fr.pop()
            if current_state.is_goal():
                return tree.get_path(current_state)
            states = current_state.get_possible_states()
            for s in states:
                if s not in explored:
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s):
                        continue
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))

        print('NO HAY SOLUCION')
        return []

    @staticmethod
    def __dls_search(initial_state, depth_limit):
        fr = deque()
        explored = set()
        tree = Tree()
        tree.set_root(initial_state)

        fr.append((initial_state, 1))
        explored.add(initial_state)
        while len(fr) > 0:
            current_state, depth = fr.pop()
            if current_state.is_goal():
                return tree.get_path(current_state)
            states = current_state.get_possible_states()
            for s in states:
                if s in explored:
                    prev_depth = tree.get_depth(s)
                    if prev_depth < (depth + 1):
                        continue
                if depth < depth_limit:
                    explored.add(s)
                    if SokobanSolver.check_dead_lock(s):
                        continue
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))
        return []

    @staticmethod
    def iddfs_search(initial_state):
        depth = 0
        result = []
        tree = Tree()
        tree.set_root(initial_state)
        while len(result) == 0:
            print('Depth: ', depth, 'Result: ', result)
            result = SokobanSolver.__dls_search(initial_state, depth)
            depth += 1
        return result

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

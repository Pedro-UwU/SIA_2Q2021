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
                    if SokobanSolver.__check_dead_lock(s):
                        continue
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))
                    # lo agrego a explored asi si llego al mismo estado desde otro, no se agrega dos veces a fr
                    explored.add(s)
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
                    tree.add_child(current_state, s)
                    fr.append((s, depth + 1))
                    explored.add(s)

        print('NO HAY SOLUCION')
        return []

    @staticmethod
    def dls_search(initial_state, depth_limit):
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
                if depth < depth_limit:
                    if s not in explored or (s in explored and tree.get_depth(s) > (depth + 1)):
                        tree.add_child(current_state, s)
                        tree.update_depth(s, depth + 1)
                        fr.append((s, depth + 1))
                        explored.add(s)

        print('NO HAY SOLUCION')
        return []

    @staticmethod
    def __check_dead_lock(board):
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
                #print(static_neighbors, 'BR', coord)
                return True
            if static_neighbors[1][2] == '#' and static_neighbors[0][1] == '#':
                #print(static_neighbors, 'TR', coord)
                return True
            if static_neighbors[0][1] == '#' and static_neighbors[1][0] == '#':
                #print(static_neighbors, 'TL', coord)
                return True
            if static_neighbors[1][0] == '#' and static_neighbors[2][1] == '#':
                #print(static_neighbors, 'BL', coord)
                return True

            


        return False
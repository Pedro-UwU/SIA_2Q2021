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
                        tree.update_depth(s, depth+1)
                        fr.append((s, depth + 1))
                        explored.add(s)

        print('NO HAY SOLUCION')
        return []

PLAYER = '@'
WALL = '#'
BOX = '$'
GOAL = '.'
SPACE = ' '
BOX_AND_GOAL = '*'


class Board:
    def __init__(self, file_name = None):
        self.static_board = []
        self.dynamic_board = []
        if file_name is None:
            return
        board_file = open(file_name, 'r')
        line = 0
        for string in board_file.readlines():
            self.static_board.append([])
            self.dynamic_board.append([])
            char = 0
            for ch in string:
                if ch == '\n':
                    continue
                if ch == WALL or ch == GOAL or ch == SPACE:
                    self.static_board[line].append(ch)
                    self.dynamic_board[line].append(SPACE)
                elif ch == BOX or ch == PLAYER:
                    self.static_board[line].append(SPACE)
                    self.dynamic_board[line].append(ch)
                elif ch == BOX_AND_GOAL:
                    self.static_board[line].append(GOAL)
                    self.dynamic_board[line].append(BOX)
                char += 1
            line += 1
        board_file.close()

    def print_board(self):
        for y in range(len(self.static_board)):
            output = ''
            for x in range(len(self.static_board[y])):
                dy_ch = self.dynamic_board[y][x]
                st_ch = self.static_board[y][x]
                if dy_ch == PLAYER:
                    output += '\033[93m' + dy_ch
                elif dy_ch == BOX:
                    output += '\033[91m' + dy_ch
                elif st_ch == WALL:
                    output += '\033[94m' + st_ch
                elif st_ch == GOAL:
                    output += '\033[92m' + st_ch
                elif st_ch == SPACE:
                    output += st_ch
            output += '\033[0m'  # Para que los prints sigan siendo blancos
            print(output)

    def __get_player_position(self):
        y = 0
        for row in self.dynamic_board:
            x = 0
            for char in row:
                if char == PLAYER:
                    return (y, x)
                x += 1
            y += 1
        return (-1, -1)

    def __copy_board(self):
        new_board = Board()
        new_board.static_board = self.static_board.copy()
        for i in range(len(self.static_board)):
            new_board.static_board[i] = self.static_board[i].copy()

        new_board.dynamic_board = self.dynamic_board.copy()
        for i in range(len(self.dynamic_board)):
            new_board.dynamic_board[i] = self.dynamic_board[i].copy()

        return new_board

    def get_possible_states(self):
        (y, x) = self.__get_player_position()
        if y == -1 or x == -1:
            return []

        states = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction in directions:
            neighbor_coord = (y + direction[0], x + direction[1])
            static_neighbor = ''
            dynamic_neighbor = ''
            # get_neighbor
            try:
                static_neighbor = self.static_board[neighbor_coord[0]][neighbor_coord[1]]
                dynamic_neighbor = self.dynamic_board[neighbor_coord[0]][neighbor_coord[1]]
            except:
                static_neighbor = WALL
                dynamic_neighbor = SPACE

            if static_neighbor == SPACE or static_neighbor == GOAL:
                if dynamic_neighbor == SPACE:
                    new_board = self.__copy_board()
                    new_board.dynamic_board[y][x] = SPACE
                    new_board.dynamic_board[neighbor_coord[0]][neighbor_coord[1]] = PLAYER
                    states.append(new_board)
                elif dynamic_neighbor == BOX and self.__check_box_movement(neighbor_coord, direction):
                    new_board = self.__copy_board()
                    new_board.dynamic_board[y][x] = SPACE
                    new_board.dynamic_board[neighbor_coord[0]][neighbor_coord[1]] = PLAYER
                    new_board.dynamic_board[neighbor_coord[0] + direction[0]][neighbor_coord[1] + direction[1]] = BOX
                    states.append(new_board)

        return states

    def __check_box_movement(self, neighbor_coord, direction):
        box_neighbor_coord = (neighbor_coord[0] + direction[0],  neighbor_coord[1] + direction[1])
        static_box_neighbor = ''
        dynamic_box_neighbor = ''
        try:
            static_box_neighbor = self.static_board[box_neighbor_coord[0]][box_neighbor_coord[1]]
            dynamic_box_neighbor = self.dynamic_board[box_neighbor_coord[0]][box_neighbor_coord[1]]
        except:
            static_box_neighbor = WALL
            dynamic_box_neighbor = SPACE
        if (static_box_neighbor == ' ' or static_box_neighbor == '.') and dynamic_box_neighbor == ' ':
            return True
        return False

    def get_dynamic(self, i, j):
        try:
            char = self.dynamic_board[i][j]
        except:
            char = ' '
        return char

    def get_static(self, i, j):
        try:
            char = self.static_board[i][j]
        except:
            char = '#'
        return char


    def __hash__(self):
        return hash(self.__str__())
        # hash_code = 0
        # count = 1
        # for i in range(len(self.static_board)):
        #     for j in range(len(self.static_board[i])):
        #         if self.dynamic_board[i][j] == SPACE:
        #             hash_code += count
        #         elif self.dynamic_board[i][j] == PLAYER:
        #             hash_code += count ** 5
        #         elif self.dynamic_board[i][j] == BOX:
        #             hash_code += count ** 3
        #
        #         if self.static_board[i][j] == SPACE:
        #             hash_code += count ** 4
        #         elif self.static_board[i][j] == WALL:
        #             hash_code += count ** 2
        #         elif self.static_board[i][j] == GOAL:
        #             hash_code += count ** 6
        #         count += 1
        # return hash_code

    def __str__(self):
        output = ''
        for y in range(len(self.static_board)):
            for x in range(len(self.static_board[y])):
                dy_ch = self.dynamic_board[y][x]
                st_ch = self.static_board[y][x]
                if st_ch == GOAL and dy_ch == BOX:
                    output += BOX_AND_GOAL
                elif dy_ch == PLAYER or dy_ch == BOX:
                    output += dy_ch
                else:
                    output += st_ch
            output += '\n'
        return output

    def __eq__(self, other):
        if other is None:
            return False
        if other is self:
            return True
        if isinstance(other, self.__class__):
            return self.__str__() ==  other.__str__()
            # if (len(self.static_board) != len(other.static_board)) or (len(self.dynamic_board) != len(other.dynamic_board)):
            #     return False
            # for i in range(len(self.static_board)):
            #     if self.static_board[i] != other.static_board[i] or self.dynamic_board[i] != other.dynamic_board[i]:
            #         return False
            # return True
        return False

    def is_goal(self):
        for i in range(len(self.static_board)):
            for j in range(len(self.static_board[i])):
                if self.static_board[i][j] == GOAL and self.dynamic_board[i][j] != BOX:
                    return False
        return True
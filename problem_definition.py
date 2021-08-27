def get_sub_matrix(ii, jj):
    return 3*(ii//3) + jj//3


class Sudoku:
    def __init__(self, matrix):
        self.matrix = [[x for x in row] for row in matrix]
        self.last_action = [(-1, -1), -1]

    def __getitem__(self, key):
        i, j = key
        if 0 <= i < 9 and 0 <= j < 9:
            return self.matrix[i][j]
        else:
            raise IndexError

    def __setitem__(self, key, value):
        i, k = key
        if self.valid_position(i, k, value):
            self.matrix[i][k] = value
            self.last_action[0] = key
            self.last_action[1] = value
        else:
            raise ValueError

    def __eq__(self, other):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __copy__(self):
        return Sudoku(self.matrix)

    def __str__(self):
        return "\n".join(["|".join([str(x) for x in row]) for row in self.matrix])

    def __len__(self):
        return len(list(self.empty_position))

    def __hash__(self):
        return hash((tuple(x) for x in self.matrix))

    def valid_position(self, i, j, value):
        if self.matrix[i][j] != 0:
            return False
        for ii in range(len(self.matrix)):
            for jj in range(len(self.matrix[ii])):
                if i == ii and value == self.matrix[ii][jj]:
                    return False
                elif j == jj and value == self.matrix[ii][jj]:
                    return False
                elif get_sub_matrix(ii, jj) == get_sub_matrix(i, j) and value == self.matrix[ii][jj]:
                    return False
        return True

    @property
    def empty_position(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 0:
                    yield i, j

    @property
    def available(self):
        availables = []
        for position in self.empty_position:
            i, j = position
            availables.append(((i, j), set()))
            for k in range(1, 10):
                if self.valid_position(i, j, k):
                    availables[-1][1].add(k)
        availables = sorted(availables, key=lambda x: len(x[1]))
        return availables

    def get_sumatrix(self, n):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if 3*(i//3) + j//3 == n:
                    yield self.matrix[i][j]

    def remove_trivial_solution_l1(self, posibles=()):
        if not posibles:
            posibles = self.available
        for posible in posibles:
            if len(posible[1]) == 1:
                try:
                    self[posible[0]] = posible[1].pop()
                except ValueError:
                    return None
            else:
                continue
        return self

    def remove_trivial_solution_l2(self, matrix):
        dif = False
        for value in range(1, 10):
            for i in range(len(matrix)):
                if value not in matrix[i]:
                    posibles = set()
                    for j in range(len(matrix)):
                        if self.valid_position(i, j, value):
                            posibles.add(j)
                    if len(posibles) == 1:
                        j = posibles.pop()
                        self[i, j] = value
                        dif = True
        return dif

    def remove_trivial_solution(self):
        posibles = tuple(self.available)
        old = len(posibles)
        new = -1
        while old != new:
            transverse = [[self.matrix[j][i] for j in range(len(self.matrix))] for i in range(len(self.matrix[0]))]
            l2 = self.remove_trivial_solution_l2(self.matrix)
            l3 = self.remove_trivial_solution_l2(transverse)
            l1 = self.remove_trivial_solution_l1(posibles)
            if l1 is None and not l2 and not l3:
                return None
            posibles = self.available
            old = new
            new = len(posibles)
        return self


class State:
    def __init__(self, sudoku, g=0, h=0):
        self.sudoku = sudoku
        self.g = g
        self.h = h

    def __eq__(self, other):
        return self.sudoku == other.sudoku

    def __copy__(self):
        return State(self.sudoku, self.g, self.h)

    def __hash__(self):
        return hash(self.sudoku)

    @property
    def complete(self):
        return len(self.sudoku) == 0

    @property
    def last_action(self):
        return self.sudoku.last_action

    def set_sudoku(self, sudoku):
        self.sudoku = sudoku


class Action:
    def __init__(self, state):
        self._state = state
        self._positions = tuple((value[0] for value in self._state.sudoku.available))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def get_successors(self):
        new_sudoku = self._state.sudoku.__copy__()

        new_sudoku = new_sudoku.remove_trivial_solution()
        new_state = State(new_sudoku, self._state.g)

        if new_sudoku is None:
            return []
        elif new_sudoku != self._state.sudoku:
            return [new_state]

        availables = new_sudoku.available
        movements = []
        pos = availables[0][0]
        for p in availables[0][1]:
            tmp_sudoku = new_sudoku.__copy__()
            tmp_sudoku[pos] = p
            tmp_state = State(tmp_sudoku, self._state.g)
            movements.append(tmp_state)

        return movements



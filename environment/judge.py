from itertools import product

from environment.grid import State


class Judge:
    @staticmethod
    def is_over_from(state: State, col: int, row: int) -> bool:
        state = state.cols_first
        c = state[col][row]
        if c is None: return False

        width, height = len(state), len(state[0])

        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if dx == dy == 0: continue
            if not (col + 3 * dx) in range(width): continue
            if not (row + 3 * dy) in range(height): continue
            if all([state[col + i * dx][row + i * dy] == c
                    for i in [1, 2, 3]]): return True

        return False

    def is_over_from_last_in_col(self, state: State, col: int) -> bool:
        grid = state.rows_first
        for row in reversed(range(len(grid))):
            if grid[row][col] is not None:
                return self.is_over_from(state, col, row)
        assert False, 'Empty column'

    @staticmethod
    def is_over(state: State) -> bool:
        return Judge.is_over_horizontal(state) or \
               Judge.is_over_vertical(state) or \
               Judge.is_over_rightdown(state) or \
               Judge.is_over_rightup(state)

    @staticmethod
    def is_over_horizontal(state: State) -> bool:
        state = state.rows_first
        width = len(state[0])
        for row, col_id in product(state, range(width - 3)):
            c = row[col_id]
            if c is not None and all([row[col_id + i] == c for i in [1, 2, 3]]): return True
        return False

    @staticmethod
    def is_over_vertical(state: State) -> bool:
        state = state.cols_first
        height = len(state[0])
        for col, row_id in product(state, range(height - 3)):
            c = col[row_id]
            if c is not None and all([col[row_id + i] == c for i in [1, 2, 3]]): return True
        return False

    @staticmethod
    def is_over_rightup(state: State) -> bool:
        state = state.cols_first
        width = len(state)
        height = len(state[0])
        for col_id, row_id in product(range(width - 3), range(height - 3)):
            c = state[col_id][row_id]
            if c is not None and all([state[col_id + i][row_id + i] == c for i in [1, 2, 3]]): return True
        return False

    @staticmethod
    def is_over_rightdown(state: State) -> bool:
        state = state.cols_first
        width = len(state)
        height = len(state[0])
        for col_id, row_id in product(range(width - 3), range(3, height)):
            c = state[col_id][row_id]
            if c is not None and all([state[col_id + i][row_id - i] == c for i in [1, 2, 3]]): return True
        return False

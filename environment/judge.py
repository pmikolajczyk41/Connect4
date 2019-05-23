from itertools import product

from environment.grid import State


class Judge:
    @staticmethod
    def is_over_from(state: State, col: int, row: int) -> bool:
        state = state.cols_first
        width, height = len(state), len(state[0])

        if col not in range(width): return False
        if row not in range(height): return False

        c = state[col][row]
        if c is None: return False

        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if dx == dy == 0: continue
            if (col + 3 * dx) not in range(width): continue
            if (row + 3 * dy) not in range(height): continue
            if all([state[col + i * dx][row + i * dy] == c
                    for i in [1, 2, 3]]): return True

        return False

    def is_over_after_move_in_col(self, state: State, col_id: int) -> bool:
        grid = state.rows_first
        row_id = None
        for row in reversed(range(len(grid))):
            if grid[row][col_id] is not None:
                row_id = row
                break
        assert row_id is not None, 'Empty column'

        return any([self.is_over_from(state, col_id + dx, row_id + dy)
                    for dx, dy in product([-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2])])

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

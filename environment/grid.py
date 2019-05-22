from typing import List, Union

from environment.colors import Color


class State:
    def __init__(self, data: List[List[Union[Color, None]]]):
        self._data = data

    @property
    def rows_first(self):
        return list(zip(*self._data))

    @property
    def cols_first(self):
        return self._data


class Grid:
    def __init__(self, ncols: int = 7, nrows: int = 6):
        self._grid = [[None for _ in range(nrows)]
                      for _ in range(ncols)]
        self._setup_with_given_grid()

    @classmethod
    def from_state(cls, state: State):
        grid = Grid(0, 0)
        grid._grid = state.cols_first
        grid._setup_with_given_grid()
        return grid

    def _setup_with_given_grid(self):
        self._ncols = len(self._grid)
        if self.ncols > 0: self._nrows = len(self._grid[0])

        self._heights = [0 for _ in range(self._ncols)]
        for col_id in range(self.ncols):
            for disc in self._grid[col_id]:
                if disc is not None:
                    self._heights[col_id] += 1

    @property
    def ncols(self) -> int: return self._ncols

    @property
    def nrows(self) -> int: return self._nrows

    @property
    def state(self) -> State: return State(self._grid)

    def move(self, color: Color, column: int) -> None:
        assert column in range(self._ncols), 'Column out of grid'
        height = self._heights[column]
        assert height < self._nrows, 'Full column'

        self._grid[column][height] = color
        self._heights[column] += 1

    def undo_move(self, column: int) -> None:
        assert column in range(self._ncols), 'Column out of grid'
        height = self._heights[column]
        assert height > 0, 'Empty column'

        self._grid[column][height - 1] = None
        self._heights[column] -= 1

    @property
    def available_moves(self) -> List[int]:
        return [col_id for col_id in range(self._ncols)
                if self._heights[col_id] < self._nrows]

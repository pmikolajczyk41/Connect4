from itertools import product

from environment.colors import Color
from environment.grid import State


class Evaluator:
    weights = [0, 0, 2, 10, 100]

    @staticmethod
    def evaluate(state: State) -> int:
        grid = state.cols_first
        width, height, value = len(grid), len(grid[0]), 0

        for col, row in product(range(width - 3), range(height)):
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                if not (col + 3 * dx) in range(width): continue
                if not (row + 3 * dy) in range(height): continue
                value += Evaluator._evaluate_block(state, col, row, dx, dy)

        return value

    @staticmethod
    def _evaluate_block(state: State,
                        col: int, row: int,
                        dx: int, dy: int) -> int:
        reds, blacks = 0, 0
        state = state.cols_first

        for i in [0, 1, 2, 3]:
            color = state[col + i * dx][row + i * dy]
            if color == Color.RED: reds += 1
            elif color == Color.BLACK: blacks += 1

        if reds == 0: return -Evaluator.weights[blacks]
        elif blacks == 0: return Evaluator.weights[reds]
        return 0

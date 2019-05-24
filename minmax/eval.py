from itertools import product, chain
from typing import Tuple

from environment.colors import Color
from environment.grid import State, Grid
from environment.judge import Judge

INF = int(1e9)
MAX_COLOR = Color.RED
MIN_COLOR = Color.BLACK


class Evaluator:
    weights = [0, 0, 4, 10]

    @staticmethod
    def evaluate(state: State, judge: Judge) -> int:
        cumulative_block_value = Evaluator._compute_block_values(state)
        if abs(cumulative_block_value) == INF: return cumulative_block_value

        next_move_finishing, winning_color = Evaluator._check_next_move(state, judge)
        if not next_move_finishing: return cumulative_block_value

        if winning_color == MAX_COLOR: return INF
        return -INF

    @staticmethod
    def _compute_block_values(state: State) -> int:
        grid = state.cols_first
        width, height, cumulative_block_value = len(grid), len(grid[0]), 0

        for col, row in product(range(width - 3), range(height)):
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                if not (col + 3 * dx) in range(width): continue
                if not (row + 3 * dy) in range(height): continue

                block_value = Evaluator._evaluate_block(state, col, row, dx, dy)
                if abs(block_value) == INF: return block_value
                cumulative_block_value += block_value

        return cumulative_block_value

    @staticmethod
    def _evaluate_block(state: State,
                        col: int, row: int,
                        dx: int, dy: int) -> int:
        maxes, mins = 0, 0
        state = state.cols_first

        for i in [0, 1, 2, 3]:
            color = state[col + i * dx][row + i * dy]
            if color == MAX_COLOR: maxes += 1
            elif color == MIN_COLOR: mins += 1

        if maxes == 4: return INF
        elif mins == 4: return -INF
        elif maxes == 0: return -Evaluator.weights[mins]
        elif mins == 0: return Evaluator.weights[maxes]
        return 0

    @staticmethod
    def _check_next_move(state: State, judge: Judge) -> Tuple[bool, Color]:
        maxes, mins = 0, 0
        for disc in list((chain(*state.cols_first))):
            if disc == MAX_COLOR: maxes += 1
            elif disc == MIN_COLOR: mins += 1

        grid = Grid.from_state(state)
        if maxes <= mins: color, result = MAX_COLOR, INF
        else: color, result = MIN_COLOR, -INF

        for move in grid.available_moves:
            grid.move(color, move)
            over = judge.is_over_after_move_in_col(grid.state, move)
            grid.undo_move(move)
            if over: return True, color

        return False, MAX_COLOR

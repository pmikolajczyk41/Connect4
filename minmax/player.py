from threading import Event, Timer
from typing import Tuple, Union

from environment.colors import Color
from environment.game import Game
from environment.grid import State, Grid
from environment.judge import Judge
from environment.player import Player
from minmax.eval import Evaluator

INF = int(1e9)
MAX_COLOR = Color.RED
MIN_COLOR = Color.BLACK


class MinmaxPlayer(Player):
    def __init__(self, color: Color,
                 judge: Judge,
                 evaluator: Evaluator,
                 timeout: int,
                 depth: int = 10):
        self._judge = judge
        self._color = color
        self._depth = depth
        self._timeout = timeout
        self._deadline = Event()
        self._evaluate = evaluator.evaluate

    def make_move_in_state(self, state: State) -> int:
        self._deadline.clear()
        Timer(self._timeout, lambda: self._deadline.set()).start()

        return self._iterative_deepening(Grid.from_state(state))

    def _iterative_deepening(self, grid: Grid) -> int:
        assert len(grid.available_moves) > 0, 'No move available'
        best_value, best_move = -INF if self._color == MAX_COLOR else INF, None

        for depth in range(1, self._depth + 1):
            value, move = self._minmax(grid, depth, -INF, INF, self._color, None)
            if self._color == MAX_COLOR and value > best_value or \
                    self._color == MIN_COLOR and value < best_value:
                best_move, best_value = move, value

        return best_move

    def _minmax(self, grid: Grid, depth: int, alpha: int, beta: int,
                color: Color, last_move: Union[int, None]) -> Tuple[int, int]:
        """Returns (best available value, move towards best value)"""
        if self._deadline.is_set() or depth == 0 or \
                (last_move is not None and self._judge.is_over_after_move_in_col(grid.state, last_move)):
            return self._evaluate(grid.state), 0

        value = -INF if color == MAX_COLOR else INF
        best_move = None
        for move in grid.available_moves:
            grid.move(color, move)
            child_value, _ = self._minmax(grid, depth - 1, alpha, beta, Color(1 - color), move)
            grid.undo_move(move)

            if color == MAX_COLOR and child_value > value:
                best_move = move
                value = child_value
                alpha = max(alpha, value)
            elif color == MIN_COLOR and child_value < value:
                best_move = move
                value = child_value
                beta = min(beta, value)

            if alpha >= beta: break

        return value, best_move


if __name__ == '__main__':
    game = Game(Grid(), Judge(),
                MinmaxPlayer(Color.RED, Judge(), Evaluator(), 3, 7),
                MinmaxPlayer(Color.BLACK, Judge(), Evaluator(), 3, 6))
    print(game.play())

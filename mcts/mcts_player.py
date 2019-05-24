from environment.colors import Color
from environment.grid import State, Grid
from environment.judge import Judge
from environment.player import Player


class MCTSPlayer(Player):

    def __init__(self, color: Color, judge: Judge, iterations: int):
        self._color = color
        self._judge = judge
        self._iterations = iterations
        self._tree = dict()

    def make_move_in_state(self, state: State) -> int:
        grid = Grid.from_state(state)
        assert len(grid.available_moves) > 0, 'No move available'

        for _ in range(self._iterations):
            self._traverse_from(grid)

        return self._pick_most_visited_child_of(grid)

    def _pick_most_visited_child_of(self, grid: Grid) -> int:
        best_move, most_visits = None, 0
        for move in grid.available_moves:
            grid.move(self._color, move)
            visits = self._tree[grid.state].visits
            grid.undo_move(move)

            if visits > most_visits:
                most_visits, best_move = visits, move

        return best_move

    def _traverse_from(self, grid: Grid) -> None:
        pass

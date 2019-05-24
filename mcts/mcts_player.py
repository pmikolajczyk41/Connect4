from typing import Union

from environment.colors import Color
from environment.grid import State, Grid
from environment.judge import Judge
from environment.player import Player
from mcts.node_info import NodeInfo


class MCTSPlayer(Player):

    def __init__(self, color: Color, judge: Judge, iterations: int):
        self._color = color
        self._judge = judge
        self._iterations = iterations
        self._tree = dict()
        self._nodes_for_backprop = []

    def make_move_in_state(self, state: State) -> int:
        grid = Grid.from_state(state)
        assert len(grid.available_moves) > 0, 'No move available'

        if state not in self._tree.keys():
            self._tree[state] = NodeInfo(visits=0, is_leaf=True, wins=0)

        for _ in range(self._iterations):
            won = self._traverse_from(grid, self._color)
            self._backprop(won)

        return self._pick_most_visited_child_of(grid)

    def _backprop(self, won: bool) -> None:
        for s in self._nodes_for_backprop:
            node_info = self._tree[s]
            new_info = NodeInfo(wins=node_info.wins + won,
                                visits=node_info.visits + 1,
                                is_leaf=node_info.is_leaf)
            self._tree[s] = new_info
        self._nodes_for_backprop.clear()

    def _pick_most_visited_child_of(self, grid: Grid) -> int:
        best_move, most_visits = None, -1
        for move in grid.available_moves:
            grid.move(self._color, move)
            visits = self._tree[grid.state].visits
            grid.undo_move(move)

            if visits > most_visits:
                most_visits, best_move = visits, move

        return best_move

    def _select_best_child_of(self, grid: Grid, current_color: Color) -> int:
        pass

    def _traverse_from(self, grid: Grid, current_color: Color) -> bool:
        pass

    def _rollout_from(self, grid: Grid, color: Color, last_col: Union[int, None] = None) -> bool:
        pass

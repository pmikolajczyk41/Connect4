import random
from threading import Event, Timer
from typing import Union

from math import sqrt, log

from environment.colors import Color
from environment.game import Game
from environment.grid import State, Grid
from environment.judge import Judge
from environment.player import Player
from mcts.node_info import NodeInfo


class MCTSPlayer(Player):

    def __init__(self, color: Color, judge: Judge, timeout: Union[int, None], iterations: int = 0):
        self._color = color
        self._judge = judge

        if timeout is None: self._iterations = iterations
        else: self._timeout, self._deadline = timeout, Event()

        self._tree = dict()
        self._nodes_for_backprop = []

    def make_move_in_state(self, state: State) -> int:
        grid = Grid.from_state(state)
        assert len(grid.available_moves) > 0, 'No move available'

        finishing_move = self._finishing_move_in(grid)
        if finishing_move is not None: return finishing_move

        if state not in self._tree.keys():
            self._tree[state] = NodeInfo(visits=0, is_leaf=True, wins=0)

        self._compute(grid)

        return self._pick_most_visited_child_of(grid)

    def _compute(self, grid: Grid) -> None:
        if hasattr(self, '_timeout'):
            self._deadline.clear()
            Timer(self._timeout, lambda: self._deadline.set()).start()
            while not self._deadline.is_set():
                has_won = self._traverse_from(grid, self._color)
                self._backprop(has_won)
        else:
            for _ in range(self._iterations):
                has_won = self._traverse_from(grid, self._color)
                self._backprop(has_won)

    def _backprop(self, has_won: bool) -> None:
        for s in self._nodes_for_backprop:
            node_info = self._tree[s]
            new_info = NodeInfo(wins=node_info.wins + has_won,
                                visits=node_info.visits + 1,
                                is_leaf=node_info.is_leaf)
            self._tree[s] = new_info
        self._nodes_for_backprop.clear()

    def _select_best_child(self, parent: Grid, map_node_info: callable,
                           current_color: Color) -> int:
        """map_node_info should take parent's node_info and child's and return a positive float"""
        assert len(parent.available_moves) > 0, 'A leaf actually'

        parent_info = self._tree[parent.state]
        best_move, best_result = None, -1
        for move in parent.available_moves:
            child_info = self._tree[parent.grid_after_move(current_color, move).state]

            temp_result = map_node_info(parent_info, child_info)
            if temp_result > best_result:
                best_result, best_move = temp_result, move

        return best_move

    def _pick_most_visited_child_of(self, grid: Grid) -> int:
        return self._select_best_child(grid,
                                       lambda _, child_info: child_info.visits,
                                       self._color)

    def _select_best_child_of(self, grid: Grid, current_color: Color) -> int:
        def ucb(parent_info: NodeInfo, child_info: NodeInfo) -> float:
            if child_info.visits == 0: return 1e9
            return child_info.wins / child_info.visits + \
                   1.5 * sqrt(log(parent_info.visits) / child_info.visits)

        return self._select_best_child(grid, ucb, current_color)

    def _traverse_from(self, grid: Grid, current_color: Color) -> bool:
        self._nodes_for_backprop.append(grid.state)
        node_info: NodeInfo = self._tree[grid.state]
        if not node_info.is_leaf:
            move = self._select_best_child_of(grid, current_color)
            return self._traverse_from(grid.grid_after_move(current_color, move),
                                       Color(1 - current_color))

        elif len(grid.available_moves) == 0: return False
        elif node_info.visits == 0:
            return self._rollout_from(grid, current_color)
        else:
            self._tree[grid.state] = NodeInfo(wins=node_info.wins,
                                              visits=node_info.visits,
                                              is_leaf=False)
            for move in grid.available_moves:
                new_grid = grid.grid_after_move(current_color, move)
                if new_grid.state not in self._tree.keys():
                    self._tree[new_grid.state] = NodeInfo(wins=0, visits=0, is_leaf=True)

            move = random.choice(grid.available_moves)
            return self._traverse_from(grid.grid_after_move(current_color, move),
                                       Color(1 - current_color))

    def _rollout_from(self, grid: Grid, color: Color, last_col: Union[int, None] = None) -> bool:
        if len(grid.available_moves) == 0 or (last_col is None and self._judge.is_over(grid.state)) or \
                (last_col is not None and self._judge.is_over_after_move_in_col(grid.state, last_col)):
            return color != self._color

        move = random.choice(grid.available_moves)
        has_won = self._rollout_from(grid.grid_after_move(color, move),
                                     Color(1 - color), move)
        return has_won

    def _finishing_move_in(self, grid: Grid) -> Union[int, None]:
        for move in grid.available_moves:
            after_move = grid.grid_after_move(self._color, move)
            if self._judge.is_over_after_move_in_col(after_move.state, move):
                return move


if __name__ == '__main__':
    game = Game(Grid(), Judge(),
                MCTSPlayer(Color.RED, Judge(), None, 1000),
                MCTSPlayer(Color.BLACK, Judge(), None, 1000))

    print(game.play())

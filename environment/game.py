from environment.colors import Color
from environment.grid import Grid
from environment.judge import Judge
from environment.player import Player
from environment.winner import Winner
from plotting.plotter import plot_state


class Game:
    def __init__(self, grid: Grid,
                 judge: Judge,
                 first_player: Player,
                 second_player: Player,
                 first_color: Color = Color.RED):
        self._grid = grid
        self._judge = judge
        self._a_player = first_player
        self._a_color = first_color
        self._b_player = second_player
        self._b_color = Color(1 - first_color)

    def play(self) -> Winner:
        size = self._grid.nrows * self._grid.ncols
        for round in range(size // 2):
            last_col = self._move(self._a_player, self._a_color)
            plot_state(self._grid.state)
            if self._judge.is_over_after_move_in_col(self._grid.state, last_col):
                return Winner.FIRST

            last_col = self._move(self._b_player, self._b_color)
            plot_state(self._grid.state)
            if self._judge.is_over_after_move_in_col(self._grid.state, last_col):
                return Winner.SECOND

        return Winner.DRAW

    def _move(self, player: Player, color: Color):
        move = player.make_move_in_state(self._grid.state)
        self._grid.move(color, move)
        return move

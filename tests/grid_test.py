from unittest import TestCase

from environment.colors import Color
from environment.grid import Grid


class GridTest(TestCase):
    def test_empty_grid(self):
        Grid(ncols=7, nrows=6)

    def test_size(self):
        g = Grid(ncols=12, nrows=2)

        self.assertEqual(g.ncols, 12)
        self.assertEqual(g.nrows, 2)

    def test_initial_state(self):
        state = Grid(ncols=7, nrows=6).state.cols_first

        self.assertEqual(len(state), 7)
        self.assertEqual(len(state[0]), 6)

    def test_initial_state_rows_first(self):
        state = Grid(ncols=7, nrows=6).state.rows_first

        self.assertEqual(len(state), 6)
        self.assertEqual(len(state[0]), 7)

    def test_move(self):
        g = Grid()
        g.move(Color.RED, 0)
        state = g.state.cols_first

        self.assertEqual(state[0][0], Color.RED)
        self.assertIsNone(state[0][1])

    def test_move_outside(self):
        g = Grid()
        with self.assertRaises(AssertionError):
            g.move(Color.RED, 7)

    def test_overflow(self):
        g = Grid()
        for _ in range(6): g.move(Color.RED, 2)
        with self.assertRaises(AssertionError):
            g.move(Color.RED, 2)

    def test_state(self):
        g = Grid(ncols=5, nrows=4)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 1)
        g.move(Color.BLACK, 2)
        g.move(Color.RED, 4)
        g.move(Color.BLACK, 1)
        state = g.state.rows_first

        # 3  - - - - -
        # 2  - B - - -
        # 1  - R - - -
        # 0  R B B - R
        #
        #    0 1 2 3 4

        self.assertSequenceEqual([None, None, None, None, None],
                                 state[3])
        self.assertSequenceEqual([None, Color.BLACK, None, None, None],
                                 state[2])
        self.assertSequenceEqual([None, Color.RED, None, None, None],
                                 state[1])
        self.assertSequenceEqual([Color.RED, Color.BLACK, Color.BLACK, None, Color.RED],
                                 state[0])

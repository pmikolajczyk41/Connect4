from unittest import TestCase

from environment.colors import Color
from environment.grid import Grid
from environment.judge import Judge


class JudgeTest(TestCase):
    def test_horizontal_win(self):
        judge = Judge()
        g = Grid(ncols=4, nrows=4)

        g.move(Color.RED, 0)
        g.move(Color.BLACK, 0)
        g.move(Color.RED, 1)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 2)
        g.move(Color.BLACK, 2)

        self.assertFalse(judge.is_over(g.state))

        g.move(Color.RED, 3)
        self.assertTrue(judge.is_over(g.state))
        self.assertTrue(judge.is_over_horizontal(g.state))
        self.assertFalse(judge.is_over_rightdown(g.state))

    def test_vertical_win(self):
        judge = Judge()
        g = Grid(ncols=2, nrows=4)

        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)

        self.assertFalse(judge.is_over(g.state))

        g.move(Color.RED, 0)
        self.assertTrue(judge.is_over(g.state))
        self.assertTrue(judge.is_over_vertical(g.state))
        self.assertFalse(judge.is_over_horizontal(g.state))

    def test_rightup_win(self):
        judge = Judge()
        g = Grid(ncols=5, nrows=4)

        g.move(Color.RED, 1)
        g.move(Color.BLACK, 0)
        g.move(Color.RED, 2)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 3)
        g.move(Color.BLACK, 2)
        g.move(Color.RED, 3)
        g.move(Color.BLACK, 2)
        g.move(Color.RED, 3)

        # 3  - - - B -
        # 2  - - B R -
        # 1  - B B R -
        # 0  B R R R -
        #    0 1 2 3 4

        self.assertFalse(judge.is_over(g.state))

        g.move(Color.BLACK, 3)
        self.assertTrue(judge.is_over(g.state))
        self.assertTrue(judge.is_over_rightup(g.state))
        self.assertFalse(judge.is_over_rightdown(g.state))

    def test_rightdown_win(self):
        judge = Judge()
        g = Grid(ncols=5, nrows=4)

        g.move(Color.RED, 2)
        g.move(Color.BLACK, 3)
        g.move(Color.RED, 1)
        g.move(Color.BLACK, 2)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 0)

        # 3  B - - - -
        # 2  R B - - -
        # 1  R B B - -
        # 0  R R R B -
        #    0 1 2 3 4

        self.assertFalse(judge.is_over(g.state))

        g.move(Color.BLACK, 0)
        self.assertTrue(judge.is_over(g.state))
        self.assertTrue(judge.is_over_rightdown(g.state))
        self.assertFalse(judge.is_over_vertical(g.state))

    def test_from_coords(self):
        judge = Judge()
        g = Grid(ncols=5, nrows=4)

        g.move(Color.RED, 2)
        g.move(Color.BLACK, 3)
        g.move(Color.RED, 1)
        g.move(Color.BLACK, 2)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 1)
        g.move(Color.RED, 0)
        g.move(Color.BLACK, 0)

        # 3  B - - - -
        # 2  R B - - -
        # 1  R B B - -
        # 0  R R R B -
        #    0 1 2 3 4

        self.assertFalse(judge.is_over_from(g.state, 1, 2))
        self.assertFalse(judge.is_over_from(g.state, 2, 1))
        self.assertTrue(judge.is_over_from(g.state, 0, 3))
        self.assertTrue(judge.is_over_from(g.state, 3, 0))

    def test_from_last_in_empty(self):
        judge = Judge()
        g = Grid(ncols=2, nrows=2)

        with self.assertRaises(AssertionError):
            judge.is_over_after_move_in_col(g.state, 1)

    def test_middle_finishing(self):
        judge = Judge()
        g = Grid(ncols=4, nrows=2)
        g.move(Color.RED, 0)
        g.move(Color.RED, 1)
        g.move(Color.RED, 3)
        g.move(Color.RED, 2)

        self.assertTrue(judge.is_over(g.state))
        self.assertTrue(judge.is_over_after_move_in_col(g.state, 2))

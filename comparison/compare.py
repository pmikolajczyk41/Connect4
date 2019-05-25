from environment.colors import Color
from environment.game import Game
from environment.grid import Grid
from environment.judge import Judge
from environment.player import Player
from environment.winner import Winner
from mcts.mcts_player import MCTSPlayer
from minmax.eval import Evaluator
from minmax.minmax_player import MinmaxPlayer

NGAMES = 100
judge = Judge()
evaluator = Evaluator()


def create_minmax_player(timeout: int) -> MinmaxPlayer:
    return MinmaxPlayer(color=Color.RED, judge=judge,
                        evaluator=evaluator, timeout=timeout)


def create_mcts_player(timeout: int) -> MCTSPlayer:
    return MCTSPlayer(color=Color.BLACK, judge=judge, timeout=timeout)


def create_game(first_player: Player, second_player: Player,
                first_color: Color = Color.RED) -> Game:
    return Game(grid=Grid(), judge=judge,
                first_player=first_player,
                second_player=second_player,
                first_color=first_color)


def minmax_wins_with_timeout_no_reset(secs: int) -> float:
    minmax_player = create_minmax_player(secs)
    mcts_player = create_mcts_player(secs)

    minmax_win = 0
    for round in range(NGAMES // 2):
        print(f'round {round}')
        game = create_game(minmax_player, mcts_player)
        if game.play() == Winner.FIRST: minmax_win += 1

        game = create_game(mcts_player, minmax_player, Color.BLACK)
        if game.play() == Winner.SECOND: minmax_win += 1

    return minmax_win / NGAMES


def minmax_wins_with_timeout_reset(secs: int):
    minmax_win = 0
    for round in range(NGAMES // 2):
        print(f'round {round}')
        game = create_game(create_minmax_player(secs),
                           create_mcts_player(secs))
        if game.play() == Winner.FIRST: minmax_win += 1

        game = create_game(create_mcts_player(secs),
                           create_minmax_player(secs),
                           Color.BLACK)
        if game.play() == Winner.SECOND: minmax_win += 1

    return minmax_win / NGAMES


if __name__ == '__main__':
    print(f'Minmax vs MCTS winning rate '
          f'(timeout: 5s, new player for each game): {minmax_wins_with_timeout_reset(5)}')
    print(f'Minmax vs MCTS winning rate '
          f'(timeout: 5s, one player for all games): {minmax_wins_with_timeout_no_reset(5)}')

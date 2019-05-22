from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from environment.colors import Color
from environment.grid import State


def _translate_color_to_number(color: Union[None, Color]):
    if color is None: return 0
    if color == Color.RED: return 1
    return 2


def plot_state(state: State, first_player_color: Color = Color.RED) -> None:
    arr = state.rows_first
    for row_id in range(len(arr)):
        arr[row_id] = list(map(_translate_color_to_number, arr[row_id]))
    x = np.array(list(reversed(arr)))

    first_color, second_color = 'darkred', 'black'
    if first_player_color == Color.BLACK:
        first_color, second_color = second_color, first_color
    cmap = ListedColormap(['white', first_color, second_color]) if len(np.unique(x)) > 2 \
        else ListedColormap(['white', first_color])

    plt.imshow(x, cmap=cmap)
    plt.show()

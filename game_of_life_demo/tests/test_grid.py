import numpy as np
import pytest

from game_of_life_demo.game_of_life import Grid

grids = [
    (
        # Input
        [[0, 1, 0], [1, 0, 0], [0, 1, 0]],
        # Expected
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    ),
    (
        # Input
        [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
        # Expected
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ),
    (
        # Input
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        # Expected
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ),
    (
        # Input
        [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        # Expected
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    ),
    (
        # Input
        [[1, 1, 1], [0, 1, 0], [1, 1, 1]],
        # Expected
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    ),
    (
        # Input
        [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        # Expected
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    ),
    (
        # Input
        [[1, 0, 1], [0, 1, 0], [1, 0, 0]],
        # Expected
        [[1, 0, 1], [0, 1, 0], [1, 0, 0]],
    ),
]


@pytest.mark.parametrize("input_grid, expected_grid", grids)
def test_grid(mocker, input_grid, expected_grid):
    def mock_init_grid(w, h, p):
        return np.array(input_grid).reshape(h, w)

    mocker.patch("game_of_life_demo.game_of_life.init_grid", mock_init_grid)

    grid = Grid(3, 3, 1.0)
    grid.update()

    np.testing.assert_array_equal(grid.grid, expected_grid)

import pytest
from game_of_life_demo import parse_args, int_tuple
from game_of_life_demo.game_of_life import Grid
import numpy as np


variants = ["numpy", "numba"]
@pytest.mark.parametrize('variant_str', variants)
def test_variant_numpy(variant_str):
    args = parse_args(["--variant", variant_str])
    assert args.variant == variant_str


variants = ["omp", "tbb", "workqueue"]
@pytest.mark.parametrize('threading_str', variants)
def test_variant_numpy(threading_str):
    args = parse_args(["--variant", threading_str])
    assert args.threading_layer == threading_str


variants = [True, False]
@pytest.mark.parametrize('parallel', variants)
def test_variant_numpy(parallel):
    args = parse_args(["--parallel", parallel])
    assert args.parallel == parallel


variants = [0, 100]
@pytest.mark.parametrize('frames_count', variants)
def test_variant_numpy(frames_count):
    args = parse_args(["--frames-count", frames_count])
    assert args.frames_count == frames_count


variants = [True, False]
@pytest.mark.parametrize('gui', variants)
def test_variant_numpy(gui):
    args = parse_args(["--gui", gui])
    assert args.gui == gui


variants = [True, False]
@pytest.mark.parametrize('stats', variants)
def test_variant_numpy(stats):
    args = parse_args(["--stats", stats])
    assert args.stats == stats


variants = ["3, 3", "100, 100"]
@pytest.mark.parametrize('task_size', variants)
def test_variant_numpy(task_size):
    args = parse_args(["--task-size", task_size])
    assert args.task_size == int_tuple(task_size)


grids = [
    (
        # Input
        [[0, 1, 0],
         [1, 0, 0],
         [0, 1, 0]],
        # Expected
        [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]],
    ),

    (
        # Input
        [[0, 1, 0],
         [0, 0, 0],
         [0, 1, 0]],
        # Expected
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
    ),

    (
        # Input
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        # Expected
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
    ),

    (
        # Input
        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],
        # Expected
        [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]],
    ),

    (
        # Input
        [[1, 1, 1],
         [0, 1, 0],
         [1, 1, 1]],
        # Expected
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
    ),

    (
        # Input
        [[0, 0, 1],
         [0, 1, 0],
         [1, 0, 0]],
        # Expected
        [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]],
    ),

    (
        # Input
        [[1, 0, 1],
         [0, 1, 0],
         [1, 0, 0]],
        # Expected
        [[1, 0, 1],
         [0, 1, 0],
         [1, 0, 0]],
    ),

]


@pytest.mark.parametrize('input_grid, expected_grid', grids)
def test_grid(mocker, input_grid, expected_grid):
    def mock_init_grid(w, h, p):
        return np.array(input_grid).reshape(h, w)

    mocker.patch('game_of_life_demo.game_of_life.init_grid', mock_init_grid)

    grid = Grid(3, 3, 1.0)
    grid.update()

    np.testing.assert_array_equal(grid.grid, expected_grid)

import numpy as np
import pytest

from game_of_life_demo.game_of_life import Grid
from game_of_life_demo import int_tuple
from game_of_life_demo import parse_args


@pytest.mark.parametrize("variant_str", ["numpy", "numba"])
def test_variant(variant_str):
    args = parse_args(["--variant", variant_str])
    assert args.variant == variant_str


@pytest.mark.parametrize("threading_str", ["omp", "tbb", "workqueue"])
def test_threading(threading_str):
    args = parse_args(["--threading-layer", threading_str])
    assert args.threading_layer == threading_str


@pytest.mark.parametrize("frames_count", [0, 100])
def _test_frames_count(frames_count):
    args = parse_args(["--frames-count", frames_count])
    assert args.frames_count == frames_count


@pytest.mark.parametrize("task_size", ["3, 3", "100, 100"])
def test_task_size(task_size):
    args = parse_args(["--task-size", task_size])
    assert args.task_size == int_tuple(task_size)


def test_parallel_true():
    args = parse_args(["--parallel"])
    assert args.parallel


def test_parallel_false():
    args = parse_args(["--no-parallel"])
    assert not args.parallel


def test_gui_true():
    args = parse_args(["--gui"])
    assert args.gui


def test_gui_false():
    args = parse_args(["--no-gui"])
    assert not args.gui


def test_stats_true():
    args = parse_args(["--stats"])
    assert args.stats


def test_stats_false():
    args = parse_args(["--no-stats"])
    assert not args.stats


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

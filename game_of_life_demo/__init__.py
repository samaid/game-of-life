import argparse
from time import time

DISPLAY_RES = DISPLAY_W, DISPLAY_H = 800, 600
CELL_COLOR = (0, 255, 0)
CELL_SIZE = 1
TEXT_BOX_TOP_LEFT = (5, 7)
TEXT_BOX_BOTTOM_RIGHT = (420, 110)

GRID_W, GRID_H = DISPLAY_W // CELL_SIZE, DISPLAY_H // CELL_SIZE

PROB_ON = 0.2

ESC_KEYCODE = 27
WINDOW_NAME = "Conway's Game of life"

MAX_FRAME = 2000


def int_tuple(tuple_str):
    return tuple(map(int, tuple_str.split(",")))


def time_meter(last, total):
    def _time_meter(func):
        def impl(self, *args, **kwargs):
            start = time()
            res = func(self, *args, **kwargs)
            end = time()
            self.time[last] = end - start
            self.time[total] += end - start

            return res

        return impl

    return _time_meter


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "--variant",
        help="Implementation variant",
        type=str.casefold,
        choices=["numpy", "numba"],
        default="numpy",
    )
    parser.add_argument(
        "--threading-layer",
        help="Threading layer",
        choices=["omp", "tbb", "workqueue"],
        default="omp",
    )
    parser.add_argument(
        "--parallel",
        help="Keyword argument parallel= for @njit. Used along with --variant numba. Default --no-parallel",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--frames-count",
        help="Stop game after specified amount of frames (default 0 - no stop frame)",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--gui",
        help="Render the evolution of the grid or do computation only and "
        "print statistics in the end. Default --no-gui",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--stats",
        help="Either display statistics in gui while running or not. Default --no-stats",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--task-size",
        help=f"Size of the grid. E.g. 1200,800. Default {GRID_W},{GRID_H}",
        type=int_tuple,
        default=int_tuple(f"{GRID_W},{GRID_H}"),
    )

    args = parser.parse_args(argv)
    return args


RUN_VERSION = parse_args().variant

if RUN_VERSION == "Numba".casefold():
    from numba import config

    from game_of_life_demo.impl_numba import grid_update
    from game_of_life_demo.impl_numba import init_grid

    config.THREADING_LAYER = parse_args().threading_layer
elif RUN_VERSION == "NumPy".casefold():
    from game_of_life_demo.impl_numpy import grid_update
    from game_of_life_demo.impl_numpy import init_grid


def variant_str():
    if RUN_VERSION == "Numba".casefold():
        return f"Numba, threading layer: {parse_args().threading_layer}, parallel: {parse_args().parallel}"
    else:
        return "NumPy"

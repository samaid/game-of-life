import argparse
from time import time

DISPLAY_RES = DISPLAY_W, DISPLAY_H = 1200, 800
CELL_COLOR = (0, 255, 0)
CELL_SIZE = 1

GRID_W, GRID_H = DISPLAY_W // CELL_SIZE, DISPLAY_H // CELL_SIZE

PROB_ON = 0.2

ESC_KEYCODE = 27
WINDOW_NAME = "Game of life"


def int_tuple(input):
    return tuple(map(int, input.split(",")))


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


parser = argparse.ArgumentParser(description="Conway's Game of Life")
parser.add_argument(
    "--variant",
    help="Implementation variant",
    type=str.casefold,
    choices=["numba", "numpy"],
    default="numba",
)
parser.add_argument(
    "--threading-layer",
    help="Threading layer",
    choices=["omp", "tbb", "workqueue"],
    default="omp",
)
parser.add_argument(
    "--parallel",
    help="Keyword argument parallel= for @njit. Used along with --variant numba",
    action=argparse.BooleanOptionalAction,
    default=False,
)
parser.add_argument(
    "--frames-count",
    help="Stop game after specified amount of frames",
    type=int,
    default=0,
)
parser.add_argument(
    "--gui",
    help="Render the evolution of the grid or do computation only and "
    "print statistics in the end",
    action=argparse.BooleanOptionalAction,
    default=True,
)
parser.add_argument(
    "--stats",
    help="Either display statistics in gui while running or not.",
    action=argparse.BooleanOptionalAction,
    default=True,
)
parser.add_argument(
    "--task-size",
    help="Size of the grid. E.g. 1200,800",
    type=int_tuple,
    default=int_tuple(f"{GRID_W},{GRID_H}"),
)

args = parser.parse_args()

RUN_VERSION = args.variant

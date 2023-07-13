import argparse

from game_of_life_demo import int_tuple


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "--variant",
        help="Implementation variant",
        type=str.casefold,
        choices=["numpy", "numba", "dpnp", "numba-dpex"],
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
        help="Keyword argument parallel= for @njit. Used along with --variant numba. If not specified runs sequentially",
        action="store_true",
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
        "print statistics in the end. If not specified runs without gui",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--gpu",
        help="Runs computation on gpu. Applicable for numba-dpex and dpnp variants only. "
        "Can't be specified together with --cpu option. "
        "If not specified decision would be made automatically",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--cpu",
        help="Runs computation on cpu. Applicable for numba-dpex and dpnp variants only. "
        "Can't be specified together with --gpu option. "
        "If not specified decision would be made automatically",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--stats",
        help="Either display statistics in gui while running or not. If not specified no stats displayed",
        action="store_true",
        default=False,
    )
    w = 960
    h = 540
    parser.add_argument(
        "--task-size",
        help=f"Size of the grid. E.g. 1200,800. Default {w},{h}",
        type=int_tuple,
        default=int_tuple(f"{w},{h}"),
    )

    args, _ = parser.parse_known_args(argv)
    return args

# Conway's Game Of Life

The Game of Life is a cellular automaton devised by John Horton Conway in 1970.
It is a zero-player game,[2][3] meaning that its evolution is determined by its initial state.
One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

![Game Of Life Demo](https://github.com/samaid/GameOfLife/blob/main/images/game-of-life-lowres.gif)

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states,
live or dead (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent. At each step in time, the following transitions occur:

* Any live cell with fewer than two live neighbours dies, as if by underpopulation.
* Any live cell with two or three live neighbours lives on to the next generation.
* Any live cell with more than three live neighbours dies, as if by overpopulation.
* Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

These rules, which compare the behaviour of the automaton to real life, can be condensed into the following:

* Any live cell with two or three live neighbours survives.
* Any dead cell with three live neighbours becomes a live cell.
* All other live cells die in the next generation. Similarly, all other dead cells stay dead.

The initial pattern constitutes the seed of the system.
The first generation is created by applying the above rules simultaneously to every cell in the seed,
live or dead; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick.
Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.

For further details please address [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

Running demo
************
From command line type:
`python game_of_life.py  [command line options]`

* `--variant [numba, numpy]`, default `numba` - implementation variant
* `--threading-layer [omp, tbb, workqueue]`, default `omp` - threading layer for `numba` implementation
* `--parallel` or `--no-parallel` - keyword argument `parallel=` for `@njit`. Used along with `--variant numba`
parser.add_argument('--frames-count', help="Stop game after specified amount of frames", type=int, default=0)
parser.add_argument('--gui', help="Render the evolution of the grid or do computation only and "
                                  "print statistics in the end", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--stats', help="Either display statistics in gui while running or not.",
                    action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--task-size', help="Size of the grid. E.g. 1200,800",
                    type=int_tuple, default=int_tuple(f"{GRID_W},{GRID_H}"))

from settings import *
from time import time
import argparse

parser = argparse.ArgumentParser(description="Conway's Game of Life")
parser.add_argument("--variant", help="Implementation variant. Can be either NumPy or Numba", default="Numba")
parser.add_argument("--threading-layer", help="Threading layer. Can be either omp, tbb, or workqueue", default="omp")
parser.add_argument("--parallel", help="Keyword argument parallel= for @njit. Can be True or False. Used along with --variant Numba", type=bool, default=False)
args = parser.parse_args()

RUN_VERSION = args.variant

IMG_MONSTER = None

if RUN_VERSION == "Numba":
    import numpy as np
    from numba import njit, prange, config

    config.THREADING_LAYER = args.threading_layer

    rules = np.array([
        # 0  1  2  3  4  5  6  7  8   # Number of alive cell neighbors
        [0, 0, 0, 1, 0, 0, 0, 0, 0],  # Rule for dead cells
        [0, 0, 1, 1, 0, 0, 0, 0, 0],  # Rule for alive cells
    ])

    def _init_grid(w, h, p):
        return np.random.choice((0, 1), w * h, p=(1.0 - p, p)).reshape(h, w)

    @njit(["int32[:,:](int32[:,:])"], parallel=args.parallel)
    def _grid_update(grid):
        m, n = grid.shape
        grid_out = np.empty_like(grid)
        grid_padded = np.empty((m+2, n+2), dtype=grid.dtype)
        grid_padded[1:-1, 1:-1] = grid  # copy input grid into the center of padded one
        grid_padded[0, 1:-1] = grid[-1]  # top row of padded grid
        grid_padded[-1, 1:-1] = grid[0]  # bottom
        grid_padded[1:-1, 0] = grid[:, -1]
        grid_padded[1:-1, -1] = grid[:, 0]
        grid_padded[0, 0] = grid[-1, -1]
        grid_padded[-1, -1] = grid[0, 0]
        grid_padded[0, -1] = grid[-1, 0]
        grid_padded[-1, 0] = grid[0, -1]
        for i in prange(m):
            for j in range(n):
                v_self = grid[i, j]
                neighbor_population = grid_padded[i:i+3, j:j+3].sum() - v_self
                grid_out[i, j] = rules[v_self, neighbor_population]
        return grid_out


if RUN_VERSION == "NumPy":
    import numpy as np

    rules = np.array([
        # 0  1  2  3  4  5  6  7  8   # Number of alive cell neighbors
        [0, 0, 0, 1, 0, 0, 0, 0, 0],  # Rule for dead cells
        [0, 0, 1, 1, 0, 0, 0, 0, 0],  # Rule for alive cells
    ])

    def _init_grid(w, h, p):
        return np.random.choice((0, 1), w * h, p=(1.0 - p, p)).reshape(h, w)


    def _grid_update(grid):
        m, n = grid.shape
        grid_out = np.empty_like(grid)
        grid_padded = np.empty((m+2, n+2), dtype=grid.dtype)
        grid_padded[1:-1, 1:-1] = grid  # copy input grid into the center of padded one
        grid_padded[0, 1:-1] = grid[-1]  # top row of padded grid
        grid_padded[-1, 1:-1] = grid[0]  # bottom
        grid_padded[1:-1, 0] = grid[:, -1]
        grid_padded[1:-1, -1] = grid[:, 0]
        grid_padded[0, 0] = grid[-1, -1]
        grid_padded[-1, -1] = grid[0, 0]
        grid_padded[0, -1] = grid[-1, 0]
        grid_padded[-1, 0] = grid[0, -1]
        for i in range(m):
            for j in range(n):
                v_self = grid[i, j]
                neighbor_population = grid_padded[i:i+3, j:j+3].sum() - v_self
                grid_out[i, j] = rules[v_self, neighbor_population]
        return grid_out


class Grid:
    def __init__(self, w, h, p):
        self.w = w
        self.h = h
        self.grid = _init_grid(w, h, p)

    def draw(self, sc):
        sc.fill(pg.Color('black'))

        y = 0
        for i in range(self.h):
            x = 0
            for j in range(self.w):
                if self.grid[i, j]:
                    sc.blit(IMG_MONSTER, (x, y))
                x += CELL_SIZE
            y += CELL_SIZE

    def update(self):
        self.grid = _grid_update(self.grid)


def main():
    ds, clk = initialize()
    global IMG_MONSTER

    IMG_MONSTER = pg.image.load("monster.png").convert()
    IMG_MONSTER.set_colorkey("white")
    IMG_MONSTER = pg.transform.scale(IMG_MONSTER, (CELL_SIZE, CELL_SIZE))

    grid = Grid(GRID_W, GRID_H, PROB_ON)

    t1 = time()
    frames = 0
    do_game = True
    while do_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                do_game = False

        # Draw objects
        grid.draw(ds)

        # Perform updates
        grid.update()

        # Prepare for next frame
        pg.display.flip()
        clk.tick(FPS)
        frames += 1
        if frames == 2000:
            break
    t2 = time()
    print("Average FPS =", frames/(t2-t1))
    pg.quit()
    #_grid_update.parallel_diagnostics(level=4)




if __name__ == "__main__":
    main()

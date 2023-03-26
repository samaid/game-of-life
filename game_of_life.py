from settings import *
from time import time
import argparse


ESC_KEYCODE = 27
WINDOW_NAME = 'Game of life'

def int_tuple(input):
    return tuple(map(int, input.split(',')))

parser = argparse.ArgumentParser(description="Conway's Game of Life")
parser.add_argument("--variant", help="Implementation variant. Can be either NumPy or Numba", type=str.casefold, choices=["numba", "numpy"], default="Numba")
parser.add_argument("--threading-layer", help="Threading layer. Can be either omp, tbb, or workqueue", default="omp")
parser.add_argument('--parallel', help="Keyword argument parallel= for @njit. Used along with --variant Numba", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('--frames-count', help="Stop game after specified amount of frames", type=int, default=0)
parser.add_argument('--gui', help="Either draw result or do only calculations", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--stats', help="Either display statistics in gui while running or not.", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument('--task-size', help="Size of the grid. E.g. 1200,800", type=int_tuple, default=int_tuple(f"{GRID_W},{GRID_H}"))

args = parser.parse_args()

RUN_VERSION = args.variant

if args.gui:
    import cv2

if RUN_VERSION == "Numba".casefold():
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

    @njit(["int32[:,:](int32[:,:])", "int64[:,:](int64[:,:])"], parallel=args.parallel)
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


if RUN_VERSION == "NumPy".casefold():
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
    draw_last = "draw_time_last"
    draw_total = "draw_time_total"

    update_last = "update_time_last"
    update_total = "update_time_total"

    if args.gui:
        font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 1
    font_color = (0,0,255) # BGR(A)
    font_height = 30
    text_y_initial_pos = 25
    text_x_initial_pos = 10

    def __init__(self, w, h, p):
        self.w = w
        self.h = h
        self.time = {self.draw_last: 0, self.draw_total: 0, self.update_last: 0, self.update_total: 0}
        self.grid = _init_grid(w, h, p)

    @staticmethod
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

    def y_pos_from_line(self, line):
        return self.text_y_initial_pos + self.font_height*line

    def putText(self, img, text, line, x_pos = text_x_initial_pos):
        y_pos = self.y_pos_from_line(line)
        cv2.putText(img, text, (x_pos, y_pos), self.font, self.font_scale, self.font_color)

    def statistics_line(self, img, name, line, fps, time):
        y_pos = self.y_pos_from_line(line)
        # no monospace fonts in OpenCV
        self.putText(img, name, line)
        self.putText(img, "FPS|time(ms)", line, 250)
        self.putText(img, f"{fps:4.1f}|{int(1000*time)}", line, 500)

    def implemetation_string(self):
        if RUN_VERSION == "Numba".casefold():
            return f"Numba, threading layer: {args.threading_layer}, parallel: {args.parallel}"
        else:
            return 'NumPy'

    def task_size_string(self):
        return f"Task size {self.w}x{self.h}"

    def get_statistics(self, frame_count):
        update_time = self.time[self.update_last]
        update_tpf = self.time[self.update_total]/frame_count
        draw_time = self.time[self.draw_last]
        draw_tpf = self.time[self.draw_total]/frame_count
        total_time = update_time + draw_time
        total_tpf = update_tpf + draw_tpf

        return update_time, update_tpf, draw_time, draw_tpf, total_time, total_tpf

    def draw_statistics(self, img, frame_count):
        update_time, update_tpf, draw_time, draw_tpf, total_time, total_tpf = self.get_statistics(frame_count)

        self.putText(img, self.implemetation_string(), 0)
        self.putText(img, self.task_size_string(), 1)
        self.putText(img, f"Frames: {(frame_count//10)*10}", 2)
        self.statistics_line(img, "Computation", 3, 1/update_tpf, update_time)
        self.statistics_line(img, "Draw", 4, 1/draw_tpf, draw_time)
        self.statistics_line(img, "Total", 5, 1/total_tpf, total_time)

    @time_meter(draw_last, draw_total)
    def draw(self, window_name, show_statistics, frame_count):
        # check if window was closed
        if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
            return False

        img = np.zeros(shape=self.grid.shape + (3,), dtype=np.uint8)
        img[:,:,1] = 255*self.grid
        img = cv2.resize(img,  (DISPLAY_W, DISPLAY_H), interpolation=cv2.INTER_NEAREST)

        if show_statistics and frame_count > 0:
            self.draw_statistics(img, frame_count)

        cv2.imshow(window_name, img)
        cv2.resizeWindow(WINDOW_NAME, DISPLAY_W, DISPLAY_H)

        # Check if Escape button was pressed
        if cv2.pollKey() == ESC_KEYCODE:
            return False

        return True

    @time_meter(update_last, update_total)
    def update(self):
        self.grid = _grid_update(self.grid)


def main():
    np.random.seed(0)

    draw_result = args.gui

    GRID_W, GRID_H = args.task_size
    grid = Grid(GRID_W, GRID_H, PROB_ON)

    if draw_result:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow(WINDOW_NAME, DISPLAY_W, DISPLAY_H)

    frames = 0
    do_game = True

    stop_frame = args.frames_count
    if stop_frame == 0 and not draw_result:
        stop_frame = 2000

    print(grid.implemetation_string())
    print(grid.task_size_string())

    while do_game:
        if draw_result:
            # Draw objects
            do_game = grid.draw(WINDOW_NAME, args.stats, frames)

        # Perform updates
        grid.update()

        frames += 1

        if stop_frame > 0 and frames >= stop_frame:
            break

    _, update_tpf, _, draw_tpf, _, total_tpf = grid.get_statistics(frames)
    print(f"Total frames {frames}")
    print("Average fps:")
    print(f"    Computation {1/update_tpf:4.1f}")
    if draw_result:
        print(f"    Draw        {1/draw_tpf:4.1f}")
        print(f"    Total       {1/total_tpf:4.1f}")

    #_grid_update.parallel_diagnostics(level=4)


if __name__ == "__main__":
    main()

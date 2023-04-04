import numpy as np

from game_of_life_demo import DISPLAY_H
from game_of_life_demo import DISPLAY_W
from game_of_life_demo import ESC_KEYCODE
from game_of_life_demo import MAX_FRAME
from game_of_life_demo import PROB_ON
from game_of_life_demo import TEXT_BOX_BOTTOM_RIGHT
from game_of_life_demo import TEXT_BOX_TOP_LEFT
from game_of_life_demo import WINDOW_NAME
from game_of_life_demo import grid_update
from game_of_life_demo import init_grid
from game_of_life_demo import parse_args
from game_of_life_demo import time_meter
from game_of_life_demo import variant_str

try:
    import cv2

    GUI_FLAG = True
except ModuleNotFoundError:
    GUI_FLAG = False


VISUALIZE_GAME = parse_args().gui and GUI_FLAG


class Grid:
    draw_last = "draw_time_last"
    draw_total = "draw_time_total"

    update_last = "update_time_last"
    update_total = "update_time_total"

    def __init__(self, w, h, p):
        self.w = w
        self.h = h
        self.time = {
            self.draw_last: 0,
            self.draw_total: 0,
            self.update_last: 0,
            self.update_total: 0,
        }
        if parse_args().gui:
            self.font = cv2.FONT_HERSHEY_TRIPLEX
            self.font_scale = 0.5
            self.font_color = (255, 255, 255)  # BGR(A)
            self.font_height = 15
        else:
            self.font = None
            self.font_scale = None
            self.font_color = None
            self.font_height = None

        self.grid = init_grid(w, h, p)

    def y_pos_from_line(self, line):
        return TEXT_BOX_TOP_LEFT[1] + self.font_height * line + 10

    def putText(self, img, text, line, x_pos=10):
        y_pos = self.y_pos_from_line(line)
        cv2.putText(
            img, text, (x_pos, y_pos), self.font, self.font_scale, self.font_color, 2
        )

    def statistics_line(self, img, name, line, fps, time):
        # no monospace fonts in OpenCV
        self.putText(img, name, line)
        self.putText(img, "FPS|time(ms)", line, 150)
        self.putText(img, f"{fps:4.1f}|{int(1000*time)}", line, 300)

    @staticmethod
    def variant_string():
        return variant_str()

    def task_size_string(self):
        return f"Task size {self.w}x{self.h}"

    def get_statistics(self, frame_count):
        update_time = self.time[self.update_last]
        update_tpf = self.time[self.update_total] / frame_count
        draw_time = self.time[self.draw_last]
        draw_tpf = self.time[self.draw_total] / frame_count
        total_time = update_time + draw_time
        total_tpf = update_tpf + draw_tpf

        return update_time, update_tpf, draw_time, draw_tpf, total_time, total_tpf

    def draw_statistics(self, img, frame_count):
        (
            update_time,
            update_tpf,
            draw_time,
            draw_tpf,
            total_time,
            total_tpf,
        ) = self.get_statistics(frame_count)

        p1 = TEXT_BOX_TOP_LEFT
        p2 = TEXT_BOX_BOTTOM_RIGHT

        sub_img = img[p1[1] : p2[1], p1[0] : p2[0]]
        black_bg = np.zeros(sub_img.shape, dtype=np.uint8)
        img[p1[1] : p2[1], p1[0] : p2[0]] = cv2.addWeighted(
            sub_img, 0.5, black_bg, 0.5, 1.0
        )
        self.putText(img, self.variant_string(), 0)
        self.putText(img, self.task_size_string(), 1)
        self.putText(img, f"Frames: {(frame_count//10)*10}", 2)
        self.statistics_line(img, "Computation", 3, 1 / update_tpf, update_time)
        self.statistics_line(img, "Draw", 4, 1 / draw_tpf, draw_time)
        self.statistics_line(img, "Total", 5, 1 / total_tpf, total_time)

    @time_meter(draw_last, draw_total)
    def draw(self, show_statistics, frame_count):
        # check if window was closed
        if not cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE):
            return False

        img = np.zeros(shape=self.grid.shape + (3,), dtype=np.uint8)
        img[:, :, 1] = 255 * self.grid
        img = cv2.resize(img, (DISPLAY_W, DISPLAY_H), interpolation=cv2.INTER_NEAREST)

        if show_statistics and frame_count > 0:
            self.draw_statistics(img, frame_count)

        cv2.imshow(WINDOW_NAME, img)
        cv2.resizeWindow(WINDOW_NAME, DISPLAY_W, DISPLAY_H)

        # Check if Escape button was pressed
        if cv2.pollKey() == ESC_KEYCODE:
            return False

        return True

    @time_meter(update_last, update_total)
    def update(self):
        self.grid = grid_update(self.grid)


def create_window():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_W, DISPLAY_H)


def main(argv=None):
    np.random.seed(777777777)

    w, h = parse_args(argv).task_size
    grid = Grid(w, h, PROB_ON)

    if VISUALIZE_GAME:
        create_window()

    frames = 0
    do_game = True

    stop_frame = parse_args(argv).frames_count
    if stop_frame == 0 and not VISUALIZE_GAME:
        stop_frame = MAX_FRAME

    print(grid.variant_string())
    print(grid.task_size_string())

    while do_game:
        # Draw objects
        if VISUALIZE_GAME:
            do_game = grid.draw(parse_args().stats, frames)

        # Perform updates
        grid.update()

        frames += 1

        if 0 < stop_frame <= frames:
            break

    _, update_tpf, _, draw_tpf, _, total_tpf = grid.get_statistics(frames)
    print(f"Total frames {frames}")
    print("Average fps:")
    print(f"    Computation {1/update_tpf:4.1f}")
    if VISUALIZE_GAME:
        print(f"    Draw        {1/draw_tpf:4.1f}")
        print(f"    Total       {1/total_tpf:4.1f}")

    # _grid_update.parallel_diagnostics(level=4)


if __name__ == "__main__":
    main()

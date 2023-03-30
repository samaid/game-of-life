from init import parse_args, time_meter  # NOQA

if parse_args().gui:
    import cv2

RUN_VERSION = parse_args().variant


from init import PROB_ON, RUN_VERSION, args, time_meter  # NOQA

if RUN_VERSION == "Numba".casefold():
    import numpy as np
    from impl_numba import grid_update, init_grid
    from numba import config

    config.THREADING_LAYER = parse_args().threading_layer
elif RUN_VERSION == "NumPy".casefold():
    import numpy as np

    from impl_numpy import grid_update, init_grid

from init import DISPLAY_H, DISPLAY_W, ESC_KEYCODE, WINDOW_NAME


class Grid:
    draw_last = "draw_time_last"
    draw_total = "draw_time_total"

    update_last = "update_time_last"
    update_total = "update_time_total"

    if args.gui:
        font = cv2.FONT_HERSHEY_TRIPLEX  # Select font
    font_scale = 0.5
    font_color = (255, 255, 255)  # BGR(A)
    font_height = 15
    text_y_initial_pos = 25
    text_x_initial_pos = 10

    def __init__(self, w, h, p):
        self.w = w
        self.h = h
        self.time = {
            self.draw_last: 0,
            self.draw_total: 0,
            self.update_last: 0,
            self.update_total: 0,
        }
        self.grid = init_grid(w, h, p)

    def y_pos_from_line(self, line):
        return self.text_y_initial_pos + self.font_height * line

    def putText(self, img, text, line, x_pos=text_x_initial_pos):
        y_pos = self.y_pos_from_line(line)
        cv2.putText(
            img, text, (x_pos, y_pos), self.font, self.font_scale, self.font_color, 2
        )

    def statistics_line(self, img, name, line, fps, time):
        # no monospace fonts in OpenCV
        self.putText(img, name, line)
        self.putText(img, "FPS|time(ms)", line, 150)
        self.putText(img, f"{fps:4.1f}|{int(1000*time)}", line, 300)

    def implemetation_string(self):
        if RUN_VERSION == "Numba".casefold():
            return f"Numba, threading layer: {parse_args().threading_layer}, parallel: {parse_args().parallel}"
        else:
            return "NumPy"

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

        p1 = (5, 7)
        p2 = (420, 110)
        sub_img = img[p1[1] : p2[1], p1[0] : p2[0]]
        black_bg = np.zeros(sub_img.shape, dtype=np.uint8)
        img[p1[1] : p2[1], p1[0] : p2[0]] = cv2.addWeighted(
            sub_img, 0.5, black_bg, 0.5, 1.0
        )
        self.putText(img, self.implemetation_string(), 0)
        self.putText(img, self.task_size_string(), 1)
        self.putText(img, f"Frames: {(frame_count//10)*10}", 2)
        self.statistics_line(img, "Computation", 3, 1 / update_tpf, update_time)
        self.statistics_line(img, "Draw", 4, 1 / draw_tpf, draw_time)
        self.statistics_line(img, "Total", 5, 1 / total_tpf, total_time)

    @time_meter(draw_last, draw_total)
    def draw(self, window_name, show_statistics, frame_count):
        # check if window was closed
        if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
            return False

        img = np.zeros(shape=self.grid.shape + (3,), dtype=np.uint8)
        img[:, :, 1] = 255 * self.grid
        img = cv2.resize(img, (DISPLAY_W, DISPLAY_H), interpolation=cv2.INTER_NEAREST)

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
        self.grid = grid_update(self.grid)


def main():
    np.random.seed(0)

    draw_result = parse_args().gui

    GRID_W, GRID_H = parse_args().task_size
    grid = Grid(GRID_W, GRID_H, PROB_ON)

    if draw_result:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow(WINDOW_NAME, DISPLAY_W, DISPLAY_H)

    frames = 0
    do_game = True

    stop_frame = parse_args().frames_count
    if stop_frame == 0 and not draw_result:
        stop_frame = 2000

    print(grid.implemetation_string())
    print(grid.task_size_string())

    while do_game:
        if draw_result:
            # Draw objects
            do_game = grid.draw(WINDOW_NAME, parse_args().stats, frames)

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

    # _grid_update.parallel_diagnostics(level=4)


if __name__ == "__main__":
    main()

import os
import pygame as pg

DISPLAY_RES = DISPLAY_W, DISPLAY_H = 1200, 800
CELL_COLOR = (0, 255, 0)
CELL_SIZE = 2
FPS = 800

GRID_W, GRID_H = DISPLAY_W//CELL_SIZE, DISPLAY_H//CELL_SIZE

PROB_ON = 0.2


def set_display():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    surface = pg.display.set_mode(DISPLAY_RES, pg.SCALED)
    clock = pg.time.Clock()

    return surface, clock


def initialize():
    surface, clock = set_display()
    return surface, clock

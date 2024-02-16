#! python3

from graphics import Window
from maze import Maze

def main():
    num_rows = 40
    num_cols = 40
    margin = 20
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed = 0)

    win.wait_for_close()

main()

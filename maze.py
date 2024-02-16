from cell import Cell
import random
import time


class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None): 
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is None:
            self._seed = random.seed(0)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            row = []
            for j in range(self._num_rows):
                row.append(Cell(i * self._cell_size_x, j * self._cell_size_y, self._cell_size_x, self._cell_size_y, self._win))
            self._cells.append(row)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()


    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True
        while True:
            unvisited = []
            # up
            if i > 0 and not self._cells[i - 1][j].visited:
                unvisited.append((i - 1, j))
            # down
            if i < len(self._cells) - 1 and not self._cells[i + 1][j].visited:
                unvisited.append((i + 1, j))
            # left
            if j > 0 and not self._cells[i][j - 1].visited:
                unvisited.append((i, j - 1))
            # right
            if j < len(self._cells[0]) - 1 and not self._cells[i][j + 1].visited:
                unvisited.append((i, j + 1))
            
            if unvisited == []:
                return
            
            next_i, next_j = unvisited[random.randrange(len(unvisited))]
            self._break_wall_between((i, j), (next_i, next_j))
            self._break_walls_r(next_i, next_j)

    def _break_wall_between(self, cell1, cell2):
        c1 = self._cells[cell1[0]][cell1[1]]
        c2 = self._cells[cell2[0]][cell2[1]]

        dx = cell2[0] - cell1[0]
        dy = cell2[1] - cell1[1]
        
        if dx == 1:  # cell2 is to the right of cell1
            c1.has_right_wall = False
            c2.has_left_wall = False
        elif dx == -1:  # cell2 is to the left of cell1
            c1.has_left_wall = False
            c2.has_right_wall = False
        elif dy == 1:  # cell2 is below cell1
            c1.has_bottom_wall = False
            c2.has_top_wall = False
        elif dy == -1:  # cell2 is above cell1
            c1.has_top_wall = False
            c2.has_bottom_wall = False

        # redraw cells 
        self._draw_cell(cell1[0], cell1[1])
        self._draw_cell(cell2[0], cell2[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        # last cell
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # left
        if (i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].visited):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # right
        if (i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].visited):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # up
        if (j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].visited):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # down
        if (j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].visited):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False

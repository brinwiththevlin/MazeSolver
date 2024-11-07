from time import sleep
from graphics import Cell, Window
import random

SLEEP_TIME = 0.005
class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        rows: int,
        cols: int,
        cell_size_x: int,
        cell_size_y: int,
        seed: int = 8451,
        win: Window | None = None,
    ):
        random.seed(seed)
        self._x1 = x1
        self._y1 = y1
        self._cell_size_y = cell_size_y
        self._cell_size_x = cell_size_x
        self.rows = rows
        self.cols = cols
        self.win = win
        self._cells: list[list[Cell]] = self._create_cells()

        self._draw_cells()
        self._break_entrance_and_exit()
        self._break_walls(random.choice(range(rows)), random.choice(range(cols)))
        self._reset_cells_visited()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int):
        self._animate()
        self._cells[i][j].visited = True

        if i == self.cols - 1 and j == self.rows - 1:
            return True

        for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if self.can_move(i, j, x, y):
                self._cells[i][j].draw_move(self._cells[x][y])
                if self._solve_r(x, y):
                    return True
                else:
                    self._cells[i][j].draw_move(self._cells[x][y], undo=True)
                    sleep(SLEEP_TIME)

        return False

    def can_move(self, i: int, j: int, x: int, y: int):
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return False

        if self._cells[x][y].visited:
            return False

        match abs(2 * (x - i) + (y - j) - 1):
            case 0:
                left = self._cells[i][j].has_bottom_wall
                right = self._cells[x][y].has_top_wall
                return not left and not right
            case 1:
                left = self._cells[i][j].has_right_wall
                right = self._cells[x][y].has_left_wall
                return not left and not right
            case 2:
                left = self._cells[i][j].has_top_wall
                right = self._cells[x][y].has_bottom_wall
                return not left and not right
            case 3:
                left = self._cells[i][j].has_left_wall
                right = self._cells[x][y].has_right_wall
                return not left and not right

    def _create_cells(self) -> list[list[Cell]]:
        cells: list[list[Cell]] = []
        for i in range(self.cols):
            x1 = self._x1 + i * self._cell_size_x
            col: list[Cell] = []
            for j in range(self.rows):
                y1 = self._y1 + j * self._cell_size_y
                col.append(
                    Cell(
                        x1, y1, x1 + self._cell_size_x, y1 + self._cell_size_y, self.win
                    )
                )
            cells.append(col)
        return cells

    def _draw_cells(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        if self.win:
            self.win.redraw()
        sleep(SLEEP_TIME)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        sleep(SLEEP_TIME)
        self._cells[self.cols - 1][self.rows - 1].has_right_wall = False
        self._draw_cell(self.cols - 1, self.rows - 1)
        sleep(SLEEP_TIME)

    def _break_walls(self, i: int, j: int):
        self._cells[i][j].visited = True
        while True:
            to_visit: list[tuple[int, int]] = []
            for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= x < self.cols and 0 <= y < self.rows:
                    if not self._cells[x][y].visited:
                        to_visit.append((x, y))
            if not to_visit:
                self._draw_cell(i, j)
                return
            c, r = random.choice(to_visit)
            match abs(2 * (c - i) + (r - j) - 1):
                case 0:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[c][r].has_top_wall = False
                case 1:
                    self._cells[i][j].has_right_wall = False
                    self._cells[c][r].has_left_wall = False
                case 2:
                    self._cells[i][j].has_top_wall = False
                    self._cells[c][r].has_bottom_wall = False
                case 3:
                    self._cells[i][j].has_left_wall = False
                    self._cells[c][r].has_right_wall = False

            self._break_walls(c, r)

    def _reset_cells_visited(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self._cells[i][j].visited = False

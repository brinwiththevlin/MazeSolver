from tkinter import Tk, BOTH, Canvas
from typing import Generator


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __iter__(self) -> Generator[float, None, None]:
        yield self.x
        yield self.y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def __iter__(self) -> Generator[float, None, None]:
        yield from self.p1
        yield from self.p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(*self, fill=fill_color, width=2)



class Window:
    def __init__(self, width, height) -> None:
        self._root: Tk = Tk()
        self._root.title("Maze solver")
        self._canvas = Canvas(self._root, bg="white", height=height, width=width)
        self._canvas.pack(fill=BOTH, expand=1)
        self._running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self) -> None:
        self._running = True
        while self._running:
            self.redraw()
        print("window closed...")

    def close(self) -> None:
        self._running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        line.draw(self._canvas, fill_color)


class Cell:
    def __init__(
        self, x1: int, y1: int, x2: int, y2: int, window: Window | None
    ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._window = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

    def draw(self):
        if not self._window:
            return

        wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        if self.has_left_wall:
            self._window.draw_line(wall, "black")
        else:
            self._window.draw_line(wall, "white")


        wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        if self.has_right_wall:
            self._window.draw_line(wall, "black")
        else:
            self._window.draw_line(wall, "white")

        wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        if self.has_top_wall:
            self._window.draw_line(wall, "black")
        else:
            self._window.draw_line(wall, "white")

        wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        if self.has_bottom_wall:
            self._window.draw_line(wall, "black")
        else:
            self._window.draw_line(wall, "white")

    def center(self) -> Point:
        return Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        if not undo:
            color = "red"
        else:
            color = "grey"

        if self._window:
            self._window.draw_line(Line(self.center(), to_cell.center()), color)


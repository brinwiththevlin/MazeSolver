from graphics import Window
from maze import Maze

def main():
    win = Window(800, 600)
    num_cols = 50
    num_rows = 40
    maze = Maze(10, 10, num_rows, num_cols, 15, 15, win=win)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()

from src.sudoku_solver import SudokuSolver
from src.sudoku_visualizer import SudokuVisualizer
import time

board: list[list[int]] = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def main() -> None:
    visualizer: SudokuVisualizer = SudokuVisualizer(time_delay=0.2)
    solver: SudokuSolver = SudokuSolver(board, visualizer, show_process=True, clear_screen=False, no_of_newlines=1)

    print("Puzzle: ")
    visualizer.print(solver.state)
    print()

    start: float = time.time()
    solved: bool = solver.solve()
    end: float = time.time()

    if solved:
        print("Solution: ")
        visualizer.print(solver.state)
    else:
        print("No solution exists!")

    print("Time taken: ", end - start, " seconds")


if __name__ == "__main__":
    main()

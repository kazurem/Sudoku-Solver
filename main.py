from sudoku_solver import SudokuSolver, SudokuController
from sudoku_visualizer import SudokuGUIVisualizer, SudokuTerminalVisualizer

# TODO -- add show_process == False functionality for command line rendering mode
# TODO -- create GUI that works with the solver
# TODO -- stop, clear board, load examples, timer delay
# TODO -- create random puzzle (puzzle generator)
# TODO -- Write tests
# TODO -- Explanation .md files and other documentation
# TODO -- Write website that runs this code? Deploy it using github pages
# TODO -- Compile to get better performance? OR maybe write it in C
# TODO -- Setup github workflow

#Improve error handling and logging (Logger and try excepts?)
# larger sudokus

# TOMORROW:
"""
Use git goddamnit
make PyQt5 GUI
Finish all the use cases
Write tests and learn pytest
"""

## Seperate the time.sleep() from the textRenderMode() function. Put it in the_backTrackSolve()

BOARD: list[list[int]] = [
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


def main():
    solver: SudokuController = SudokuController(SudokuSolver(BOARD, show_process=True), SudokuGUIVisualizer())
    solver.run()

if __name__ == "__main__":
    main()


      



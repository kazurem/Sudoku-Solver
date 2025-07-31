try:
    from sudoku_visualizer import SudokuGUIVisualizer, SudokuTerminalVisualizer
    from sudoku_solver import SudokuSolver
    from sudoku_controller import SudokuController
except ModuleNotFoundError:
    # Fallback if running main.py directly
    from src.sudoku_visualizer import SudokuGUIVisualizer, SudokuTerminalVisualizer
    from src.sudoku_solver import SudokuSolver

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
    
    controller: SudokuController = SudokuController(board, time_delay=100)
    controller.makeApp()
    controller.showUI(SudokuGUIVisualizer(table_dimensions=len(board)))

if __name__ == "__main__":
    main()
import colorsys
import copy
from sudoku_visualizer import SudokuObserver, SudokuState, SudokuTerminalVisualizer, SudokuGUIVisualizer
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

class SudokuSolver:
    def __init__(
        self,
        board: list[list[int]] | None = None,
        show_process: bool = False,
        horizontal_spacing: int = 2,
        vertical_spacing: int = 1,
        algorithm: str = "backtrack",
        visualizer: SudokuObserver | None = None,
    ) -> None:

        original_board: list[list[int]] = copy.deepcopy(board)
        board_size: int = len(board)
        box_size: int = board_size ** (1 / 2)
        self.state: SudokuState = SudokuState(
            board,
            original_board,
            board_size,
            box_size,
            horizontal_spacing,
            vertical_spacing,
        )
        self.isValidBoard()

        self.visualizer: SudokuObserver = visualizer
        self.algorithm: str = algorithm
        self.show_process: bool = show_process

        # Add solving state management
        self.solving = False
        self._backtrack_stack = []
        self.timer = QTimer()

    def notify(self, row: int, column: int):
        self.visualizer.updateUI(self.state, row, column)

    def addVisualizer(self, visualizer: SudokuObserver):
        self.visualizer = visualizer

    def isValidBoard(self) -> None:

        # check if box size is valid (Box size is equal to board size)
        box_size = int(self.state.board_size ** 0.5)
        if box_size * box_size != self.state.board_size:
            raise ValueError("Invalid board: board size must be a perfect square")
    
        self.state.box_size = box_size

        # Check if the puzzle has invalid non-zero values
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                value = self.state.board[y][x]
                if value != 0 and not self.isMoveValid((y, x), value):
                    raise Exception(
                        f"Invalid board: Conflict at (row:{y}, col:{x}) with value {value}"
                    )
                
    def clearBoard(self):
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                self.state.board[y][x] = 0

    def isMoveValid(self, position: tuple[int, int], number: int) -> bool:
        if number > self.state.board_size:
            return False
        
        pos_x: int = position[1]
        pos_y: int = position[0]

        # Check whether column has same number
        for y in range(self.state.board_size):
            if self.state.board[y][pos_x] == number and pos_y != y:
                return False
        # Check whether row has same number
        for x in range(self.state.board_size):
            if self.state.board[pos_y][x] == number and pos_x != x:
                return False

        # Check whether square has same number
        box_x: int = pos_x // self.state.box_size
        box_y: int = pos_y // self.state.box_size

        for y in range(
            box_y * self.state.box_size,
            (box_y * self.state.box_size) + self.state.box_size,
        ):
            for x in range(
                box_x * self.state.box_size,
                (box_x * self.state.box_size) + self.state.box_size,
            ):
                if self.state.board[y][x] == number and (y, x) != position:
                    return False

        return True

    def findEmpty(self) -> tuple[int, int] | None:
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                if self.state.board[y][x] == 0:
                    return (y, x)
        return None
    
    def solve(self):
        if type(self.visualizer) == SudokuGUIVisualizer:
            row, column = self.findEmpty()
            print(row, " ", column)
            self._backtrack_stack = [(row, column, 1)]
            self._backTrackSolveStep()
        else:
            self._backTrackSolve()

    def _backTrackSolveStep(self): #For PySide6 GUI

        """Non-recursive backtracking solver for GUI"""
        if not self.solving:
            return
            
        if not self._backtrack_stack:
            print("Failed to solve - no solution exists!")
            self.solving = False
            return

        row, column, number, is_placed = self._backtrack_stack.pop()
        
        # If we placed a number in the previous step, we need to clear it for backtracking
        if is_placed:
            self.state.board[row][column] = 0
            self.notify(row, column)
        
        # Try numbers from the current number to board_size
        found_valid = False
        for num in range(number, self.state.board_size + 1):
            if self.isMoveValid((row, column), num):
                # Place the number
                self.state.board[row][column] = num
                self.notify(row, column)
                found_valid = True
                
                # Find next empty position
                next_empty = self.findEmpty()
                if next_empty is None:
                    # Puzzle solved!
                    print("Puzzle solved!")
                    self.solving = False
                    return
                
                # Add current position back to stack for potential backtracking
                # with next number to try
                if num < self.state.board_size:
                    self._backtrack_stack.append((row, column, num + 1, True))
                
                # Add next empty position to stack
                next_row, next_column = next_empty
                self._backtrack_stack.append((next_row, next_column, 1, False))
                break
        
        if not found_valid:
            # No valid number found, need to backtrack
            # The cell should already be cleared from the previous step
            pass
        
        # Continue solving after delay
        if self.solving:
            delay = int(getattr(self.visualizer, 'time_delay', 0.1) * 1000)
            QTimer.singleShot(delay, self._backTrackSolveStep)

    def _backTrackSolve(self) -> bool: #Recursive (for terminal printing)

        empty_pos: tuple[int, int] | None = self.findEmpty()

        # if key.pressed:
        #     while True:
        #         cont = input("Enter C to continue: ")
        #         if cont == "C":
        #             break

        if empty_pos is None:
            return True
        else:
            row, column = empty_pos

        for i in range(1, self.state.board_size + 1):
            if self.isMoveValid(empty_pos, i):
                self.state.board[row][column] = i
                if self.show_process:
                    self.notify(row, column)

                if self._backTrackSolve():
                    return True

                self.state.board[row][column] = 0

                if self.show_process:
                    self.notify(row, column)

        return False

class SudokuController:
    
    def __init__(self, solver: SudokuSolver, visualizer: SudokuObserver):
        self.solver: SudokuSolver = solver
        self.solver.addVisualizer(visualizer)

        if(type(visualizer) == SudokuGUIVisualizer):
            self.setupConnections()


    def setupConnections(self):
        self.solver.visualizer.window.solve_mode_combo_box.currentIndexChanged.connect(self.solveModeChanged)
        self.solver.visualizer.window.quit_button.clicked.connect(self.quitButtonClicked)
        self.solver.visualizer.window.clear_button.clicked.connect(self.clearButtonClicked)
        self.solver.visualizer.window.load_example.clicked.connect(self.loadExampleButtonClicked)
        self.solver.visualizer.window.create_puzzle.clicked.connect(self.createPuzzleButtonClicked)
        self.solver.visualizer.window.time_delay.textChanged.connect(self.timerDelayLineEditChanged)
        self.solver.visualizer.window.solve_button.clicked.connect(self.solveButtonClicked)
        self.solver.visualizer.window.stop_button.clicked.connect(self.stopSolvingButtonClicked)
        self.solver.visualizer.window.board.cellChanged.connect(self.boardCellChanged)
        
    def solveModeChanged(self, index: int):
        if self.solver.visualizer.window.solve_mode_combo_box.itemText(index) == "Fast":
            self.solver.visualizer.window.time_delay.setDisabled(True)
        else:
            self.solver.visualizer.window.time_delay.setDisabled(False)

    def quitButtonClicked(self):
        self.solver.visualizer.window.close()

    def loadExampleButtonClicked(self):
        for y in range(self.solver.state.board_size):
            for x in range(self.solver.state.board_size):
                if self.solver.state.board[y][x] == 0:
                    self.solver.visualizer.window.board.item(y, x).setText(None)
                else:
                    self.solver.visualizer.window.board.item(y, x).setText(str(self.solver.state.board[y][x]))

    def clearButtonClicked(self):
        self.solver.clearBoard()
        QApplication.processEvents()

    def solveButtonClicked(self):
        solved: bool = self.solver.solve()

    def createPuzzleButtonClicked(self):
        pass #needs a puzzle generator

    def timerDelayLineEditChanged(self, new_time: str):
        #Properly validate input (reject all things other than numbers or floats)
        if new_time == '':
            return None
        self.solver.visualizer.time_delay = int(new_time)

    def stopSolvingButtonClicked(self):
        pass

    def boardCellChanged(self, row: int, column: int):
        pass

    def run(self):
        if type(self.solver.visualizer) == SudokuGUIVisualizer:
            self.solver.visualizer.run()
        elif type(self.solver.visualizer) == SudokuTerminalVisualizer:
            self.solver.solve()
        

    
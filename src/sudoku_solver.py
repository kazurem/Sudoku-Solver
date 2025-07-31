from dataclasses import dataclass
import copy

try:
    from sudoku_visualizer import SudokuObserver
except ModuleNotFoundError:
    from src.sudoku_visualizer import SudokuObserver

from PySide6.QtCore import QObject, Signal, Slot, QTimer, QThread
from PySide6.QtWidgets import QApplication

import time

@dataclass
class SudokuState:
    board: list[list[int]]
    original_board: list[list[int]] | None
    board_size: int
    box_size: int
    horizontal_spacing: int
    vertical_spacing: int
    clear_screen: int
    no_of_newlines: int


class SudokuSolver(QObject):
    session_ended: Signal = Signal()
    session_started: Signal = Signal()
    
    started_solving: Signal = Signal()
    stop_solving: Signal = Signal()
    
    done_solving: Signal = Signal()

    value_changed: Signal = Signal(int, int, int) #row, column, value
    quit_solving: Signal = Signal()

    def __init__(
        self,
        board: list[list[int]],
        time_delay: float,
        main_thread: QThread,
        visualizer: SudokuObserver | None = None,
        show_process: bool = False,
        horizontal_spacing: int = 2,
        vertical_spacing: int = 1,
        clear_screen: bool = True,
        no_of_newlines: int = 2,
    ) -> None:
        super().__init__()

        self.time_delay: float = time_delay

        original_board: list[list[int]] = copy.deepcopy(board)
        board_size: int = len(board)
        box_size: int = int(board_size ** (1 / 2))

        self.visualizer: SudokuObserver = visualizer

        self.state: SudokuState = SudokuState(
            board,
            original_board,
            board_size,
            box_size,
            horizontal_spacing,
            vertical_spacing,
            clear_screen,
            no_of_newlines
        )

        self.show_process: bool = show_process

        self.backtrack_stack = []
        self.is_stopped: bool = True
        
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self._backTrackStep)

        self.solved = False
        
        self.main_thread = main_thread

    #----------------------------------------------
    # Helper functions
    #----------------------------------------------
    def isValidBoard(self) -> None:

        # check if box size is valid (Box size is equal to board size)
        box_size = int(self.state.board_size ** 0.5)
        if box_size * box_size != self.state.board_size:
            raise ValueError("Invalid board: board size must be a perfect square")
    
        # Check if the puzzle has invalid non-zero values
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                value = self.state.board[y][x]
                if value != 0 and not self.isMoveValid((y, x), value):
                    raise Exception(
                        f"Invalid board: Conflict at (row:{y}, col:{x}) with value {value}"
                    )
                
    def isMoveValid(self, position: tuple[int, int], number: int) -> bool:
        if number > self.state.board_size or number < 1:
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
        self.thread()

    def findEmpty(self) -> tuple[int, int] | None:
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                if self.state.board[y][x] == 0:
                    return (y, x)
        return None
    

    #----------------------------------------------
    # API for controller to use
    #----------------------------------------------
    def clearBoard(self):
        print("clear in solver")
        self.backtrack_stack.clear()
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                self.state.board[y][x] = 0
                self.value_changed.emit(y, x, 0)

    def setCellValue(self, row: int, column: int, value: int):
        print("setCellValue")
        if self.isMoveValid((row, column), value):
            self.state.board[row][column] = value
        elif value == 0:
            self.state.board[row][column] = 0
        else:
            print(f"Number {value} can't be placed at ({row}, {column})")
            return False
        
        return True
    
    def solve(self):
        self.started_solving.emit()
        self.session_started.emit()
        self.is_stopped = False

        empty_cell = self.findEmpty()
        self.backtrack_stack.append((empty_cell[0], empty_cell[1], 1))
        print("in solver.solve")
        while not self.is_stopped:
            if not self._backTrackStep():
                self.session_ended.emit()
                break

        self.is_stopped = True
        self.moveToThread(self.main_thread)
        self.done_solving.emit()


    #----------------------------------------------
    #Algorithm
    #----------------------------------------------
    
    def _backTrackStep(self):
        if not self.is_stopped:
            if len(self.backtrack_stack) == 0:
                return False
            
            row, column, number = self.backtrack_stack.pop()

            if self.isMoveValid((row, column), number):
                self.state.board[row][column] = number
                self.value_changed.emit(row, column, number)

                self.backtrack_stack.append((row, column, number + 1))

                new_cell = self.findEmpty()
                if new_cell is None:
                    return False
                self.backtrack_stack.append((new_cell[0], new_cell[1], 1))
            else:
                if number < self.state.board_size:
                    self.backtrack_stack.append((row, column, number + 1))
                else:
                    self.state.board[row][column] = 0
                    self.value_changed.emit(row, column, 0)

            return True
        else:
            return True
        
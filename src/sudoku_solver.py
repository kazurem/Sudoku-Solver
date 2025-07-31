import copy
from dataclasses import dataclass

from PySide6.QtCore import Signal, QObject, QThread

try:
	from src.sudoku_visualizer import SudokuObserver
except ModuleNotFoundError:
    from sudoku_visualizer import SudokuObserver


@dataclass
class SudokuState:
    board: list[list[int]]
    original_board: list[list[int]] | None
    board_size: int
    box_size: int
    horizontal_spacing: int
    vertical_spacing: int
    time_delay: float
    clear_screen: int
    no_of_newlines: int

class SudokuSolver(QObject):
    #signal for when a board value gets changed
    value_changed: Signal = Signal(int, int, int) #row, column, value

    def __init__(
        self,
        board: list[list[int]],
        show_process: bool = False,
        horizontal_spacing: int = 2,
        vertical_spacing: int = 1,
        time_delay: float = 0,
        clear_screen: bool = True,
        no_of_newlines: int = 2,
        algorithm: str = "backtrack",
    ) -> None:
        
        super().__init__()

        original_board: list[list[int]] = copy.deepcopy(board)
        board_size: int = len(board)
        box_size: int = int(board_size ** (1 / 2))
        self.state: SudokuState = SudokuState(
            board,
            original_board,
            board_size,
            box_size,
            horizontal_spacing,
            vertical_spacing,
            time_delay,
            clear_screen,
            no_of_newlines
        )
        self.algorithm: str = algorithm
        self.show_process: bool = show_process

        self._backtrack_stack = []

    def setSolverThread(self, thread: QThread):
        self.solver_thread = thread

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
                
    def clearBoard(self):
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                self.state.board[y][x] = 0

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

    def findEmpty(self) -> tuple[int, int] | None:
        for y in range(self.state.board_size):
            for x in range(self.state.board_size):
                if self.state.board[y][x] == 0:
                    return (y, x)
        return None
    
    def solve(self):
        empty_cell = self.findEmpty()
        self._backtrack_stack.append((empty_cell[0], empty_cell[1], 1))

        while True:
            if not self._backTrackStep():
                break

        self.moveToThread(self.solver_thread)

    def _backTrackStep(self):       
        if len(self._backtrack_stack) == 0:
            return False
        
        row, column, number = self._backtrack_stack.pop()

        if self.isMoveValid((row, column), number):
            self.state.board[row][column] = number
            self.value_changed.emit(row, column, number)

            self._backtrack_stack.append((row, column, number + 1))

            new_cell = self.findEmpty()
            if new_cell is None:
                return False
            self._backtrack_stack.append((new_cell[0], new_cell[1], 1))
        else:
            if number < self.state.board_size:
                self._backtrack_stack.append((row, column, number + 1))
            else:
                self.state.board[row][column] = 0
                self.value_changed.emit(row, column, 0)

        return True
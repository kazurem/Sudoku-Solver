from dataclasses import dataclass
import copy
try:
	from src.sudoku_visualizer import SudokuVisualizer
except ModuleNotFoundError:
    from sudoku_visualizer import SudokuVisualizer

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

class SudokuSolver:
    def __init__(
        self,
        board: list[list[int]],
        visualizer: SudokuVisualizer | None = None,
        show_process: bool = False,
        horizontal_spacing: int = 2,
        vertical_spacing: int = 1,
        time_delay: float = 0,
        clear_screen: bool = True,
        no_of_newlines: int = 2,
        algorithm: str = "backtrack",
    ) -> None:

        original_board: list[list[int]] = copy.deepcopy(board)
        board_size: int = len(board)
        box_size: int = int(board_size ** (1 / 2))
        self.visualizer: SudokuVisualizer = visualizer
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
        solved = self._backTrackSolve()
        return solved

    def _backTrackSolve(
        self
    ) -> bool:
        
        if self.show_process:
            self.visualizer.print(
                self.state
            )

        empty_pos: tuple[int, int] | None = self.findEmpty()
        if empty_pos is None:
            return True
        else:
            row, column = empty_pos
        for i in range(1, self.state.board_size + 1):
            if self.isMoveValid(empty_pos, i):
                self.state.board[row][column] = i

                if self._backTrackSolve():
                    return True

                self.state.board[row][column] = 0
        return False
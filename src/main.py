import time
from colorama import Fore, init
import copy
import os
from dataclasses import dataclass
from typing import ClassVar
import sys

init(autoreset=True)

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
    
class ANSIColors:
    YELLOW_BOLD: ClassVar[str]  = "\033[1;33m"
    GREEN_BOLD:  ClassVar[str]  = "\033[1;32m"
    WHITE_BOLD:  ClassVar[str]  = "\033[1;37m"
    END:         ClassVar[str]  = "\033[0m"

class SudokuVisualizer:

    def __init__(self, time_delay: int = 0):
        print("\033[2J\033[H")
        self.time_delay = time_delay

    def print(self, state):
        sys.stdout.write("\033[H") #moves the cursor to the top (doesnt clear screen)

        # BOARD_SIZE * PUZZLE_HORIZONTOL_SPACE is for every number
        # BOARD_SIZE//BOX_WIDTH is the number of |'s in the puzzle. Multiply it with PUZZLE_HORIZONTOL_SPACE to get the full space
        # + 1 for the last |
        horizontol_line_length: int = (
            (state.board_size * state.horizontal_spacing)
            + ((state.board_size // state.box_size) * state.horizontal_spacing)
            + 1
        )

        board_row: str = ""
        for y in range(state.board_size):
            if y % state.box_size == 0:  # put horizontol line at top
                board_row += (f"{ANSIColors.WHITE_BOLD}{'-' * horizontol_line_length}{ANSIColors.END}\n")

            for x in range(state.board_size):
                if x % state.box_size == 0:  # put | every BOX_WIDTH
                    board_row += (f"{ANSIColors.WHITE_BOLD}{'|':<{state.horizontal_spacing}}{ANSIColors.END}")

                # Print the numbers (if original board is given then solution numbers are colored differently)
                value: int = state.board[y][x]
                if value == 0: # Empty cells
                    board_row += (f"{ANSIColors.YELLOW_BOLD}{'-':<{state.horizontal_spacing}}{ANSIColors.END}")
                elif state.original_board and value != state.original_board[y][x]: #solution values
                    board_row += (f"{ANSIColors.GREEN_BOLD}{value:<{state.horizontal_spacing}}{ANSIColors.END}")
                else:  # given numbers
                    board_row += (f"{ANSIColors.WHITE_BOLD}{value:<{state.horizontal_spacing}}")

                if x == state.board_size - 1:  # put | at the right edge
                    board_row += (f"{ANSIColors.WHITE_BOLD}|{ANSIColors.END}\n")

            if y == state.board_size - 1:
                board_row += (f"{ANSIColors.WHITE_BOLD}{'-' * horizontol_line_length}{ANSIColors.END}")
            
        sys.stdout.write(board_row)
        sys.stdout.flush()

        if self.time_delay > 0:
            time.sleep(self.time_delay)



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
    visualizer: SudokuVisualizer = SudokuVisualizer(time_delay=0)
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

import time
from colorama import Fore, init
import copy
import os

init(autoreset=True)

"""
Todo:
3. A good readme which explains the algorithm and the code
4. A recursive and non-recursive solution (different py files) for backtracking
5. Solve using dancing links algorithm
6. Write tests
8. Make a GUI (using pyqt or pygame). Make the UI clean
9. Make the code OOP
"""

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


# board: list[list[int]] = [
#     [0, 1, 0, 5, 4, 7, 6, 0],
#     [7, 8, 0, 0, 3, 0, 0, 5],
#     [3, 0, 0, 0, 0, 8, 5, 1],
#     [1, 0, 2, 8, 0, 6, 4, 3],
#     [6, 0, 4, 1, 0, 2, 0, 7],
#     [5, 0, 0, 2, 0, 3, 0, 4],
#     [0, 0, 1, 3, 0, 0, 7, 0],
#     [0, 2, 0, 0, 0, 0, 3, 0],
# ]

board_copy: list[list[int]] = copy.deepcopy(board)

BOARD_SIZE: int = len(board)
BOX_WIDTH: int = 3
BOX_HEIGHT: int = 3

# For drawing
PUZZLE_HORIZONTOL_SPACING: int = 3
PUZZLE_VERTICAL_SPACING: int = 1

def isValidBoard(board: list[list[int]]) -> bool:
    """
    :param board: list[list[int]]
    """

    # check if box size is valid (Box size is equal to board size)
    if BOX_WIDTH * BOX_HEIGHT != BOARD_SIZE:
        print("Invalid board: box dimensions do not match board size.")
        return False

    # Check if the puzzle has invalid non-zero values
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            value = board[y][x]
            if value != 0 and not isValid((y, x), value, board):
                print(f"Invalid board: Conflict at (col:{y}, row:{x}) with value {value}")
                return False

    return True


def printBoard(
    board: list[list[int]],
    original_board: list[list[int]] | None = None,
    time_delay: float = 0.2,
    no_of_newlines: int = 0,
    clear_screen: bool = False
) -> None:
    """Pretty prints the Sudoku board with optional colors. \n
    :param board: The board to be printed \n
    :param original_board: The unsolved board (for coloring the solution numbers)\n
    :param time_delay: Sleep time after each function call (for algorithmic visualization purposes) \n
    :param no_of_newlines: newlines printed after drawing the board
    :param clear_screen: clear the screen before the board is drawn
    :return: None
    """

    # BOARD_SIZE * PUZZLE_HORIZONTOL_SPACE is for every number
    # BOARD_SIZE//BOX_WIDTH is the number of |'s in the puzzle. Multiply it with PUZZLE_HORIZONTOL_SPACE to get the full space
    # + 1 for the last |
    if clear_screen:
        os.system("cls" if os.name == "nt" else "clear")

    horizontol_line_length: int = (
        (BOARD_SIZE * PUZZLE_HORIZONTOL_SPACING)
        + ((BOARD_SIZE // BOX_WIDTH) * PUZZLE_HORIZONTOL_SPACING)
        + 1
    )

    for y in range(BOARD_SIZE):
        if y % BOX_HEIGHT == 0:  # put horizontol line at top
            print("-" * horizontol_line_length)

        for x in range(BOARD_SIZE):
            if x % BOX_WIDTH == 0:  # put | every BOX_WIDTH
                print(f"{'|':<{PUZZLE_HORIZONTOL_SPACING}}", end="")

            # Print the numbers (if original board is given then solution numbers are colored differently)
            value: int = board[y][x]
            if value == 0:
                print(f"{Fore.YELLOW}{'-':<{PUZZLE_HORIZONTOL_SPACING}}", end="")
            elif original_board and value != original_board[y][x]:
                print(
                    f"{Fore.GREEN}{value:<{PUZZLE_HORIZONTOL_SPACING}}",
                    end="",
                )
            else:  # given numbers
                print(f"{value:<{PUZZLE_HORIZONTOL_SPACING}}", end="")


            if x == BOARD_SIZE - 1:  # put | at the right edge
                print("|", end="\n" * PUZZLE_VERTICAL_SPACING)

        if y == BOARD_SIZE - 1:  # put a horizontol line at bottom
            print("-" * horizontol_line_length)

    print("\n" * no_of_newlines, end="")
    time.sleep(time_delay)


def findEmpty(board: list[list[int]]) -> tuple[int, int] | None:
    """
    Returns the position of the first empty square in the board. It is found after looping from left to right and top to bottom \n
    :param board: The board we are working with
    :return: tuple(row, col)
    """
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                return (y, x)
    return None


def isValid(position: tuple[int, int], number: int, board: list[list[int]]) -> bool:
    """
    Checks whether placing a number at a position is valid

    :param position: tuple(row, column)
    :param number: int
    :param board: list[list[int]]
    :return: bool
    """
    pos_x: int = position[1]
    pos_y: int = position[0]

    # Check whether column has same number
    for y in range(BOARD_SIZE):
        if board[y][pos_x] == number and pos_y != y:
            return False
    # Check whether row has same number
    for x in range(BOARD_SIZE):
        if board[pos_y][x] == number and pos_x != x:
            return False

    # Check whether square has same number
    box_x: int = pos_x // BOX_WIDTH
    box_y: int = pos_y // BOX_HEIGHT

    for y in range(box_y * BOX_HEIGHT, (box_y * BOX_HEIGHT) + BOX_HEIGHT):
        for x in range(box_x * BOX_WIDTH, (box_x * BOX_WIDTH) + BOX_WIDTH):
            if board[y][x] == number and (y, x) != position:
                return False

    return True


def backTrackSolve(
    board: list[list[int]],
    visualize: bool = False,
    time_delay: float = 0.2,
    no_of_newlines: int = 0,
) -> bool:
    """
    Tries to solve the board using backtracking algorithm

    :param no_of_newlines: newlines printed after each board
    :param time_delay: how much time between two printed boards
    :param visualize: print the board after every iteration
    :param board: the board that needs to be solved
    :return: whether the puzzle has been solved or not
    """
    if visualize:
        printBoard(
            board,
            time_delay=time_delay,
            original_board=board_copy,
            no_of_newlines=no_of_newlines,
        )

    empty_pos: tuple[int, int] | None = findEmpty(board)
    if empty_pos is None:
        return True
    else:
        row, column = empty_pos
    for i in range(1, BOARD_SIZE + 1):
        if isValid(empty_pos, i, board):
            board[row][column] = i

            if backTrackSolve(board, visualize=visualize, time_delay=time_delay):
                return True

            board[row][column] = 0
    return False


def main() -> None:
    if isValidBoard(board):
        print("Puzzle: ")
        printBoard(board)
        print()

        start: float = time.time()
        solved = backTrackSolve(board, visualize=False, time_delay=0.2)
        end = time.time()

        if solved:
            print("Solution: ")
            printBoard(board, original_board=board_copy)
        else:
            print("No solution exists!")

        print("Time taken: ", end - start, " seconds")


if __name__ == "__main__":
    main()

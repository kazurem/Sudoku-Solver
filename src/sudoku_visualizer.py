from typing import ClassVar
import sys
import time


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


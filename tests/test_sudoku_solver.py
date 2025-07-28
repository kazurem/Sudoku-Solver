import pytest
from src.sudoku_solver import SudokuSolver

# ---------------------------
# Tests for isValidBoard
# ---------------------------

def test_valid_board(solver):
    solver.isValidBoard()  # should not raise

@pytest.mark.parametrize("key", ["row", "column", "square", "row_dimension", "column_dimension"])
def test_invalid_boards_raise(key, invalid_boards):
    with pytest.raises(Exception):
        SudokuSolver(invalid_boards[key]).isValidBoard()

# ---------------------------
# Tests for findEmpty
# ---------------------------

def test_find_empty(solver):
    result = solver.findEmpty()
    assert result == (0, 2)

def test_find_empty_full_board():
    full_board = [[i for i in range(1, 10)] for _ in range(9)]
    solver = SudokuSolver(full_board)
    result = solver.findEmpty()
    assert result is None  # Assuming findEmpty returns None if no empty cells

# ---------------------------
# Tests for isMoveValid
# ---------------------------

def test_is_move_not_valid_in_row(solver):
    assert solver.isMoveValid((0, 2), 7) is False

def test_is_move_valid_in_row(solver):
    assert solver.isMoveValid((0, 2), 1) is True

def test_is_move_not_valid_in_column(solver):
    assert solver.isMoveValid((8, 2), 6) is False

def test_is_move_valid_in_column(solver):
    assert solver.isMoveValid((8, 2), 1) is True

def test_is_move_not_valid_in_square(solver):
    assert solver.isMoveValid((0, 8), 1) is False

def test_is_move_valid_in_square(solver):
    assert solver.isMoveValid((0, 8), 2) is True

# ---------------------------
# Extra Edge Cases
# ---------------------------

def test_invalid_number_move(solver):
    assert solver.isMoveValid((0, 2), 12) is False

# ---------------------------
# Backtracking algorithm
# ---------------------------
def test_solver_solution(solver, valid_board_solution):
    solver.solve()
    assert solver.state.board == valid_board_solution
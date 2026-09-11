from __future__ import annotations

import copy
import random

Board = list[list[int]]

SIZE = 9
BOX_SIZE = 3
EMPTY = 0
MIN_VALUE = 1
MAX_VALUE = SIZE
CELL_COUNT = SIZE * SIZE
DEFAULT_CLUES = 35


def deep_copy(board: Board) -> Board:
    """Return an independent copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board() -> Board:
    """Create a board containing only empty cells."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board: Board, row: int, col: int, num: int) -> bool:
    """Return whether ``num`` can be placed at ``row`` and ``col``."""
    for index in range(SIZE):
        if board[row][index] == num or board[index][col] == num:
            return False

    start_row = row - row % BOX_SIZE
    start_col = col - col % BOX_SIZE
    for box_row in range(start_row, start_row + BOX_SIZE):
        for box_col in range(start_col, start_col + BOX_SIZE):
            if board[box_row][box_col] == num:
                return False
    return True


def fill_board(board: Board) -> bool:
    """Fill empty cells in place with a valid randomized Sudoku solution."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(MIN_VALUE, MAX_VALUE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def generate_solution() -> Board:
    """Generate and return a complete valid Sudoku solution."""
    solution = create_empty_board()
    fill_board(solution)
    return solution


def carve_holes(solution: Board, clues: int) -> Board:
    """Return a copy of ``solution`` with cells removed until clues remain."""
    puzzle = deep_copy(solution)
    attempts = CELL_COUNT - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if puzzle[row][col] != EMPTY:
            puzzle[row][col] = EMPTY
            attempts -= 1
    return puzzle


def remove_cells(board: Board, clues: int) -> None:
    """Remove cells in place until a board contains the requested clues."""
    carved_board = carve_holes(board, clues)
    board[:] = carved_board


def count_solutions(board: Board, limit: int = 2) -> int:
    """Count valid solutions for ``board``, stopping once ``limit`` is reached."""
    if limit <= 0:
        return 0

    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if value < MIN_VALUE or value > MAX_VALUE:
                return 0
            board[row][col] = EMPTY
            valid = is_safe(board, row, col, value)
            board[row][col] = value
            if not valid:
                return 0

    def search() -> int:
        best_cell = None
        best_candidates = None

        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] != EMPTY:
                    continue

                candidates = [
                    value
                    for value in range(MIN_VALUE, MAX_VALUE + 1)
                    if is_safe(board, row, col, value)
                ]
                if not candidates:
                    return 0
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates

        if best_cell is None:
            return 1

        row, col = best_cell
        solutions = 0
        for candidate in best_candidates:
            board[row][col] = candidate
            solutions += search()
            board[row][col] = EMPTY
            if solutions >= limit:
                return limit
        return solutions

    return search()


def validate_unique_solution(puzzle: Board) -> bool:
    """Return whether ``puzzle`` has exactly one solution."""
    return count_solutions(puzzle) == 1


def generate_puzzle(clues: int = DEFAULT_CLUES) -> tuple[Board, Board]:
    """Generate a puzzle with its complete solution.

    The puzzle is carved from a separately copied solution and restored until
    it has exactly one solution.
    """
    solution = generate_solution()
    puzzle = carve_holes(solution, clues)
    while not validate_unique_solution(puzzle):
        empty_cells = [
            (row, col)
            for row in range(SIZE)
            for col in range(SIZE)
            if puzzle[row][col] == EMPTY
        ]
        row, col = random.choice(empty_cells)
        puzzle[row][col] = solution[row][col]
    return puzzle, solution

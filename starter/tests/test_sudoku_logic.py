import sudoku_logic


def assert_valid_board(board):
    expected = set(range(1, sudoku_logic.SIZE + 1))

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)

    for row in board:
        assert set(row) == expected

    for column in range(sudoku_logic.SIZE):
        assert {board[row][column] for row in range(sudoku_logic.SIZE)} == expected

    for box_row in range(0, sudoku_logic.SIZE, 3):
        for box_col in range(0, sudoku_logic.SIZE, 3):
            values = {
                board[row][column]
                for row in range(box_row, box_row + 3)
                for column in range(box_col, box_col + 3)
            }
            assert values == expected


def test_is_safe_accepts_valid_candidate_and_rejects_row_column_and_box_duplicates():
    board = [
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

    assert sudoku_logic.is_safe(board, 0, 2, 4)
    assert not sudoku_logic.is_safe(board, 0, 2, 5)
    assert not sudoku_logic.is_safe(board, 0, 2, 8)
    assert not sudoku_logic.is_safe(board, 0, 2, 9)


def test_fill_board_completes_a_valid_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board)
    assert_valid_board(board)


def test_generate_puzzle_returns_valid_solution_with_fewer_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert_valid_board(solution)
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(
        puzzle[row][column] in range(sudoku_logic.SIZE + 1)
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )
    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )
    assert sum(value != sudoku_logic.EMPTY for row in puzzle for value in row) < sum(
        value != sudoku_logic.EMPTY for row in solution for value in row
    )


def test_generate_puzzle_has_exactly_one_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(clues=35)

    assert sudoku_logic.count_solutions(puzzle) == 1

from typing import TypedDict

from flask import Flask, jsonify, render_template, request
import sudoku_logic

app = Flask(__name__)


class CurrentGame(TypedDict):
    """The puzzle and solution for the currently active in-memory game."""

    puzzle: sudoku_logic.Board | None
    solution: sudoku_logic.Board | None


# The application intentionally keeps one game in memory for this small app.
CURRENT: CurrentGame = {'puzzle': None, 'solution': None}

DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 25,
}

@app.route('/')
def index():
    """Render the Sudoku game page."""
    return render_template('index.html')


@app.route('/new')
def new_game():
    """Generate a new puzzle using a difficulty or an explicit clue count."""
    difficulty = request.args.get('difficulty', 'medium').lower()
    if difficulty not in DIFFICULTY_CLUES:
        return jsonify({
            'error': 'Invalid difficulty. Choose easy, medium, or hard.'
        }), 400

    clues_value = request.args.get('clues')
    try:
        clues = DIFFICULTY_CLUES[difficulty] if clues_value is None else int(clues_value)
        if not 0 <= clues <= sudoku_logic.CELL_COUNT:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({'error': 'Clues must be an integer from 0 to 81.'}), 400

    try:
        puzzle, solution = sudoku_logic.generate_puzzle(clues)
    except Exception:
        app.logger.exception('Failed to generate a Sudoku puzzle')
        return jsonify({'error': 'Unable to generate a new puzzle.'}), 500

    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle, 'solution': solution})


@app.route('/check', methods=['POST'])
def check_solution():
    """Compare a submitted board with the active solution."""
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or 'board' not in data:
            return jsonify({'error': 'Request JSON must include a board.'}), 400

        board = data['board']
        if (
            not isinstance(board, list)
            or len(board) != sudoku_logic.SIZE
            or any(
                not isinstance(row, list)
                or len(row) != sudoku_logic.SIZE
                or any(not isinstance(cell, int) or isinstance(cell, bool) for cell in row)
                for row in board
            )
        ):
            return jsonify({'error': 'Board must be a 9x9 array of integers.'}), 400

        solution = CURRENT['solution']
        if solution is None:
            return jsonify({'error': 'No game in progress'}), 400

        incorrect = [
            [row, col]
            for row in range(sudoku_logic.SIZE)
            for col in range(sudoku_logic.SIZE)
            if board[row][col] != solution[row][col]
        ]
        return jsonify({'incorrect': incorrect})
    except Exception:
        app.logger.exception('Failed to check Sudoku solution')
        return jsonify({'error': 'Unable to check the submitted solution.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
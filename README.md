# Sudoku Game

A responsive Sudoku game built with Python, Flask, and vanilla JavaScript. The application generates playable puzzles, validates solutions, tracks performance, and keeps a local leaderboard for completed games.

## Features

### Puzzle generation

- Generates a complete, valid 9x9 Sudoku solution using randomized backtracking.
- Removes cells to create a puzzle with the selected number of clues.
- Verifies that every generated puzzle has exactly one solution.
- Supports three difficulty levels:
  - **Easy:** 45 clues
  - **Medium:** 35 clues
  - **Hard:** 25 clues

### Gameplay

- Starts a new puzzle from the difficulty selector or the **New Game** button.
- Runs an elapsed-time timer for each active game.
- Prevents editing prefilled puzzle cells.
- Provides hints by filling an empty cell with the correct value and highlighting it with a distinct color.
- Uses event delegation to validate board input as the player types.
- Highlights duplicate values in rows, columns, and 3x3 boxes immediately.
- Restricts cell input to a single digit from 1 through 9.

### Solution checking and feedback

- The **Check Solution** button compares the current board with the server-side solution.
- Incorrect entries and empty cells are highlighted separately.
- Displays clear error messages for invalid requests, missing games, and incomplete solutions.
- Stops the timer when the puzzle is solved.
- Shows a completion message with the final time and number of hints used.

### Scores and presentation

- Prompts for the player's name after a successful solve.
- Stores the top 10 scores in browser `localStorage`.
- Displays each score's rank, player name, time, difficulty, and hints used.
- Sorts leaderboard entries by fastest completion time.
- Supports light and dark themes, with the preference persisted in `localStorage`.
- Uses a responsive layout that adapts the board, controls, dialog, and leaderboard for mobile screens.

## Technology

- **Backend:** Python 3 and Flask
- **Frontend:** HTML, CSS, and native JavaScript modules
- **Persistence:** Browser `localStorage` for theme and leaderboard data
- **Testing:** pytest

The active puzzle and solution are held in server memory for the current application instance. The leaderboard is client-side and is specific to the browser used to play the game.

## Project Structure

```text
starter/
├── app.py                       Flask routes and request validation
├── sudoku_logic.py              Puzzle generation and solution validation
├── requirements.txt             Python dependencies
├── templates/index.html         Game page markup
├── static/
│   ├── api.js                   Backend API requests
│   ├── board-rendering.js       Board creation and cell feedback
│   ├── game-state.js            Timer and active-game state
│   ├── main.js                  Game interactions and leaderboard
│   └── styles.css               Responsive light and dark themes
└── tests/
    ├── test_app.py              Flask route tests
    └── test_sudoku_logic.py     Sudoku generation and validation tests
```

## Getting Started

### Prerequisites

- Python 3
- A modern web browser

### Installation

From the `starter` directory, create a virtual environment and install the dependencies:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the packages:

```bash
pip install -r requirements.txt
```

Start the Flask development server:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

## API Endpoints

### `GET /new`

Generates a new puzzle. Pass `difficulty=easy`, `difficulty=medium`, or `difficulty=hard` as a query parameter. The response contains the puzzle and its solution.

An optional `clues` query parameter can be used to request an explicit clue count from 0 to 81.

### `POST /check`

Checks a submitted 9x9 board against the active solution.

```json
{
  "board": [[0, 5, 0, 0, 7, 0, 0, 0, 0]]
}
```

The response contains an `incorrect` array with the row and column of each incorrect cell. An empty array means the submitted board matches the solution.

## Running Tests

From the `starter` directory:

```bash
pytest -v
```

The test suite covers valid board generation, unique-solution puzzles, candidate validation, route responses, request validation, and incorrect-cell reporting.

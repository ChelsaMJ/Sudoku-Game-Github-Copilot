import {checkBoard, fetchNewGame} from './api.js';
import {
  getBoard,
  getBoardElement,
  applyHint,
  markConflictingCells,
  markIncorrectCells,
  renderPuzzle,
} from './board-rendering.js';
import {
  gameState,
  formatTimer,
  startGame,
  stopTimer,
  subscribeToTimer,
} from './game-state.js';

const messageElement = document.getElementById('message');
const timerElement = document.getElementById('timer');
const leaderboardBody = document.getElementById('leaderboard-body');
const nameDialog = document.getElementById('name-dialog');
const nameForm = document.getElementById('name-form');
const themeToggle = document.getElementById('theme-toggle');
const LEADERBOARD_KEY = 'sudokuTop10';
const THEME_KEY = 'sudokuTheme';

function updateThemeToggle() {
  const isDark = document.documentElement.dataset.theme === 'dark';
  themeToggle.innerText = isDark ? 'Switch to light mode' : 'Switch to dark mode';
  themeToggle.setAttribute('aria-pressed', String(isDark));
}

function toggleTheme() {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = nextTheme;
  localStorage.setItem(THEME_KEY, nextTheme);
  updateThemeToggle();
}

function getLeaderboard() {
  try {
    const entries = JSON.parse(localStorage.getItem(LEADERBOARD_KEY) || '[]');
    return Array.isArray(entries) ? entries : [];
  } catch (error) {
    return [];
  }
}

function renderLeaderboard() {
  const entries = getLeaderboard().sort((first, second) => first.time - second.time).slice(0, 10);
  leaderboardBody.innerHTML = '';
  entries.forEach((entry, index) => {
    const row = document.createElement('tr');
    [index + 1, entry.name, formatTimer(entry.time), entry.difficulty, entry.hints].forEach((value) => {
      const cell = document.createElement('td');
      cell.innerText = value;
      row.appendChild(cell);
    });
    leaderboardBody.appendChild(row);
  });
}

function saveScore(name) {
  if (!name || !name.trim()) return;

  const entries = getLeaderboard();
  entries.push({
    name: name.trim(),
    time: gameState.timer,
    difficulty: document.getElementById('difficulty').value,
    hints: gameState.hintsUsed,
  });
  entries.sort((first, second) => first.time - second.time);
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(entries.slice(0, 10)));
  renderLeaderboard();
}

function promptForName() {
  nameForm.reset();
  if (typeof nameDialog.showModal === 'function') {
    nameDialog.showModal();
  }
}

subscribeToTimer((seconds) => {
  timerElement.innerText = formatTimer(seconds);
});

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const data = await fetchNewGame(difficulty);
  if (data.error) {
    showMessage(data.error, 'error');
    return;
  }
  startGame(data.puzzle, data.solution);
  renderPuzzle(data.puzzle);
  showMessage('');
}

function useHint() {
  const emptyCells = Array.from(getBoardElement().querySelectorAll('.sudoku-cell'))
    .filter((cell) => !cell.disabled && !cell.value);

  if (emptyCells.length === 0) {
    showMessage('There are no empty cells left.', 'error');
    return;
  }

  const cell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  const row = Number(cell.dataset.row);
  const col = Number(cell.dataset.col);
  applyHint(row, col, gameState.solution[row][col]);
  gameState.hintsUsed += 1;
  markConflictingCells();
}

async function checkSolution() {
  const data = await checkBoard(getBoard());
  if (data.error) {
    showMessage(data.error, 'error');
    return;
  }
  markIncorrectCells(data.incorrect);
  if (data.incorrect.length === 0) {
    stopTimer();
    showMessage(
      `Congratulations! You solved it in ${formatTimer(gameState.timer)} with ${gameState.hintsUsed} hint${gameState.hintsUsed === 1 ? '' : 's'} used.`,
      'success'
    );
    promptForName();
  } else {
    showMessage('Some cells are incorrect.', 'error');
  }
}

function showMessage(text, status = '') {
  messageElement.innerText = text;
  messageElement.className = status ? `status-${status}` : '';
}

getBoardElement().addEventListener('input', (event) => {
  if (event.target.matches('.sudoku-cell')) {
    event.target.value = event.target.value.replace(/[^1-9]/g, '');
    markConflictingCells();
  }
});

document.getElementById('new-game').addEventListener('click', newGame);
document.getElementById('check-solution').addEventListener('click', checkSolution);
document.getElementById('hint').addEventListener('click', useHint);
themeToggle.addEventListener('click', toggleTheme);
nameForm.addEventListener('submit', (event) => {
  if (event.submitter.value === 'save') saveScore(new FormData(nameForm).get('playerName'));
});
renderLeaderboard();
updateThemeToggle();
newGame();
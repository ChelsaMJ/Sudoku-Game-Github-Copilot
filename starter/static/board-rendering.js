export const SIZE = 9;

const boardElement = document.getElementById('sudoku-board');

export function createBoard() {
  boardElement.innerHTML = '';
  for (let row = 0; row < SIZE; row += 1) {
    const rowElement = document.createElement('div');
    rowElement.className = 'sudoku-row';
    for (let col = 0; col < SIZE; col += 1) {
      const cell = document.createElement('input');
      cell.type = 'text';
      cell.maxLength = 1;
      cell.className = 'sudoku-cell';
      cell.dataset.row = row;
      cell.dataset.col = col;
      rowElement.appendChild(cell);
    }
    boardElement.appendChild(rowElement);
  }
}

export function renderPuzzle(puzzle) {
  createBoard();
  const cells = boardElement.querySelectorAll('.sudoku-cell');
  puzzle.forEach((row, rowIndex) => {
    row.forEach((value, colIndex) => {
      const cell = cells[rowIndex * SIZE + colIndex];
      cell.value = value || '';
      cell.disabled = value !== 0;
      if (value !== 0) cell.classList.add('prefilled');
    });
  });
}

export function getBoard() {
  return Array.from({length: SIZE}, (_, row) =>
    Array.from({length: SIZE}, (_, col) => {
      const cell = boardElement.querySelector(`[data-row="${row}"][data-col="${col}"]`);
      return cell.value ? parseInt(cell.value, 10) : 0;
    })
  );
}

export function applyHint(row, col, value) {
  const cell = boardElement.querySelector(`[data-row="${row}"][data-col="${col}"]`);
  cell.value = value;
  cell.disabled = true;
  cell.classList.remove('incorrect', 'empty');
  cell.classList.add('hint-cell');
}

export function markConflictingCells() {
  const board = getBoard();
  const conflictingIndexes = new Set();

  const markDuplicateValues = (indexes) => {
    const indexesByValue = new Map();
    indexes.forEach(([row, col]) => {
      const value = board[row][col];
      if (!value) return;
      if (!indexesByValue.has(value)) indexesByValue.set(value, []);
      indexesByValue.get(value).push(row * SIZE + col);
    });
    indexesByValue.forEach((cellIndexes) => {
      if (cellIndexes.length > 1) {
        cellIndexes.forEach((index) => conflictingIndexes.add(index));
      }
    });
  };

  for (let row = 0; row < SIZE; row += 1) {
    markDuplicateValues(Array.from({length: SIZE}, (_, col) => [row, col]));
  }
  for (let col = 0; col < SIZE; col += 1) {
    markDuplicateValues(Array.from({length: SIZE}, (_, row) => [row, col]));
  }
  for (let boxRow = 0; boxRow < SIZE; boxRow += 3) {
    for (let boxCol = 0; boxCol < SIZE; boxCol += 3) {
      markDuplicateValues(
        Array.from({length: 3}, (_, rowOffset) =>
          Array.from({length: 3}, (_, colOffset) => [boxRow + rowOffset, boxCol + colOffset])
        ).flat()
      );
    }
  }

  boardElement.querySelectorAll('.sudoku-cell').forEach((cell, index) => {
    cell.classList.toggle('invalid', conflictingIndexes.has(index));
  });
}

export function markIncorrectCells(incorrect) {
  const incorrectIndexes = new Set(incorrect.map(([row, col]) => row * SIZE + col));
  boardElement.querySelectorAll('.sudoku-cell').forEach((cell, index) => {
    if (cell.disabled) return;

    const isIncorrect = incorrectIndexes.has(index);
    cell.classList.toggle('incorrect', isIncorrect && Boolean(cell.value));
    cell.classList.toggle('empty', isIncorrect && !cell.value);
  });
}

export function getBoardElement() {
  return boardElement;
}
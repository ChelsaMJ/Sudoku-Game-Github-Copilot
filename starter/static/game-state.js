export const gameState = {
  puzzle: null,
  solution: null,
  timer: 0,
  hintsUsed: 0,
};

let timerInterval = null;
let timerUpdateListener = null;

export function formatTimer(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const remainingSeconds = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${remainingSeconds}`;
}

export function subscribeToTimer(listener) {
  timerUpdateListener = listener;
  listener(gameState.timer);
}

function notifyTimerUpdate() {
  if (timerUpdateListener) timerUpdateListener(gameState.timer);
}

export function startTimer() {
  stopTimer();
  notifyTimerUpdate();
  timerInterval = setInterval(() => {
    gameState.timer += 1;
    notifyTimerUpdate();
  }, 1000);
}

export function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

export function startGame(puzzle, solution = null) {
  stopTimer();
  gameState.puzzle = puzzle;
  gameState.solution = solution;
  gameState.timer = 0;
  gameState.hintsUsed = 0;
  notifyTimerUpdate();
  if (puzzle) startTimer();
}

export function resetGame() {
  startGame(null);
}
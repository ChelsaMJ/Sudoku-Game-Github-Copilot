export async function fetchNewGame(difficulty) {
  const response = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  return response.json();
}

export async function checkBoard(board) {
  const response = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board}),
  });
  return response.json();
}
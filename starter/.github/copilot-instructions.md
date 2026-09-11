# Project Instructions

## Overview

This project is a modular Sudoku game with:

- **Backend:** Python 3 with Flask
- **Frontend:** Vanilla JavaScript using ES6+ features
- **Testing:** `pytest`
- **No frontend framework:** Do not introduce React, Vue, Angular, or similar frameworks.

## Code Style

### Python

- Follow PEP 8.
- Use descriptive names for variables, functions, classes, and modules.
- Keep functions small and single-purpose.
- Add a docstring to every Python function.
- Prefer clear, explicit code over clever abstractions.
- Use type hints where they improve readability.

### JavaScript

- Use modern ES6+ syntax.
- Use descriptive names; avoid unexplained abbreviations.
- Keep functions small and single-purpose.
- Prefer `const` and `let` over `var`.
- Avoid unnecessary global state.
- Keep browser-specific code organized and modular.

## Project Structure

- Keep Sudoku rules, validation, puzzle generation, and game state logic separate from Flask routes.
- Flask routes should handle HTTP concerns, request validation, response formatting, and status codes.
- Do not place game logic directly inside route handlers.
- In JavaScript, keep DOM manipulation separate from game state and Sudoku logic.
- UI functions should render or update the DOM.
- State and game-logic functions should not directly query or mutate DOM elements.
- Reuse existing modules and project conventions before introducing new abstractions.

## Error Handling

### Flask

- Always return JSON error responses.
- Use the appropriate HTTP status code for each error.
- Do not expose stack traces or internal implementation details to clients.
- Validate request data before passing it to game logic.
- Use a consistent error shape, such as:

```json
{
  "error": "A clear description of the problem."
}
```

### JavaScript

- Never silently ignore errors.
- Handle failed network requests and invalid responses explicitly.
- Provide a useful message or accessible UI feedback when an operation fails.
- Log unexpected technical details with `console.error` when appropriate.
- Avoid empty `catch` blocks.

## Comments and Documentation

- Add docstrings to all Python functions.
- Add comments to JavaScript only when explaining non-obvious behavior, algorithms, or browser-specific workarounds.
- Do not add comments that merely restate what the code already says.
- Keep documentation synchronized with behavior when public APIs or commands change.

## Testing

- Use `pytest` for Python tests.
- Tests must be runnable with a single command from the project root.
- Keep tests deterministic and independent.
- Test Sudoku rules and game logic separately from Flask route behavior.
- Include coverage for valid input, invalid input, boundary cases, and error responses.
- When changing frontend behavior, add or update an appropriate browser-level or integration test if the project provides frontend test tooling.
- Do not consider a change complete until the test command passes.

The canonical test command should be documented in the project README and remain executable without manual setup beyond installing dependencies.

## Accessibility

Target **WCAG 2.1 AA**.

- Provide proper labels for all inputs and interactive controls.
- Ensure the game is fully usable with keyboard navigation.
- Preserve a logical focus order.
- Use semantic HTML elements where appropriate.
- Do not rely on color alone to communicate state, errors, or success.
- Maintain sufficient color contrast.
- Provide accessible names and states for custom controls.
- Make validation and game-status messages available to assistive technologies.
- Ensure focus indicators are visible.
- Avoid interactions that require a mouse or pointer exclusively.

## Change Guidelines

- Prefer minimal, focused changes.
- Preserve existing behavior unless the task explicitly changes it.
- Keep backend, game logic, frontend state, and DOM concerns clearly separated.
- Update tests and documentation when behavior changes.
- Before considering work complete, run the project's single-command test suite and verify accessibility-sensitive UI changes manually.

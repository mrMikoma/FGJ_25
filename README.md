# Bubble Pop Game: GitHub Pull Request Edition 🎮

## Overview
The **Bubble Pop Game** is a fun, interactive game designed to be played directly within GitHub Pull Requests! 🧩 Two players compete against each other by making moves through comments on a PR. The first player to score **10 points** wins the game, and the PR is updated dynamically to reflect the current game state and winner.

The game state is stored in a JSON file within the repository, and each move updates the game board and scores.

---

## How It Works

### Initializing a New Game
- A new game can be initialized by creating a **new branch** and opening a pull request.
- The game state is unique to each branch, so multiple games can run simultaneously in different PRs.

### Player Assignment
- The **first commenter** on the PR is assigned as `Player A`.
- The **second commenter** is assigned as `Player B`.
- Player names are stored and displayed in the PR title and comments.

### Game Objective
Players take turns "popping bubbles" :large_blue_circle: by specifying a row and column using a comment in the format:  

```
move <row_letter> <column_number>
```

Example:  
```
move A 1
```

The board is updated after each move, and the player’s score increases based on the bubbles popped.

---

## Advanced Features

### Error Handling
- If an invalid move is submitted, the workflow gracefully notifies the player to correct it.

### Game State Management
- All moves and scores are tracked in a JSON file specific to the branch.

### Automated Updates
- The workflow dynamically updates the PR title and posts the current game state after every move.

### Cleaning Up the Game
- The game state is automatically cleaned up by **closing the pull request**. This ensures that no unnecessary files or data persist after the game ends.

---

## Technical Details

### Files and Scripts
- **Game State JSON**:  
    The game state is stored in a JSON file at `./states/game-state-<branch-name>.json`.

- **Comment Processing**:  
    GitHub Actions listens to comments on the PR, processes valid moves, and updates the game state.

- **Python Logic**:  
    The core game logic is implemented in Python, which calculates scores and updates the state.

### Automation via GitHub Actions
The game uses GitHub Actions to:
1. Assign players based on comment authors.
2. Process comments for moves.
3. Update the PR title with the current game state.
4. Post the game board and scores as PR comments.

---

## Enjoy the Game 🎈
The Bubble Pop Game is a great way to add some fun to your GitHub workflow. Compete, strategize, and celebrate your victories directly in your Pull Requests! 🏆

---

## Acknowledgements
This project has heavily utilized GitHub Copilot and ChatGPT for code suggestions, documentation, and overall development assistance.
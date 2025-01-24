import json
import math
import os
import random

GAME_FILE = "game_state.json"

def load_game_state():
    with open(GAME_FILE, "r") as f:
        return json.load(f)

def save_game_state(state):
    with open(GAME_FILE, "w") as f:
        json.dump(state, f)

def render_board(grid, p1_defense, p2_defense):
    board = ""
    for i, row in enumerate(grid):
        defense = " "
        if i == p1_defense:
            defense = "D1"
        elif i == p2_defense:
            defense = "D2"
        board += defense + " " + " ".join(row) + "\n"
    return board

def simulate_shot(angle, power, grid, p1_defense, p2_defense):
    # Convert angle to radians
    angle_rad = math.radians(angle)
    dx = round(power * math.cos(angle_rad))
    dy = round(power * math.sin(angle_rad))

    # Start position (bottom of the board)
    x, y = len(grid) - 1, len(grid[0]) // 2

    # Simulate trajectory
    while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        if grid[x][y] != "-":  # Hit bubble
            grid[x][y] = "-"  # Remove bubble
            break
        if x == p1_defense or x == p2_defense:  # Hit defense block
            break
        x -= dy
        y += dx
    return grid

def main():
    game_state = load_game_state()
    grid = game_state["grid"]
    p1_defense = game_state["player1_defense"]
    p2_defense = game_state["player2_defense"]
    next_turn = game_state["next_turn"]

    # Get player action
    action = os.environ.get("GITHUB_EVENT_COMMENT_BODY")
    if action.startswith("shoot"):
        _, angle, power = action.split()
        grid = simulate_shot(int(angle), int(power), grid, p1_defense, p2_defense)
    elif action.startswith("move"):
        _, direction = action.split()
        if next_turn == "player1" and direction == "up":
            game_state["player1_defense"] = max(0, p1_defense - 1)
        elif next_turn == "player1" and direction == "down":
            game_state["player1_defense"] = min(len(grid) - 1, p1_defense + 1)
        elif next_turn == "player2" and direction == "up":
            game_state["player2_defense"] = max(0, p2_defense - 1)
        elif next_turn == "player2" and direction == "down":
            game_state["player2_defense"] = min(len(grid) - 1, p2_defense + 1)

    # Switch turn
    game_state["next_turn"] = "player2" if next_turn == "player1" else "player1"
    game_state["grid"] = grid
    save_game_state(game_state)

    # Render and print the board
    board = render_board(grid, p1_defense, p2_defense)
    print(board)

if __name__ == "__main__":
    main()

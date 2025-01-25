import json
import sys
import os
import random

GAME_STATE_FILE = "game_state.json"

# Handle a move command
def make_move(row, col):
    game_state = load_game_state()

    # Validate inputs
    if not (0 <= row < 8 and 0 <= col < 8):
        print("Invalid move: Row and Column must be between 0 and 7.")
        return

    if game_state["game_state"][row][col] != ":large_blue_circle:":
        print("Invalid move: The selected bubble spot is already occupied.")
        return

    # Get current player
    current_player = "player_a" if game_state["next_player"]["name"] == game_state["player_a"]["name"] else "player_b"
    
    # Place the bubble for the current player
    bubble_type = game_state[current_player]["bubble_emoji"]
    game_state["game_state"][row][col] = bubble_type

    # Check for matches after the move
    if check_matches(game_state["game_state"], row, col, bubble_type):
        pop_bubbles(game_state["game_state"], row, col, bubble_type)
        game_state[current_player]["score"] += 1  # Increment player's score
    else:
        print("No match found!")

    # Update the next player
    game_state["next_player"]["name"] = game_state["player_b"]["name"] if current_player == "player_a" else game_state["player_a"]["name"]
    game_state["next_player"]["emoji"] = game_state["player_b"]["emoji"] if current_player == "player_a" else game_state["player_a"]["emoji"]

    save_game_state(game_state)
    print("Move registered!")
    print(json.dumps(game_state, indent=4))

# Check for a match-3 (or more) horizontally, vertically, and diagonally
def check_matches(grid, row, col, bubble_type):
    match_found = False

    # Horizontal, Vertical, Diagonal checks
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dr, dc in directions:
        match = [(row, col)]
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8 and grid[r][c] == bubble_type:
            match.append((r, c))
            r, c = r + dr, c + dc
        if len(match) >= 3:
            match_found = True
            break

    return match_found

# Pop bubbles by setting them to an empty space (":large_blue_circle:")
def pop_bubbles(grid, row, col, bubble_type):
    for r in range(8):
        for c in range(8):
            if grid[r][c] == bubble_type:
                grid[r][c] = ":large_blue_circle:"  # Reset bubble spot to empty

# Load game state from file
def load_game_state():
    if not os.path.exists(GAME_STATE_FILE):
        print("Error: Game state file not found. Starting a new game.")
        return initialize_game_state()

    with open(GAME_STATE_FILE, "r") as f:
        return json.load(f)

# Initialize a new game state
# def initialize_game_state():
#     # Generate an 8x8 grid with empty bubble spots
#     game_state = {
#         "player_a": {
#             "name": "Player A",
#             "score": 0,
#             "emoji": ":a:"
#         },
#         "player_b": {
#             "name": "Player B",
#             "score": 0,
#             "emoji": ":b:"
#         },
#         "next_player": "Player A",
#         "game_state": [[":large_blue_circle:" for _ in range(8)] for _ in range(8)]
#     }
#     return game_state

# Save game state to file
def save_game_state(game_state):
    with open(GAME_STATE_FILE, "w") as f:
        json.dump(game_state, f, indent=4)

# Main function to handle command-line arguments
def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python bubble_pop_game.py start             # Start a new game")
        print("  python bubble_pop_game.py move <row> <col>  # Make a move")
        sys.exit(1)

    command = sys.argv[1]

    if command == "move":
        if len(sys.argv) != 4:
            print("Usage: python bubble_pop_game.py move <row> <col>")
            sys.exit(1)
        try:
            row = int(sys.argv[2])
            col = int(sys.argv[3])
            make_move(row, col)
        except ValueError:
            print("Row and Column must be integers.")
    # elif command == "start":
    #     game_state = initialize_game_state()
    #     save_game_state(game_state)
    #     print("New game started!")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

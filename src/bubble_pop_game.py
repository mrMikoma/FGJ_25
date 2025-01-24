import json
import sys
import os

GAME_STATE_FILE = "game_state.json"

# Initialize a new game
def start_game():
    initial_game_state = {
        "player_a": {
            "name": "Player A",
            "score": 0
        },
        "player_b": {
            "name": "Player B",
            "score": 0
        },
        "next_player": "First comment will be made by Player A",
        "game_state": [
            [":large_blue_circle:"] * 10 for _ in range(10)
        ]
    }

    save_game_state(initial_game_state)
    print("New game initialized!")
    print(json.dumps(initial_game_state, indent=4))

# Handle a move command
def make_move(row, col):
    game_state = load_game_state()

    # Validate inputs
    if not (0 <= row < 10 and 0 <= col < 10):
        print("Invalid move: Row and Column must be between 0 and 9.")
        return

    if game_state["game_state"][row][col] != ":large_blue_circle:":
        print("Invalid move: The selected bubble is already popped.")
        return

    # Update the game state
    current_player = "player_a" if game_state["next_player"] == game_state["player_a"]["name"] else "player_b"
    game_state["game_state"][row][col] = ":boom:"  # Pop the bubble
    game_state[current_player]["score"] += 1  # Increment player's score
    game_state["next_player"] = game_state["player_b"]["name"] if current_player == "player_a" else game_state["player_a"]["name"]

    save_game_state(game_state)
    print("Move registered!")
    print(json.dumps(game_state, indent=4))

# Load game state from file
def load_game_state():
    if not os.path.exists(GAME_STATE_FILE):
        print("Error: Game state file not found. Start a new game first.")
        sys.exit(1)

    with open(GAME_STATE_FILE, "r") as f:
        return json.load(f)

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

    if command == "start":
        start_game()
    elif command == "move":
        if len(sys.argv) != 4:
            print("Usage: python bubble_pop_game.py move <row> <col>")
            sys.exit(1)
        try:
            row = int(sys.argv[2])
            col = int(sys.argv[3])
            make_move(row, col)
        except ValueError:
            print("Row and Column must be integers.")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

import json
import sys
import os

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

    # Get current player by ID (use 'id' instead of 'name')
    current_player_id = game_state["next_turn"]["id"]
    current_player = "player_a" if current_player_id == "a" else "player_b"
    
    # Get the current player's bubble emoji
    bubble_type = game_state[current_player]["bubble_emoji"]
    game_state["game_state"][row][col] = bubble_type

    # Check for matches after the move
    if check_matches(game_state["game_state"], row, col, bubble_type):
        popped_count = pop_bubbles(game_state["game_state"], row, col, bubble_type, game_state[current_player]["emoji"])
        game_state[current_player]["score"] += popped_count
    else:
        print("No match found!")

    # Update the next player by switching the 'id' between 'a' and 'b'
    game_state["next_turn"] = game_state["player_b"] if current_player_id == "a" else game_state["player_a"]

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

# Function to check for matches
def check_matches(game_state, row, col, bubble_type):
    # Check for horizontal match
    horizontal_count = 1
    for i in range(col - 1, -1, -1):  # left side
        if game_state[row][i] == bubble_type:
            horizontal_count += 1
        else:
            break
    for i in range(col + 1, 8):  # right side
        if game_state[row][i] == bubble_type:
            horizontal_count += 1
        else:
            break

    # Check for vertical match
    vertical_count = 1
    for i in range(row - 1, -1, -1):  # up side
        if game_state[i][col] == bubble_type:
            vertical_count += 1
        else:
            break
    for i in range(row + 1, 8):  # down side
        if game_state[i][col] == bubble_type:
            vertical_count += 1
        else:
            break

    # If there are 3 or more matching bubbles, return True
    if horizontal_count >= 3 or vertical_count >= 3:
        return True
    return False

# Function to pop bubbles
def pop_bubbles(game_state, row, col, bubble_type, player_emoji):
    # Track the number of bubbles popped
    popped_count = 1  # Start with the initial bubble

    # Replace the bubble at the specified position
    game_state[row][col] = player_emoji  # Empty the popped bubble

    # Pop horizontal bubbles
    for i in range(col - 1, -1, -1):  # Left side
        if game_state[row][i] == bubble_type:
            game_state[row][i] = player_emoji
            popped_count += 1
        else:
            break
    for i in range(col + 1, 8):  # Right side
        if game_state[row][i] == bubble_type:
            game_state[row][i] = player_emoji
            popped_count += 1
        else:
            break

    # Pop vertical bubbles
    for i in range(row - 1, -1, -1):  # Up side
        if game_state[i][col] == bubble_type:
            game_state[i][col] = player_emoji
            popped_count += 1
        else:
            break
    for i in range(row + 1, 8):  # Down side
        if game_state[i][col] == bubble_type:
            game_state[i][col] = player_emoji
            popped_count += 1
        else:
            break

    print(f"Bubbles popped: {popped_count}")
    return popped_count

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
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

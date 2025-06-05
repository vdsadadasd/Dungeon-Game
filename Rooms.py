class Room:
    def __init__(self, row, col):
        self.row = row
        self.col = col

# -- Original grid made by myself --
# def get_grid(player_row, player_col): 
#     for r in range(2):
#         row = ""
#         for c in range(2):
#             if r == player_row and c == player_col:
#                 row = row + " P "
#             else:
#                 row = row + " . "
#         print(row)


# Made by AI for the purpose of user experience, does not effect backend, helped with cheat mode layout
def get_grid(
    player_row, player_col, grid_size,
    cheat_mode=False, bow_pos=None, arrow_pos=None, guardian_pos=None,
    inventory=None, player_health=None, player_max_health=100
):
    inventory = inventory or []
    # Build inventory summary (no duplicates, correct quantities)
    item_counts = {}
    for item in inventory:
        if getattr(item, "quantity", 1) > 0:
            key = getattr(item, "name", str(item))
            item_counts[key] = item_counts.get(key, 0) + getattr(item, "quantity", 1)
    inv_lines = ["Inventory:"]
    if not item_counts:
        inv_lines.append(" (empty)")
    else:
        for name, qty in item_counts.items():
            inv_lines.append(f" {name} x{qty}")

    # Print inventory above the grid
    for line in inv_lines:
        print(line)
    print()  # Blank line for spacing

    # Determine what to show in the grid
    has_bow = any(getattr(item, "name", "").lower() == "bow" and getattr(item, "quantity", 1) > 0 for item in inventory)
    has_arrow = any(getattr(item, "name", "").lower() == "arrow" and getattr(item, "quantity", 1) > 0 for item in inventory)
    bow_pos_to_show = None if has_bow else bow_pos
    arrow_pos_to_show = None if has_arrow else arrow_pos

    # Print the grid
    for r in range(grid_size):
        # Top border
        row_border = "+-----" * grid_size + "+"
        print(row_border)
        # First line: show player/guardian/bow/arrow if present
        row_content = ""
        for c in range(grid_size):
            char = "     "
            if (r, c) == (player_row, player_col):
                char = "  P  "
            elif cheat_mode:
                if guardian_pos and (r, c) == guardian_pos:
                    char = "  G  "
                elif bow_pos_to_show and (r, c) == bow_pos_to_show:
                    char = "  B  "
                elif arrow_pos_to_show and (r, c) == arrow_pos_to_show:
                    char = "  A  "
            row_content += f"|{char}"
        row_content += "|"
        print(row_content)
        # Second line: always empty
        print("|" + "     |" * grid_size)
    # Bottom border
    print("+-----" * grid_size + "+")

    # Print health bar below the grid, only once
    if player_health is not None:
        bar_length = 20
        hp = max(0, min(player_health, player_max_health))
        filled = int(bar_length * hp // player_max_health)
        empty = bar_length - filled
        bar = "[" + "#" * filled + "-" * empty + f"] {hp}/{player_max_health} HP"
        print("Health:")
        print(f" {bar}")
    print()  # Blank line for spacing before move options
















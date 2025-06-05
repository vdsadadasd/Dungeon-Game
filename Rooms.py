class Room:
    def __init__(self, row, col):
        self.row = row
        self.col = col

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

    # Grid settings
    CELL_WIDTH = 13
    CELL_HEIGHT = 5

    def center_cell(content):
        content_str = str(content) if content else ""
        pad = CELL_WIDTH - len(content_str)
        left = pad // 2
        right = pad - left
        return " " * left + content_str + " " * right

    # Priority: Player > Guardian > Bow > Arrow
    def cell_icon(r, c):
        if (r, c) == (player_row, player_col):
            return "P"
        if cheat_mode:
            if guardian_pos and (r, c) == guardian_pos:
                return "G"
            if bow_pos and (r, c) == bow_pos and not any(getattr(item, "name", "").lower() == "bow" and getattr(item, "quantity", 1) > 0 for item in inventory):
                return "B"
            if arrow_pos and (r, c) == arrow_pos and not any(getattr(item, "name", "").lower() == "arrow" and getattr(item, "quantity", 1) > 0 for item in inventory):
                return "A"
        return ""

    # Print the grid (fancy, with thick borders and more space)
    thick_h = "═" * CELL_WIDTH
    thick_v = "║"
    cross = "╬"
    top_left = "╔"
    top_right = "╗"
    bottom_left = "╚"
    bottom_right = "╝"
    left_t = "╠"
    right_t = "╣"
    top_t = "╦"
    bottom_t = "╩"

    # Top border
    top_border = top_left + (top_t.join([thick_h]*grid_size)) + top_right
    print(top_border)
    for r in range(grid_size):
        # Each cell is CELL_HEIGHT tall
        for h in range(CELL_HEIGHT):
            row_content = ""
            for c in range(grid_size):
                if h == CELL_HEIGHT // 2:
                    icon = cell_icon(r, c)
                    cell = center_cell(icon)
                else:
                    cell = " " * CELL_WIDTH
                row_content += thick_v + cell
            row_content += thick_v
            print(row_content)
        # Row separator or bottom border
        if r < grid_size - 1:
            sep = left_t + (cross.join([thick_h]*grid_size)) + right_t
            print(sep)
        else:
            bottom_border = bottom_left + (bottom_t.join([thick_h]*grid_size)) + bottom_right
            print(bottom_border)

    # Print health bar below the grid, only once
    if player_health is not None:
        bar_length = 30
        hp = max(0, min(player_health, player_max_health))
        filled = int(bar_length * hp // player_max_health)
        empty = bar_length - filled
        bar = "[" + "#" * filled + "-" * empty + f"] {hp}/{player_max_health} HP"
        print("Health:")
        print(f" {bar}")
    print()  # Blank line for spacing before move options
















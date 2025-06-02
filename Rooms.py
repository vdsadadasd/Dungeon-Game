class Room:
    def __init__(self,row, col):
        self.row = row
        self.col = col
        
    
# -- Original grid made by myself --
# def get_grid(player_row, player_col): 
#     for r in range(5):
#         row = ""
#         for c in range(5):
#             if r == player_row and c == player_col:
#                 row = row + " P "
#             else:
#                 row = row + " . "
#         print(row)


# Made by AI for the purpose of user experience, does not effect backend
def get_grid(player_row, player_col, grid_size, cheat_mode=False, bow_pos=None, arrow_pos=None, guardian_pos=None, inventory=None):
    inventory = inventory or []
    inv_lines = ["Inventory:"]
    item_counts = {}
    # Use item name as key, sum all quantities for that name
    for item in inventory:
        if item.name in item_counts:
            item_counts[item.name] += item.quantity
        else:
            item_counts[item.name] = item.quantity
    if not item_counts:
        inv_lines.append(" (empty)")
    else:
        for name, qty in item_counts.items():
            inv_lines.append(f" {name} x{qty}")
    max_inv_lines = max(len(inv_lines), grid_size * 2 + 1)
    inv_lines += [""] * (max_inv_lines - len(inv_lines))

    has_bow = any(item.name.lower() == "bow" and item.quantity > 0 for item in inventory)
    has_arrow = any(item.name.lower() == "arrow" and item.quantity > 0 for item in inventory)
    bow_pos_to_show = None if has_bow else bow_pos
    arrow_pos_to_show = None if has_arrow else arrow_pos

    for r in range(grid_size):
        grid_row = ""
        for c in range(grid_size):
            grid_row += "+-----"
        grid_row += "+"
        inv_idx = r * 2
        print(grid_row + "   " + (inv_lines[inv_idx] if inv_idx < len(inv_lines) else ""))
        for line in range(2):
            row_str = ""
            for c in range(grid_size):
                char = "     "
                if (r, c) == (player_row, player_col) and line == 0:
                    char = "  P  "
                elif cheat_mode and line == 0:
                    if guardian_pos and (r, c) == guardian_pos:
                        char = "  G  "
                    elif bow_pos_to_show and (r, c) == bow_pos_to_show:
                        char = "  B  "
                    elif arrow_pos_to_show and (r, c) == arrow_pos_to_show:
                        char = "  A  "
                row_str += f"|{char}"
            row_str += "|"
            inv_idx = r * 2 + line + 1
            print(row_str + "   " + (inv_lines[inv_idx] if inv_idx < len(inv_lines) else ""))
    grid_row = ""
    for c in range(grid_size):
        grid_row += "+-----"
    grid_row += "+"
    print(grid_row)
















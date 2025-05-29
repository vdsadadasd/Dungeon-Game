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
def get_grid(player_row, player_col, grid_size, cheat_mode=False, bow_pos=None, arrow_pos=None, guardian_pos=None):
    for r in range(grid_size):
        for c in range(grid_size):
            print("+-----", end='')
        print("+")
        for line in range(2):
            for c in range(grid_size):
                char = "     "
                if (r, c) == (player_row, player_col) and line == 0:
                    char = "  P  "
                elif cheat_mode and line == 0:
                    if bow_pos and (r, c) == bow_pos:
                        char = "  B  "
                    elif arrow_pos and (r, c) == arrow_pos:
                        char = "  A  "
                    elif guardian_pos and (r, c) == guardian_pos:
                        char = "  G  "
                print(f"|{char}", end='')
            print("|")
    for c in range(grid_size):
        print("+-----", end='')
    print("+")







    









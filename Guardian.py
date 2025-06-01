import random

class Guardian:
    def __init__(self, guardian_health, guardian_strength):
        self.guardian_health = guardian_health
        self.guardian_strength = guardian_strength 
        self.row = None
        self.col = None

    def guardian_attack(self, damage):
        damage.player_health = damage.player_health - self.guardian_strength  
        if damage.player_health < 0:
            damage.player_health = 0
        
    def move_guardian(self, grid_size):
        if random.random() < 0.5:
            move_type = random.choice(["row", "col"])
            move_direction = random.choice([-1, 1])

            if move_type == "row":
                new_row = self.row + move_direction
                if 0 <= new_row < grid_size:
                    self.row = new_row
            else:
                new_col = self.col + move_direction
                if 0 <= new_col < grid_size:
                    self.col = new_col

        

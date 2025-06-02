import random
import sys
import time
from assets import take_aim_art

def slow_text(text, delay=0.04):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def slow_art(art, line_delay=0.1):
        lines = art.strip('\n').split('\n')
        for line in lines:
            print(line)
            time.sleep(line_delay)

class Player:
    def __init__(self, player_health, player_strength, grid_size):
        self.player_health = player_health
        self.player_strength = player_strength  
        self.inventory = []  
        self.current_room = None
        self.row = random.randint(0, grid_size - 1)
        self.col = random.randint(0, grid_size - 1)
        self.grid_size = grid_size

    def player_attack(self, guardian):
        guardian.guardian_health -= self.player_strength  
        if guardian.guardian_health < 0:
            guardian.guardian_health = 0
        slow_text(f"You did {self.player_strength} damage. The guardian has {guardian.guardian_health} HP remaining.", 0.03)
    
    def get_health(self):
        slow_text(f"Current HP: {self.player_health}", 0.03)
    
    def get_inventory(self):
        if self.inventory == []:
            slow_text("Your inventory is empty", 0.03)
        else:
            slow_text("Your inventory:", 0.03)
            for i, item in enumerate(self.inventory, 1):
                slow_text(f"{i}: {item.name} x{item.quantity}", 0.03)
    
    def use_arrow(self):
        slow_text("You have an arrow, Use them with a bow", 0.03)

    def use_bow_encounter(self, guardian):
        slow_text("You hit the guardian with your bow! 100 guardian dealt.", 0.03)
        guardian.guardian_health -= 100
        if guardian.guardian_health < 0:
            guardian.guardian_health = 0
        slow_text(f"Guardian health is now {guardian.guardian_health}.", 0.03)
        

    def use_bow(self, guardian):
        if not any(item.name == "Bow" for item in self.inventory):
            slow_text("Bow not in inventory", 0.03)
            return
        if not any(item.name == "Arrow" for item in self.inventory):
            slow_text("No arrows left", 0.03)
            return
        slow_text("You take aim", 0.06)
        slow_art(take_aim_art())
        slow_text("Shoot direction (W/A/S/D): ", 0.03)
        direction = input().upper()

        for item in self.inventory:
            if item.name == "Arrow" and item.quantity > 0:
                item.quantity -= 1
                if item.quantity == 0:
                    self.inventory.remove(item)
                break

        target_row, target_col = self.row, self.col
        if direction == "W":
            target_row -= 1
        elif direction == "S":
            target_row += 1
        elif direction == "A":
            target_col -= 1
        elif direction == "D":
            target_col += 1
        else:
            slow_text("Invalid direction.", 0.03)
            return False

        if (target_row, target_col) == (guardian.row, guardian.col):
            slow_text("Critical hit! The guardian's life force fades away", 0.03)
            guardian.guardian_health = 0 
            return False
        else:
            slow_text("The arrow missed.", 0.03)
            slow_text("A new arrow has spawned.", 0.03)
            return True
            

    def use_item(self, guardian):
        while True:
            if guardian.guardian_health <= 0:
                break
            else:
                pass
                slow_text("What item would you like to use: ", 0.03)
                item_choice = input().lower()
                for item in self.inventory:
                    if item.name.lower() == item_choice and item.quantity > 0:
                        if item.name == "Bow":
                            self.use_bow(guardian)
                            if guardian.guardian_health <= 0:
                                return 
                        elif item.name == "Arrow":
                            self.use_arrow()
                        break
                else:
                    slow_text("Item not in inventory", 0.03)  

                slow_text("Would you like to use anything else? (Y/N): ", 0.03)
                again = input().lower()
                if again != "y":
                    break
                

    def move_player(self, direction):
        direction = direction.upper()
        max_index = self.grid_size - 1
        if direction == "W" and self.row > 0:
            self.row -= 1
            return True
        elif direction == "S" and self.row < max_index:
            self.row += 1
            return True
        elif direction == "A" and self.col > 0:
            self.col -= 1
            return True
        elif direction == "D" and self.col < max_index:
            self.col += 1
            return True
        return False

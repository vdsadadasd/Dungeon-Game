import random

class Player:
    def __init__(self, player_health, player_strength, grid_size):
        self.player_health = player_health
        self.player_strength = player_strength  
        self.inventory = []  
        self.bow_quiver = 0
        self.current_room = None
        self.row = random.randint(0, grid_size - 1)
        self.col = random.randint(0, grid_size - 1)

    def player_attack(self, damage):
        damage.guardian_health -= self.player_strength  
        if damage.guardian_health < 0:
            damage.guardian_health = 0
        print(f"You did {self.player_strength} damage. The guardian has {damage.guardian_health} HP remaining.")
    
    def get_health(self):
        print(f"Current HP: {self.player_health}")
    
    def get_inventory(self):
        if self.inventory == []:
            print("Your inventory is empty")
        else:
            print("Your inventory:")
            for i, item in enumerate(self.inventory, 1):
                print(f"{i}: {item.name} x{item.quantity}")

    def use_bow(self):
        for item in self.inventory:
            if item.name == "Bow" and item.quantity > 0:
                if self.bow_quiver > 0:
                    direction = input("What direction do you want to shoot? W/A/S/D").upper()
                    self.bow_quiver -= 1
                    print(f"You currently have {self.bow_quiver}/6 arrows in the quiver")
                else:
                    print("No arrows in the quiver")                             
                return
        print("Not in inventory")


    def use_arrow(self):
        for item in self.inventory:
            if "Bow" in item.name:
                for arrow in self.inventory:
                    if arrow.name == "Arrow" and arrow.quantity > 0:
                        self.bow_quiver += arrow.quantity
                        if self.bow_quiver > 6:
                            self.bow_quiver = 6
                        print(f"You inserted {arrow.quantity} arrow into your quiver. quiver: {self.bow_quiver}/1")
                        arrow.quantity = 0
                        self.inventory.remove(arrow)
                        return
                print("Not in inventory")
                return
        print("You don't have a bow")

    def use_item(self):
        while True:
            item_choice = input("What item would you like to use: ").lower()
            for item in self.inventory:
                if item.name.lower() == item_choice and item.quantity > 0:
                    if item.name == "Bow":
                        self.use_bow()
                    elif item.name == "Arrow":
                        self.use_arrow()
                    break
            else:
                print("Item not in inventory")  

            again = input("Would you like to use anything else? (Y/N): ").lower()
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

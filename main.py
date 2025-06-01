from Player import Player
from Guardian import Guardian
from Items import Items
from Rooms import Room, get_grid
from assets import guardian_encounter_art, guardian_intro_art, dungeon_art, bow_art, arrow_art, player_death, guardian_look
import os
import random
import time
import sys
import sys
import tty
import termios



def getch(): # Made by AI for the purpose of user experience, does not effect backend
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Game:
    def __init__(self):
        self.grid_size = 4
        self.P1 = Player(100, 20, self.grid_size)
        self.guard = Guardian(200, 40)
        self.bow = Items("Bow", "Weapon", 1)
        self.arrow = Items("Arrow", "Ammo", 1)
        self.cheat_mode = False
        
    # Made by AI for the purpose of user experience, does not effect backend
    def slow_text(self, text, delay=0.05):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    # Made by AI for the purpose of user experience, does not effect backend
    def slow_art(self, art, line_delay=0.1):
        lines = art.strip('\n').split('\n')
        for line in lines:
            print(line)
            time.sleep(line_delay)

    def guard_encounter(self):
        import random

        self.clear_screen()
        print(guardian_encounter_art())
        self.slow_text("You encounter it, what will you do- test git?", 0.04)
        option = input("Attack(A) or Attempt to Run(R): ").upper()

        if option == "R":
            if random.random() < 0.6:
                self.slow_text("You managed to escape\n", 0.03)
                self.slow_text("For now...", 0.25)
                input("Press Enter to continue...")
                self.clear_screen()
            else:
                self.slow_text("You attempted to escape \nIt managed to hit you on way out.", 0.04)
                self.P1.player_health = self.P1.player_health - 50
                if self.P1.player_health < 0:
                    self.P1.player_health = 0
                self.P1.get_health()
                input("Press Enter to continue...")
                self.clear_screen()

        else:
            self.slow_text("How will you attack?\n", 0.04)
            attack = input("Melee(M) or Shoot your Bow(B)\n").upper()

            if attack == "M":
                self.P1.player_attack(self.guard)
                input("Press Enter to continue...")

            elif attack == "B":
                if any(item.name == "Bow" for item in self.P1.inventory):
                    self.P1.use_bow_encounter(self.guard)
                    input("Press Enter to continue...")
                else:
                    print("You don't have a bow in your inventory!")
                    input("Press Enter to continue...")

            else:
                print("Invalid choice. You hesitate and miss your chance!")
                input("Press Enter to continue...")

            if random.random() < 0.5:
                self.slow_text("The Guardian cowers and retreats into the shadows...", 0.04)
                input("Press Enter to continue...")
            else:
                self.slow_text("The Guardian is enraged and lunges at you!", 0.04)
                dodge = input("Quick! Dodge Left (L) or Right (R)? ").upper()
                while dodge not in ["L", "R"]:
                    dodge = input("Please choose L or R: ").upper()

                guardian_choice = random.choice(["L", "R"])
                self.slow_text("The Guardian strikes!", 0.04)
                if dodge == guardian_choice:
                    self.slow_text("You failed to dodge!", 0.04)
                    self.P1.player_health -= self.guard.guardian_strength
                    if self.P1.player_health < 0:
                        self.P1.player_health = 0
                    print(f"You took {self.guard.guardian_strength} damage. Your health is now {self.P1.player_health}.")
                else:
                    self.slow_text("You dodged just in time!", 0.04)
                    self.slow_text("The guardian cowers and retreats into the shadows...", 0.04)
                input("Press Enter to continue...")
        
        if self.guard.guardian_health > 0:
            self.guardian_spawn()
    
    def difficulty_select(self):
        while True:
            self.clear_screen()
            self.slow_text("========================================", 0.01)
            self.slow_text("         Select Difficulty", 0.05)
            self.slow_text("========================================", 0.01)
            self.slow_text("1. Normal (4x4)", 0.03)
            self.slow_text("2. Brutal (5x5)", 0.03)
            self.slow_text("----------------------------------------", 0.01)
            
            choice = input("Enter 1 or 2: ")
            if choice == "1":
                self.grid_size = 4
                break
            elif choice == "2":
                self.grid_size = 5
                break
            else:
                self.slow_text("Invalid choice. Try again.", 0.03)

        cheat = input("Enable Cheat Mode? (Y/N): ").upper()
        if cheat == "Y":
            self.cheat_mode = True 
        else:
            self.cheat_mode = False

        self.slow_text("========================================", 0.01)
        choice2 = input("Skip Intro? (Y/N): ").upper()
        if choice2 == "N":
            self.intro()


    def guard_intro(self):
        self.clear_screen()
        print(guardian_intro_art())
        print()
        self.slow_text("...\n", 0.5)
        self.slow_text("The Guardian sees you.\n", 0.1)
        self.slow_text("“Your fate is sealed.”\n", 0.12)
        self.slow_text("You manage to escape.\n", 0.15)
        self.slow_text("For now...\n", 0.3)
        input("Press Enter to continue...")
        self.clear_screen()

    def found_bow(self):
        self.slow_text("you've found a bow...", 0.05)

    def found_arrow(self):
        self.slow_text("you've found an arrow...", 0.05)

    def intro(self):
        self.clear_screen()
        print(dungeon_art())
        self.slow_text("...\n", 0.5)
        self.slow_text("You wake up in a cold, dark dungeon.\n", 0.07)
        self.slow_text("Your head throbs... you can't remember how you got here.\n", 0.07)
        self.slow_text("You hear something lurking in the shadows.\n", 0.07)
        self.slow_text("You must find a way out... before it's too late.\n", 0.07)
        input("Press Enter to begin...")
        self.guard_intro()
        self.clear_screen()
    
    def player_death(self):
        self.clear_screen()
        self.slow_text("\n========================================", 0.01)
        self.slow_text("          You have been defeated!         ", 0.05)
        self.slow_text("========================================\n", 0.01)
        self.slow_art(player_death())
        self.slow_text("Your fate is sealed\n", 0.07)
        self.slow_text("Better luck next time!", 0.05)
        input("Press Enter to exit...")
    
    def guardian_death(self):
        self.clear_screen()
        self.slow_text("\n========================================", 0.01)
        self.slow_text("          You have defeated it!         ", 0.05)
        self.slow_text("========================================\n", 0.01)
        self.slow_text("You feel a shiver down your spine...", 0.05)
        self.slow_art(guardian_look())
        self.slow_text("Well done", 0.05)
        input("Press Enter to exit...")
        
        

    def guardian_spawn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) != (self.P1.row, self.P1.col):
                self.guard.row = row
                self.guard.col = col
                break

    def bow_spawn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) != (self.P1.row, self.P1.col):
                self.bow.row = row
                self.bow.col = col
                break

    def arrow_spawn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) != (self.P1.row, self.P1.col) and (row, col) != (self.bow.row, self.bow.col):
                self.arrow.row = row
                self.arrow.col = col
                break

    def clear_screen(self):
        os.system('clear') # Made by AI for the purpose of user experience, does not effect backend

    def start(self):
        self.difficulty_select()
        self.P1.grid_size = self.grid_size
        self.bow_spawn()
        self.arrow_spawn()
        self.guardian_spawn()

        while True:
            if self.P1.player_health <= 0:
                self.player_death()
                break
            elif self.guard.guardian_health <= 0:
                self.guardian_death()
                break
            else:
                pass

            self.clear_screen()
            get_grid(
            self.P1.row,
            self.P1.col,
            self.grid_size,
            self.cheat_mode,
            bow_pos=(self.bow.row, self.bow.col),
            arrow_pos=(self.arrow.row, self.arrow.col),
            guardian_pos=(self.guard.row, self.guard.col),
            inventory=self.P1.inventory 
        )

            messages = ["You hear it...", "Footsteps approach...", "Something is nearby..."]
            distance = abs(self.P1.row - self.guard.row) + abs(self.P1.col - self.guard.col)
            if distance == 1:
                print()
                self.slow_text(random.choice(messages), 0.04)

            # Original Move Input
            # move = input("Move(W/A/S/D),Inventory(I), Quit(Q): ").upper()

            print("Move(W/A/S/D), Use item(U): ", end='', flush=True)
            move = getch().upper() # I used AI to get the input without waiting for Enter key
            print(move)  

            if move in ["W", "A", "S", "D"]:
                if not self.P1.move_player(move):
                    self.slow_text("Invalid movement, try again.", 0.04)

                else:
                    self.clear_screen()

                self.guard.move_guardian(self.grid_size)

                if (self.P1.row, self.P1.col) == (self.bow.row, self.bow.col) and self.bow not in self.P1.inventory:
                    self.found_bow()
                    self.P1.inventory.append(self.bow)
                    self.bow.row = None
                    self.bow.col = None

                if (self.P1.row, self.P1.col) == (self.arrow.row, self.arrow.col) and self.arrow not in self.P1.inventory:
                    self.found_arrow()
                    self.P1.inventory.append(self.arrow)
                    self.arrow.row = None
                    self.arrow.col = None

                if (self.P1.row, self.P1.col) == (self.guard.row, self.guard.col):
                    self.guard_encounter()

            elif move == "U":
                if not self.P1.inventory:
                    self.slow_text("Your inventory is empty", 0.01)
                    self.slow_text("Press Enter to continue...", 0.01)
                    input()
                else:
                    self.P1.use_item(self.guard)
                    self.slow_text("Press Enter to continue...", 0.01)
                    input()
            

            else:
                self.slow_text("Invalid input. Use W, A, S, D, I, or Q.", 0.01)
                self.slow_text("Press Enter to continue...", 0.01)
                input()

game = Game()
game.start()

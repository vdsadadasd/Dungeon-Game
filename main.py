from Player import Player
from Guardian import Guardian
from Items import Items
from Rooms import Room, get_grid
from assets import guardian_encounter_art, dungeon_art, player_death, guardian_look
import os
import random
import time
import sys
import tty
import termios
import subprocess
import signal

# --Important Note--

# If I forget to mention when uploading, since I have used AI for audio that runs directly in the terminal
# There is a chance that it wont stop playing if you accidently close the terminal
# In the case that happens, you can run the following command in your terminal to stop all audio:
# sh stop_audio.sh (The script is included in the file, made by AI), it kills the afplay process in the code

EERIE_MUSIC_PATH = "assets/eerie_music.wav"
ENCOUNTER_MUSIC_PATH = "assets/encounter.wav"
VICTORY_MUSIC_PATH = "assets/victory.mp3"
DEATH_MUSIC_PATH = "assets/death.mp3"
ITEM_PICKUP_SOUND_PATH = "assets/item_pickup.aiff"
DIFFICULTY_SELECT_MUSIC_PATH = "assets/difficulty_select.mp3"

def getch(): # Made by AI for the purpose of user experience, does not effect backend, this removes the need for pressing enter after each input
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
        self.P1 = Player(100, 35, self.grid_size)
        self.guard = Guardian(200, 50)
        self.bow = Items("Bow", "Weapon", 1)
        self.arrow = Items("Arrow", "Ammo", 1)
        self.cheat_mode = False
        self.music_proc = None  # Track the current music process
            
        
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

     # Made by AI for the purpose of user experience, does not effect backend
    def play_music(self, path, loop=True):
        self.stop_music()
        abs_path = os.path.abspath(path)
        if loop:
            # Save the shell process so we can kill it directly
            self.music_proc = subprocess.Popen(
                ['bash', '-c', f'trap "" SIGHUP; while true; do afplay "{abs_path}"; done'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )
            self.music_shell_pid = self.music_proc.pid
        else:
            self.music_proc = subprocess.Popen(
                ['afplay', abs_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.music_shell_pid = None

    def stop_music(self):
        # Stop the current music process if running
        if hasattr(self, 'music_proc') and self.music_proc and self.music_proc.poll() is None:
            try:
                os.killpg(os.getpgid(self.music_proc.pid), signal.SIGTERM)
            except Exception:
                try:
                    self.music_proc.terminate()
                except Exception:
                    pass
            self.music_proc = None
        # Kill the shell process if it exists (for looped music)
        if hasattr(self, 'music_shell_pid') and self.music_shell_pid:
            try:
                os.killpg(os.getpgid(self.music_shell_pid), signal.SIGTERM)
            except Exception:
                pass
            self.music_shell_pid = None
        # Kill any stray afplay processes
        os.system("killall afplay 2>/dev/null")

    def play_sound(self, path):
        abs_path = os.path.abspath(path)
        subprocess.Popen(
            ['afplay', abs_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


    def audio_warning(self):
        self.slow_text("For maximum enjoyment, please increase your volume", 0.05)
        self.clear_screen()


    def guard_encounter(self):
        self.stop_music()
        self.play_music(ENCOUNTER_MUSIC_PATH, loop=True)
        try:
            self.clear_screen()
            print(guardian_encounter_art())
            self.slow_text("You encounter it, what will you do?", 0.04)
            option = input("Attack(A) or Attempt to Run(R): ").upper()

            if option == "R":
                # if user tries to run, there is a 40% chance they escape
                if random.random() < 0.4:
                    self.slow_text("You managed to escape\n", 0.03)
                    self.slow_text("For now...", 0.25)
                    input("Press Enter to continue...")
                    self.clear_screen()
                else:
                # If they fail to escape, the guardian attacks them, with chance ranging from higher to lower damage
                    rand = random.randint(1, 3)
                    if rand == 1:
                        self.slow_text("You attempted to escape.\nIt managed to hit you on the way out.", 0.04)
                        dmg = 50
                    elif rand == 2:
                        self.slow_text("You try to run, but the Guardian slashes your back!", 0.04)
                        dmg = 35
                    else:
                        self.slow_text("You stumble as you flee and the Guardian claws at you!", 0.04)
                        dmg = 40
                    self.P1.player_health = self.P1.player_health - dmg
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
                    # Simply checks if bow is appended anywhere in the inventory, important if they found the arrow first
                    if any(item.name == "Bow" for item in self.P1.inventory):
                        for item in self.P1.inventory:
                            if item.name == "Arrow" and item.quantity > 0: #Checks for arrow and removes when used
                                item.quantity = item.quantity - 1
                                if item.quantity == 0:
                                    self.P1.inventory.remove(item)
                                break
                        else:
                            print("No arrows left!")
                            input("Press Enter to continue...")
                        self.P1.use_bow_encounter(self.guard) #This function is different to shooting from across the room, as it only occurs during guardian encounter
                        print("A new arrow has spawned.")
                        self.arrow_spawn()
                        input("Press Enter to continue...")
                    else:
                        print("You don't have a bow in your inventory!")
                        input("Press Enter to continue...")

                else:
                    print("Invalid choice. You hesitate and miss your chance!") #If they dont input correctly, they miss their chance
                    input("Press Enter to continue...")

                if self.guard.guardian_health <= 0: #End of encounter, if guardian health is 0 or less
                    return
                # 50% chance the guardian will attack back, else it will cower and retreat
                if random.random() < 0.5:
                    self.slow_text("The Guardian cowers and retreats into the shadows...", 0.04)
                    input("Press Enter to continue...")
                else:
                    self.slow_text("The Guardian is enraged and lunges at you!", 0.04)
                    dodge = input("Quick! Dodge Left (L) or Right (R)? ").upper()
                    while dodge not in ["L", "R"]:
                        dodge = input("Please choose L or R: ").upper()
                    # The guardian randomly chooses a side to attack, if player guesses they exit the encounter, else they take damage
                    guardian_choice = random.choice(["L", "R"])
                    self.slow_text("The Guardian strikes!", 0.04)
                    if dodge == guardian_choice:
                        self.slow_text("You failed to dodge!", 0.04)
                        self.P1.player_health = self.P1.player_health - self.guard.guardian_strength
                        if self.P1.player_health < 0:
                            self.P1.player_health = 0
                        print(f"You took {self.guard.guardian_strength} damage. Your health is now {self.P1.player_health}.")
                    else:
                        self.slow_text("You dodged just in time!", 0.04)
                        self.slow_text("The guardian cowers and retreats into the shadows...", 0.04)
                    input("Press Enter to continue...")

            if self.guard.guardian_health > 0:
                self.guardian_spawn()
        finally:
            self.stop_music()
            self.play_music(EERIE_MUSIC_PATH, loop=True)

    def player_death(self):
        self.stop_music()
        self.play_music(DEATH_MUSIC_PATH, loop=True)
        self.clear_screen()
        self.slow_text("\n========================================", 0.01)
        self.slow_text("          You have been defeated!         ", 0.05)
        self.slow_text("========================================\n", 0.01)
        self.slow_art(player_death())
        self.slow_text("Your fate is sealed...\n", 0.07)
        self.slow_text("Do you dare to try again?", 0.05)
        input("Press Enter to exit...")
        self.stop_music()

    def guardian_death(self):
        self.stop_music()
        self.play_music(VICTORY_MUSIC_PATH, loop=True)
        self.clear_screen()
        self.slow_text("\n========================================", 0.01)
        self.slow_text("          You have defeated it!         ", 0.05)
        self.slow_text("========================================\n", 0.01)
        self.slow_text("You feel a shiver down your spine...", 0.05)
        self.slow_art(guardian_look())
        self.slow_text("It gives you one final look as it withers away", 0.05)
        self.slow_text("...", 0.9)
        input("Press Enter to exit...")
        self.stop_music()

    def title_card(self):
        title = r"""
  ____                                     
|  _ \ _   _ _ __   __ _  ___  ___  _ __  
| | | | | | | '_ \ / _` |/ _ \/ _ \| '_ \ 
| |_| | |_| | | | | (_| |  __/ (_) | | | |
|____/ \__,_|_| |_|\__, |\___|\___/|_| |_|
|  _ \  ___  ___  _|___/_ _ __ | |_       
| | | |/ _ \/ __|/ __/ _ \ '_ \| __|      
| |_| |  __/\__ \ (_|  __/ | | | |_       
|____/ \___||___/\___\___|_| |_|\__|      
        """
        self.clear_screen()
        print(title)
        self.slow_text("\nWelcome to Dungeon Descent!", 0.04)
        self.slow_text("Press Enter to continue...", 0.03)
        input()

    def difficulty_select(self):
        self.play_music(DIFFICULTY_SELECT_MUSIC_PATH, loop=True)
        self.title_card()
        while True:
            self.clear_screen()
            self.slow_text("========================================", 0.01)
            self.slow_text("         Select Difficulty", 0.05)
            self.slow_text("========================================", 0.01)
            self.slow_text("1. Normal (4x4)", 0.03)
            self.slow_text("2. Brutal (5x5)", 0.03)
            self.slow_text("3. Nightmare (5x5, your health is reduced)", 0.03)
            self.slow_text("----------------------------------------", 0.01)
            
            choice = input("Enter 1, 2 or 3: ")
            if choice == "1":
                self.grid_size = 4
                self.nightmare_mode = False
                break
            elif choice == "2":
                self.grid_size = 5
                self.nightmare_mode = False
                break
            elif choice == "3":
                self.grid_size = 5
                self.nightmare_mode = True
                break
            else:
                self.slow_text("Invalid choice. Try again.", 0.03)

        # Cheat mode input validation
        while True:
            cheat = input("Enable Cheat Mode? (Y/N): ").upper()
            if cheat == "Y":
                self.cheat_mode = True
                break
            elif cheat == "N":
                self.cheat_mode = False
                break
            else:
                self.slow_text("Invalid input. Please enter Y or N.", 0.03)

        self.slow_text("========================================", 0.01)
        # Skip intro input validation
        while True:
            choice2 = input("Skip Intro? (Y/N): ").upper()
            if choice2 in ["Y", "N"]:
                break
            else:
                self.slow_text("Invalid input. Please enter Y or N.", 0.03)
        self.stop_music()  # Stop difficulty select music before intro/game music
        if choice2 == "N":
            self.intro()
        else:
            # Start eerie music after skipping intro
            self.play_music(EERIE_MUSIC_PATH, loop=True)



    def found_bow(self):
        self.play_sound(ITEM_PICKUP_SOUND_PATH)
        self.slow_text("you've found a bow...", 0.05)

    def found_arrow(self):
        self.play_sound(ITEM_PICKUP_SOUND_PATH)
        self.slow_text("you've found an arrow...", 0.05)

    def intro(self):
        self.clear_screen()
        # Start eerie music at the beginning of the intro
        self.play_music(EERIE_MUSIC_PATH, loop=True)
        print(dungeon_art())
        self.slow_text("...\n", 0.5)
        self.slow_text("You wake up in a cold, dark dungeon.\n", 0.07)
        self.slow_text("Your head throbs... you can't remember how you got here.\n", 0.07)
        self.slow_text("You hear something lurking in the shadows.\n", 0.07)
        self.slow_text("You must do something before its too late...\n", 0.07)
        input("Press Enter to begin...")
        self.clear_screen()
    
    def guardian_spawn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) != (self.P1.row, self.P1.col): # Ensures guardian does not spawn on player as coords will keep changing until unique to player
                self.guard.row = row
                self.guard.col = col
                break

    def bow_spawn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) != (self.P1.row, self.P1.col): # Ensures bow does not spawn on player as coords will keep changing until unique to player
                self.bow.row = row
                self.bow.col = col
                break

    def arrow_spawn(self):
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if (row, col) != (self.P1.row, self.P1.col) and (row, col) != (self.bow.row, self.bow.col): # Ensures arrow does not spawn on player aswell as the bow as coords will keep changing until unique to player
                self.arrow.row = row
                self.arrow.col = col
                break

    def clear_screen(self):
        os.system('clear') # Made by AI for the purpose of user experience, does not effect backend, useful for clearing the terminal screen

    def start(self):
        self.audio_warning()
        self.difficulty_select()
        self.P1.grid_size = self.grid_size  # Adjust player grid size based on difficulty
        if self.nightmare_mode:
            self.P1.player_health = 50  # Double guardian damage in nightmare mode
        self.bow_spawn()
        self.arrow_spawn()
        self.guardian_spawn()
        # Eerie music already started in difficulty_select
        while True: #Main game loop
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
                self.cheat_mode, #If you comment out the rest of the parameters under this my original grid will work on Rooms.py, these are only for cheat mode made by Ai.
                bow_pos=(self.bow.row, self.bow.col),
                arrow_pos=(self.arrow.row, self.arrow.col),
                guardian_pos=(self.guard.row, self.guard.col),
                inventory=self.P1.inventory 
            ) #Initializes the grid with player, bow, arrow, and guardian positions, useful for cheatmode

            #Implemented by AI for the purpose of user experience, does not effect backend, simply displays a health bar 
            # Live health meter display

            if self.nightmare_mode:
                max_health = 50
            else:
                max_health = 100  

            health = self.P1.player_health
            bar_length = 20
            filled_length = int(bar_length * health // max_health)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            print(f"\nHealth: [{bar}] {health}/{max_health}")

            # Create a list of messages to display when the guardian is nearby    
            messages = ["You hear it...", "Footsteps approach...", "Something is nearby..."]
            distance = abs(self.P1.row - self.guard.row) + abs(self.P1.col - self.guard.col)
            # The point of abs (abosolute value) is to make sure the distance shows for all directions, not just up and down
            if distance == 1:
                print()
                self.slow_text(random.choice(messages), 0.04)

            print("Move(W/A/S/D), Use item(U), Help(H), Quit(Q): ", end='', flush=True)
            move = getch().upper()
            print(move)  

            if move in ["W", "A", "S", "D"]:
                # Move the player first
                if not self.P1.move_player(move):
                    self.slow_text("Invalid movement, try again.", 0.04)
                    time.sleep(1.5)
                    continue  # Skip the rest of the loop if invalid move

                # Now check for item pickups after moving
                # Check for bow pickup
                if (self.P1.row, self.P1.col) == (self.bow.row, self.bow.col):
                    if self.bow not in self.P1.inventory:
                        self.P1.inventory.append(self.bow)
                        self.found_bow()
                    self.bow.row = None
                    self.bow.col = None

                # Check for arrow pickup (only one arrow exists at a time)
                if (self.P1.row, self.P1.col) == (self.arrow.row, self.arrow.col):
                    if self.arrow not in self.P1.inventory:
                        self.P1.inventory.append(self.arrow)
                        self.found_arrow()
                    self.arrow.row = None
                    self.arrow.col = None

                # Move the guardian after player and item pickup
                self.guard.move_guardian(self.grid_size)

                # Check for guardian encounter after moving
                if (self.P1.row, self.P1.col) == (self.guard.row, self.guard.col):
                    self.guard_encounter()


            elif move == "U":
                if not self.P1.inventory:
                    self.slow_text("Your inventory is empty", 0.01)
                    self.slow_text("Press Enter to continue...", 0.01)
                    input()
                else:
                    result = self.P1.use_item(self.guard) #Passed through the guardian because if the player wants to use bow, it can alter the guardians data (i.e. damage it)
                    if result == True: #The point of using result is to check if arrow was used. if so a new one spawns
                        self.arrow_spawn()
                        self.slow_text("Press Enter to continue...", 0.01)
                        input()

            elif move == "H":
                self.slow_text("\n=== Dungeon Game Info ===", 0.01)
                self.slow_text("Objective: Escape the dungeon by defeating the Guardian.", 0.03)
                self.slow_text("You can move using W (up), A (left), S (down), D (right).", 0.03)
                self.slow_text("Pick up the Bow and Arrow to fight the Guardian.", 0.03)
                self.slow_text("You can attack the Guardian directly, but it's risky.", 0.03)
                self.slow_text("Hint: If you have a Bow and Arrow, you can shoot the Guardian from a neighboring room to instantly defeat it.", 0.03)
                self.slow_text("Use 'U' to use items from your inventory by typing out what you want to use", 0.03)
                self.slow_text("If you see 'You hear it...', 'Footsteps approach...', 'Something is nearby...' that means the guardian is in a neighboring room", 0.03)
                self.slow_text("Defeat the Guardian before it defeats you!", 0.03)
                self.slow_text("=========================", 0.03)
                self.slow_text("Press Enter to continue...", 0.01)
                input()

            elif move == "Q":
                self.slow_text("Quitting game. Goodbye!", 0.03)
                self.stop_music()
                break

            else:
                self.slow_text("Invalid input. Use W, A, S, D, U, H, or Q.", 0.01)
                self.slow_text("Press Enter to continue...", 0.01)
                input()

game = Game() #Initialises the game
if __name__ == "__main__": #Checks if the file name is main.py, if so it runs the game
    game.start()
import math
from locations import *
from user_interface import *
from items import *
from characters import *
from game_data import *
import time
from termcolor import colored
from ascii_art import clear_screen
import pygame

# 2. **game_engine.py**: Contains game engine logic, including state management, events, and state transitions.

# Function to select choice type. 
def select_choice_type():
    choice_type = random.choice(["good", "bad", "neutral"])
    return choice_type

# Function to check if the direction entered by the user leads to a valid exit. 
def is_valid_exit(exits, user_input):
    if user_input in exits:
        return True
    else:
        return False
    
# Calculate how much to increase XP by -> to be used in conjunction with the increase_xp method from the character class. 
def xp_increase_value(range_high = None):
    
    # If high end of XP increase range is None (default) then return arbitrary high.    
    if range_high == None:
        range_high = random.randint(10, 100)
        value = random.randint(math.ceil(range_high/4), range_high)
    
    elif range_high > 1:
        value = random.randint(math.ceil(range_high/4), range_high)
    
    return value

def execute_go(direction, current_exit, current_location):
    if direction in filler_locations:
        new_location = direction  # This is already a location name
        choice_type = select_choice_type()
        pathfinder.make_choice(choice_type)
        return new_location

    elif is_valid_exit(current_exit, direction):
        new_location = str(current_exit[direction])  # Convert the location to a string
        choice_type = select_choice_type()
        pathfinder.make_choice(choice_type)
        return new_location

    else:
        print(colored("You cannot go there.", color = 'red', attrs = ['bold']))
        return current_exit["name"]  # Return the name of the current location if it's an invalid exit

# Function to execute TAKE command.
def execute_take(item_name, current_location):
    found = False
    for index, item in enumerate(current_location['items']):
        if item.name == item_name:
            found = True
            if pathfinder.carrying_mass <= 20:
                pathfinder.add_item(item)
                pathfinder.carrying_mass += item.mass_kg
                del current_location['items'][index]
                print(f"{colored('You have picked up ' + item.name, color = 'green', attrs = ['bold'])}.")
            else: 
                print(f"{colored('You cannot carry more than 20kg, you are currently carrying ' + pathfinder.carrying_mass + 'kg. ' + 'Please drop some items to carry more.', color = 'green', attrs = ['bold'])}.")
            time.sleep(1)
            choice_type = select_choice_type()
            pathfinder.make_choice(choice_type)
            value = xp_increase_value(None)
            pathfinder.increase_xp(value)

    if found == False:
        print(colored("You cannot take that item", color = 'red', attrs = ['bold']) + '.')
        clear_screen()
    
# Function to execute DROP command.       
def execute_drop(item_name, current_location):
    found = False
    for index, item in enumerate(pathfinder.inventory):
        if item.name == item_name:
            found = True
            current_location['items'].append(item)
            del pathfinder.inventory[index]
            if pathfinder.carrying_mass <= 20 and pathfinder.carrying_mass > 0:
                pathfinder.carrying_mass -= item.mass_kg
                pathfinder.carrying_mass = max(0, pathfinder.carrying_mass)
            print(f"{colored('You have dropped ' + item.name, color = 'green', attrs = ['bold'])}.")
            time.sleep(1)
            choice_type = select_choice_type()
            pathfinder.make_choice(choice_type)
            value = xp_increase_value(None)
            pathfinder.increase_xp(value)

    if found == False:
        print(colored("You cannot drop that item", color = 'red', attrs = ['bold']) + '.')
        clear_screen()

# Function to execute USE command. 
def execute_use(item_name, target = None):
    found = False
    for index, item in enumerate(pathfinder.inventory):
        if item.name == item_name:
            found = True
            if target == None:
                if item.is_special:
                    item.use_special(pathfinder, pathfinder)
                    print(f"{colored('You have used ' + item.name, color = 'green', attrs = ['bold'])}.")
                    time.sleep(1)
                    choice_type = select_choice_type()
                    pathfinder.make_choice(choice_type)
                    value = xp_increase_value(None)
                    pathfinder.increase_xp(value)
                else:
                    item.use(pathfinder, pathfinder)
                    print(f"{colored('You have used ' + item.name, color = 'green', attrs = ['bold'])}.")
                    time.sleep(1)
                    choice_type = select_choice_type()
                    pathfinder.make_choice(choice_type)
                    value = xp_increase_value(None)
                    pathfinder.increase_xp(value)
            else:
                if item.is_special:
                    if target in [key for key in Enemies.keys()]:
                        item.use_special(Enemies[target], pathfinder)
                        pathfinder.attack(Enemies[target])
                        Enemies[target].attack(pathfinder)
                        print(f"{colored('You have used ' + item.name, color = 'green', attrs = ['bold'])}.")
                        time.sleep(2)
                        choice_type = select_choice_type()
                        pathfinder.make_choice(choice_type)
                        value = xp_increase_value(None)
                        pathfinder.increase_xp(value)
                else:
                    if target in [key for key in Enemies.keys()]:
                        item.use(Enemies[target], pathfinder)
                        pathfinder.attack(Enemies[target])
                        Enemies[target].attack(pathfinder)
                        print(f"{colored('You have used ' + item.name, color = 'green', attrs = ['bold'])}.")
                        time.sleep(2)
                        choice_type = select_choice_type()
                        pathfinder.make_choice(choice_type)
                        value = xp_increase_value(None)
                        pathfinder.increase_xp(value)
            
# Function to execute DISPLAY command.
def execute_display(command, command2 = None):
    pass

# Function to execute BUY command.
def execute_buy(command):
    pass

# Function to execute commands from the following: [GO, TAKE, DROP, USE, DISPLAY, BUY]
def execute_command(command, current_location):
    if len(command) == 0:
        return True

    """if command[0] == "go":
        if len(command) == 2:
            execute_go(command[1])
        else:
            print("GO where?")"""

    if command[0] == "take":
        if  len(command) == 3:
            execute_take(command[1], current_location)
            clear_screen()
        else:
            print("TAKE what?")

    elif command[0] == "drop":
        if len(command) == 3:
            execute_drop(command[1], current_location)
            clear_screen()
        else:
            print("DROP what?")

    elif command[0] == "use":
        if len(command) == 3:
            execute_use(command[1])
            clear_screen()
        elif len(command) == 5:
            execute_use(command[1], command[3])
            clear_screen()
        else:
            print("USE what?")

    elif command[0] == "display":
        if len(command) == 2:
            execute_display(command[1])
        if len(command) == 3:
            execute_command(command[1], command[2])
        else:
            print("USE what?")

    elif command[0] == "buy":
        if len(command) > 1 and len(command) <= 2:
            execute_display(command[1])
        elif len(command) in [3, 4]:
            execute_command(command[1], [2])
        else:
            print("BUY what?")
    
    elif command[0].lower() == "quit":
        return False
    
    else:
        if command[0] != "go":
            print("This does not make sense.")
    
    return True


# TODO
def move(location_exits, direction):
    return locations[location_exits[direction]]

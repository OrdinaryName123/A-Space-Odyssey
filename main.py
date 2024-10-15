from user_interface import *
from ascii_art import *
from termcolor import colored
from story import *
from locations import *
from characters import *
import threading
from game_engine import execute_command, execute_go

# **main.py**: The game's entry point, responsible for initialization, the game loop, and control flow. 

# Create a shared threading.Event to signal when input is received.
input_received = threading.Event()

# Function to get user input with a timeout.
def input_with_timeout(prompt, timeout, countdown_timer):

    user_input = [None]

    def get_input():
        user_input[0] = input(prompt)
        input_received.set()  # Set the event when input is received.
    
    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()

    countdown_thread = threading.Thread(target=countdown_timer)
    countdown_thread.daemon = True
    countdown_thread.start()
    
    input_thread.join(timeout)
    countdown_thread.join()
    
    return user_input[0]

def countdown_timer():
    start_time2 = time.time() + 5
    remaining_time = start_time2 - time.time()
    while remaining_time >= 0 and not input_received.is_set():
        clear_screen()
        print(colored(f"Press Enter to skip the introduction, {remaining_time:.1f} seconds left.", color="green", attrs=['bold']))
        time.sleep(1)  # Wait for 1 second.
        remaining_time -= 1

def main():
    current_location = locations["Azeroth"]

    start_time = time.time()
    game_state = False

    # Display the introduction and allow the user to skip with Enter key.
    while not game_state:
        if time.time() - start_time <= 4:
            pass
            #animator(filenames, delay=0.25, repeat=5)
        else:
            # Check for Enter key press to skip the introduction.
            user_input = input_with_timeout("", 5, countdown_timer)  # Allow 5 seconds to press Enter.
            if user_input == "":
                clear_screen()
                game_state = True
            else:
                # Continue with the introduction.
                introduction()
                start_time = time.time()

    while game_state:
        current_exits = current_location["exits"]
        if 'choices' in current_location:
            current_choices = current_location["choices"]
        else: 
            current_choices = None
        current_items = current_location["items"]
        display_location(current_location)
        user_command = menu(current_exits, current_choices, current_items, pathfinder.inventory, current_location)

        # Implementing execute_go in main.py to avoid circular import errors. 
        if user_command == "":
                continue
        elif user_command[0] == "go":
            start_time2 = time.time()
            journey_time = (2000/pathfinder.current_speed)
            if len(user_command) == 2:
                if user_command[1] not in filler_locations:
                    current_location = locations[execute_go(user_command[1], current_exits, current_location)]
                else:
                    current_location = current_location[execute_go(user_command[1], current_exits, current_location)]
            else:
                print("GO where?")
                # Calculate time spent in transition
            transition_time = time.time() - start_time2

            # Check if it's time to trigger the animation
            if transition_time <= journey_time:
                animator(filenames, delay=0.25, repeat=int(journey_time/1.5))
        
        # Main game iteration is contingent uoon user_command variable, if user_input == "quit", loop ends. 
        game_state = execute_command(user_command, current_location)



if __name__ == "__main__":
    main()
from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
opposite = {'w':'e', 'e':'w', 'n':'s', 's':'n'}

# "starting_room" and "checked" take input from 'else' statement below
def explore_map(starting_room, checked=[]):
    path = []
    # For each exit direction recieved for the current room by the "get_exits" function in room.py
    print("\n--FUNCTION START --\nPlayer started here at the start of function: Room ID ->", player.current_room.id, player.current_room)
    # For loop will explore every direction available to this room
    for direction in player.current_room.get_exits():
        # The player variable that was given will use the travel function within player.py
        print("Player moved ", direction)
        player.travel(direction)
        print("Player is now in room ", player.current_room.id)

        # If that new node/room is within the "checked" array
        if player.current_room.id in checked:
            # Then move in the opposite direction by referencing the dictionary key to get its value
            # print("opposite of north", opposite['n'])
            # print("opposite of west", opposite['w'])
            print("This room checked, traveling back ", opposite[direction])
            player.travel(opposite[direction])
            print("Player is now in room ", player.current_room.id)
        # Otherwise this is a new node/room
        else:
            print("This room has not been checked, so it will be explored now: Room ID added ->", player.current_room.id)
            # Add this current room ID to the "checked" array
            checked.append(player.current_room.id)
            # Add the current direction to the "path" array to track movements
            path.append(direction)
            # And now that path equals the existing path plus the function
            print("Path traveled to NEW rooms so far since function started", path)
            path = path + explore_map(player.current_room.id, checked)
            # print("2", path)
            # Now that the arrays have been updated -
            # Move the player to the opposite direction by referencing the dictionary key to get its value
            print("Player traveled", opposite[direction])
            player.travel(opposite[direction])
            # Add that opposite path to the path tracking array since we traveled that direction
            path.append(opposite[direction])
            print("PATH AFTER APPEND", path)
    return path

# Set traversal_path to equal the output of the explore function to map out the rooms
# taking in the current room as starting_room
traversal_path = explore_map(player.current_room.id)
# Print mapped rooms
print("Mapped path", traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

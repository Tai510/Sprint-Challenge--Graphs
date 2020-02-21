from room import Room
from player import Player
from world import World
from utils import Stack, Queue

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


opposites_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
# back to room with exit
previousRoom = [None]
#create a empty dictionary
visited = {}
path = []
direction = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
#add starting room to visited
visited[player.current_room.id] = player.current_room.get_exits()
#while visited list is less than the amount of rooms on the graph
while len(visited) < len(room_graph) - 1:
    #if not visited
    #add to visited and remove previous direction from potential paths to explore
    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()
        previous_direction = path[-1]
        visited[player.current_room.id].remove(previous_direction)
    #while all paths have been explored
    #backtrack to previous room until a room with optional paths is found
    while len(visited[player.current_room.id]) == 0: # (when all room's exits explored)
        previous_direction = path.pop()
        traversal_path.append(previous_direction)
        player.travel(previous_direction)
    #if there is an unexplored direction
    #add the direction to the traversalPath
    #explore the new room
    move = visited[player.current_room.id].pop(0)
    traversal_path.append(move)
    path.append(direction[move])
    player.travel(move)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

print('Enter your name:')
name = input()
print('Hello' ,name)

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
        print(name, 'has quit the game')
        break
    else:
        print("I did not understand that command.")

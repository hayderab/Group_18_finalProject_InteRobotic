#!/usr/bin/env python3

import copy
import helper

# Creates a dummy dictionary which will work as a policy
# This is for testing the movement of t robot based given policy
# Can be deleted later
def create_dummy_policy_dict(dummy_dict, x, y):
    # keep just the 2 digits of the floats (for easier comparison)
    x = float("{0:.1f}".format(x))
    y = float("{0:.1f}".format(y))
    # Set the following range of points (x,y) to go "right" or "up" etc.
    if (0.0 <= x < 6.0) and (0.0 <= y <= 2.0):
        dummy_dict[x, y] = "EAST"
    if (x >= 5.9) and (0.0 <= y <= 6.0):
        dummy_dict[x, y] = "NORTH"
    return dummy_dict


# Returns a dictionary with:
# coordinates, reward, value state (default: 0), policy direction with default (-1, -1), "terminal state?" and "SOUTH/EAST/NORTH/WEST?" (default: "DEFAULT")
def create_dict_grid(dict_grid, width_index, height_index, x, y, grid_cell):
    if grid_cell > 0:  # for obstacles
        dict_grid[width_index, height_index] = [x, y, -100.0, 0.0, (-1, -1), False, "DEFAULT"]  # reward = -1
    elif grid_cell == -1:  # for unknown cells
        dict_grid[width_index, height_index] = [x, y, -100.0, 0.0, (-1, -1), False,
                                                "DEFAULT"]  # reward = -1 (safer because it can be a wall too)
    else:  # for known cells
        if (8 <= x <= 10) and (9 <= y <= 11):  # for the target goal cell (I chose for now the centre of the maze)
            dict_grid[width_index, height_index] = [x, y, 10.0, 0.0, (-1, -1), True, "DEFAULT"]  # reward = 10
        else:
            dict_grid[width_index, height_index] = [x, y, 0.0, 0.0, (-1, -1), False, "DEFAULT"]  # reward = 0
    return dict_grid


def wall_thicc(maze_dict_copy, width, height, x, y):
    for y_buffer in range(y-5, y+6):
        for x_buffer in range(x-5, x+6):
            if not(x_buffer >= width) and not(x_buffer < 0) and not (y_buffer >= height) and not (y_buffer < 0):
                value = maze_dict_copy[(x_buffer, y_buffer)]
                value[2] = -100.0
                maze_dict_copy[(x,y)] = value
    return maze_dict_copy


# Returns and saves a dictionary of the maze occupancy grid with the coordinates (x, y) and reward of every cell
def maze_dict_grid(data):
    width_index = 0
    maze_dict = {}
    dummy_dict = {}  # can be deleted later
    while width_index < data.info.width:
        height_index = 0
        while height_index < data.info.height:
            # Reference: https://answers.ros.org/question/201172/get-xy-coordinates-of-an-obstacle-from-a-map/?answer=262245#post-id-262245
            grid_cell = data.data[height_index * data.info.width + width_index]
            # if grid_cell > 0:  # >0 is only for the obstacles
            x = width_index * data.info.resolution + data.info.resolution / 2  # coordinate x of the current grid cell
            y = height_index * data.info.resolution + data.info.resolution / 2  # coordinate y of the current grid cell
            maze_dict = create_dict_grid(maze_dict, width_index, height_index, x, y, grid_cell)
            dummy_dict = create_dummy_policy_dict(dummy_dict, x, y)  # can be deleted later
            height_index += 1
        width_index += 1
    # helper.save_to_text_file(dummy_dict, 'results.txt')

    maze_dict_copy = copy.deepcopy(maze_dict)
    #helper.save_to_text_file(maze_dict, "original_maze.txt")
    width = data.info.width
    height = data.info.height

    for y in range(0, height):
        for x in range(0, width):
            coord_values = maze_dict[(x,y)]
            if coord_values[2] == -100:
                #print("Wall hit")
                maze_dict_copy = wall_thicc(maze_dict_copy, width, height, x, y)

    #helper.save_to_text_file(maze_dict_copy, "new_maze.txt")
            


    return maze_dict_copy, data.info.width, data.info.height, dummy_dict  # dummy_dict can be deleted later

#!/usr/bin/env python3

import copy


# Add comments here
def wall_thicc(maze_dict_copy, width, height, x, y):
    for y_buffer in range(y - 4, y + 5, 2):
        for x_buffer in range(x - 4, x + 5, 2):
            if not (x_buffer >= width) and not (x_buffer < 0) and not (y_buffer >= height) and not (y_buffer < 0):
                value = maze_dict_copy[(x_buffer, y_buffer)]
                value[2] = -100.0
                maze_dict_copy[(x, y)] = value
    return maze_dict_copy


# Returns a dictionary with:
# [0] coordinates' indexes,
# [1] coordinates' values,
# [2] reward of the state,
# [3] value of the state (default value: 0)
# [4] policy direction (default indexes: (-1, -1))
# [5] "terminal state?" boolean flag (True/False)
# [6] "SOUTH/EAST/NORTH/WEST?" (default value: "DEFAULT")
def create_dict_grid(dict_grid, x_index, y_index, x, y, terminal_x, terminal_y, occ_grid_value, negative_reward,
                     positive_reward, default_reward):
    if occ_grid_value == 0:  # for known cells

        # keep just the first 2 digits of the floats (for easier comparison)
        formatted_x = int((float("{0:.1f}".format(x))))
        formatted_y = int((float("{0:.1f}".format(y))))

        if (formatted_x == terminal_x) and (formatted_y == terminal_y):  # for the target goal cell(s)
            dict_grid[x_index, y_index] = [x, y, positive_reward, 0.0, (-1, -1), True, "DEFAULT"]  # positive reward=10
        else:
            dict_grid[x_index, y_index] = [x, y, default_reward, 0.0, (-1, -1), False, "DEFAULT"]  # reward = 0

    else:  # for >0 (obstacles) and == -1 (unknown cells)
        dict_grid[x_index, y_index] = [x, y, negative_reward, 0.0, (-1, -1), False, "DEFAULT"]  # negative reward = -100
    return dict_grid


# Returns a dictionary of the maze occupancy grid (including extra info required for the policy iteration
def maze_dict_grid(data):
    maze_dict = {}
    width = data.info.width
    height = data.info.height

    for y_index in range(0, height, 2):
        for x_index in range(0, width, 2):
            # Reference: https://answers.ros.org/question/201172/get-xy-coordinates-of-an-obstacle-from-a-map/?answer=262245#post-id-262245
            occ_grid_value = data.data[y_index * data.info.width + x_index]

            x = x_index * data.info.resolution + data.info.resolution / 2  # coordinate x of the current grid cell
            y = y_index * data.info.resolution + data.info.resolution / 2  # coordinate y of the current grid cell

            # Modify the terminal position here
            # I chose as default the centre of the maze
            terminal_x = 9.0
            terminal_y = 9.0

            # Specify the rewards here
            negative_reward = -100.0
            positive_reward = 10.0
            default_reward = 0.0

            maze_dict = create_dict_grid(maze_dict, x_index, y_index, x, y, terminal_x, terminal_y, occ_grid_value,
                                         negative_reward, positive_reward, default_reward)

    # Add comments here
    maze_dict_copy = copy.deepcopy(maze_dict)
    for y_index in range(0, height, 2):
        for x_index in range(0, width, 2):
            coord_values = maze_dict[(x_index, y_index)]
            if coord_values[2] == -100:
                # print("Wall hit")
                maze_dict_copy = wall_thicc(maze_dict_copy, width, height, x_index, y_index)

    return maze_dict_copy, width, height

import os


# This created because terminal could not print all the results properly
# The file will be created/saved on your desktop
def save_to_text_file(givenDict, filename):
    home_dir = os.path.expanduser('~')
    desktop_dir = os.path.join(home_dir, 'Desktop')

    try:
        textfile = open(os.path.join(desktop_dir, filename), "w+")
        for coordinates, values in givenDict.items():
            textfile.write(
                "(x_index, y_index)" + "[" + "x, " + "y, " + "cell value, " + "reward value" + "]" + "\n")
            textfile.write(str(coordinates) + str(values) + "\n")
            textfile.write(" " + "\n")
        textfile.close()
        print("Done")

    except IOError as e:
        print(e)


# Returns a dictionary with coordinates, grade_cell value and reward
def create_dict_grid(dict_grid, width_index, height_index, x, y, grid_cell):
    if grid_cell > 0:  # for obstacles
        dict_grid[width_index, height_index] = [x, y, grid_cell, -1]  # reward = -1
    elif grid_cell == -1:  # for unknown cells
        dict_grid[width_index, height_index] = [x, y, grid_cell, 0]  # reward = 0
    else:  # for known cells
        if (8 <= x <= 10) and (9 <= y <= 11):  # for the target goal cell (I chose for now the centre of the maze)
            dict_grid[width_index, height_index] = [x, y, grid_cell, 10]  # reward = 10
        else:
            dict_grid[width_index, height_index] = [x, y, grid_cell, 0]  # reward = 0
    return dict_grid


# Returns and saves a dictionary of the maze occupancy grid with the coordinates (x, y) and reward of every cell
def cell_coordinates_reward(data):
    width_index = 0
    dict_grid = {}
    while width_index < data.info.width:
        height_index = 0
        while height_index < data.info.height:
            grid_cell = data.data[height_index * data.info.width + width_index]
            # if grid_cell > 0:  # only for the obstacles
            x = width_index * data.info.resolution + data.info.resolution / 2  # coordinate x of the current gird cell
            y = height_index * data.info.resolution + data.info.resolution / 2  # coordinate y of the current grid cell
            dict_grid = create_dict_grid(dict_grid, width_index, height_index, x, y, grid_cell)
            height_index += 1
        width_index += 1
    save_to_text_file(dict_grid, 'results.txt')

    return dict_grid

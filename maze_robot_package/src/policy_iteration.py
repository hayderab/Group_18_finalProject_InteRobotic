import copy

def policy_generate(dicts_grid, width_length, height_length, gamma):
    # Stores the dictionary with policy directions
    new_dicts_grid = {}
    # Loop through all coords
    for y in range(0, height_length):
        for x in range(0, width_length):

            # Reset at the start of each loop
            Qvalue = -100
            # Direction the policy is pointing for given coord
            p_direction = "SELF"

            # Check if coord is the goal state reference self in policy
            if dicts_grid[(x, y)][5]:
                value = dicts_grid[(x, y)]
                value[4] = (x, y)
                new_dicts_grid[(x, y)] = value

            # Generate a policy direction for the path
            else:
                # Check 4 surrounding coords for highest reward
                # Includes logic to prevent going off the grid
                east = 0
                south = 0
                west = 0
                north = 0

                # Calculate Qvalue for each surround square
                # Transition function is assumed to be 1, so it has been omitted for simplicity
                if not ((x + 1) >= width_length):
                    east = dicts_grid[(x + 1, y)][2] + gamma * dicts_grid[(x + 1, y)][3]

                if not ((y - 1) < 0):
                    south = dicts_grid[(x, y - 1)][2] + gamma * dicts_grid[(x, y - 1)][3]

                if not ((x - 1) < 0):
                    west = dicts_grid[(x - 1, y)][2] + gamma * dicts_grid[(x - 1, y)][3]

                if not ((y + 1) >= height_length):
                    north = dicts_grid[(x, y + 1)][2] + gamma * dicts_grid[(x, y + 1)][3]

                # Decide which neighbor has the largest value
                if not ((x + 1) >= width_length) and (east >= Qvalue):
                    Qvalue = east
                    p_direction = "EAST"

                if not ((y - 1) < 0) and (south >= Qvalue):
                    Qvalue = south
                    p_direction = "SOUTH"

                if not ((x - 1) < 0) and (west >= Qvalue):
                    Qvalue = west
                    p_direction = "WEST"

                if not ((y + 1) >= height_length) and (north >= Qvalue):
                    Qvalue = north
                    p_direction = "NORTH"

                # Obtain the value list for current coord to change and
                # insert into new dictionary
                dict_value = dicts_grid[(x, y)]

                # Insert the correct policy direction
                if p_direction == "SELF":
                    dict_value[4] = (x, y)
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "EAST":
                    dict_value[4] = (x + 1, y)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "SOUTH":
                    dict_value[4] = (x, y - 1)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "WEST":
                    dict_value[4] = (x - 1, y)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "NORTH":
                    dict_value[4] = (x, y + 1)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

    return new_dicts_grid


def policy_evaluation(dicts_grid, width_length, height_length, gamma):
    # Initialise variables needed
    new_dicts_grid = {}
    theta = 0.01
    delta = 1

    # Perform the value iteration until the changes are insignificant, hence converged
    while delta > theta:
        delta = 0
        # Loop through each coordinate
        for y in range(0, height_length):
            for x in range(0, width_length):

                # If it is in the terminal state, don't change the value
                if dicts_grid[(x, y)][5]:
                    new_dicts_grid[(x, y)] = dicts_grid[(x, y)]

                # update the value
                else:
                    coord_var = dicts_grid[(x, y)]
                    policy_var = dicts_grid[coord_var[4]]
                    old_value = coord_var[3]
                    # Transition function is assumed to be 1, so it has been omitted for simplicity
                    # Thus, the sum is also not required in the formula
                    new_value = policy_var[2] + gamma * policy_var[3]
                    difference = abs(old_value - new_value)
                    # Records the largest value change across the whole grid
                    delta = max(delta, difference)
                    coord_var[3] = new_value
                    new_dicts_grid[(x, y)] = coord_var

        # update the dictionary with the new values
        new_dicts_grid_copy = copy.deepcopy(new_dicts_grid)
        dicts_grid = new_dicts_grid_copy
    return dicts_grid


def policy_iteration(dicts_grid, width_length, height_length, gamma):
    # Generate the initial policy
    dicts_grid = policy_generate(dicts_grid, width_length, height_length, gamma)

    policy_stable = False

    while not policy_stable:
        dicts_grid_copy = copy.deepcopy(dicts_grid)
        new_dicts_grid = policy_evaluation(dicts_grid_copy, width_length, height_length, gamma)
        new_dicts_grid_copy = copy.deepcopy(new_dicts_grid)
        new_dicts_grid_evaluated = policy_generate(new_dicts_grid_copy, width_length, height_length, gamma)
        if dicts_grid_copy == new_dicts_grid_evaluated:
            policy_stable = True
        dicts_grid = new_dicts_grid_evaluated

    print("Optimal Policy Found!")
    return dicts_grid

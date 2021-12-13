import copy
import random

def policy_generate(dicts_grid, width_length, height_length, gamma):
    # Stores the dictionary with policy directions
    new_dicts_grid = {}
    # Loop through all coords
    for y in range(0, height_length, 2):
        for x in range(0, width_length, 2):

            # Reset at the start of each loop
            Qvalue = -1000000000
            # Direction the policy is pointing for given coord
            p_direction = "SELF"

            p_choices = []

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
                if not ((x + 2) >= width_length):
                    east = dicts_grid[(x + 2, y)][2] + gamma * dicts_grid[(x + 2, y)][3]

                if not ((y - 2) < 0):
                    south = dicts_grid[(x, y - 2)][2] + gamma * dicts_grid[(x, y - 2)][3]

                if not ((x - 2) < 0):
                    west = dicts_grid[(x - 2, y)][2] + gamma * dicts_grid[(x - 2, y)][3]

                if not ((y + 2) >= height_length):
                    north = dicts_grid[(x, y + 2)][2] + gamma * dicts_grid[(x, y + 2)][3]

                # Decide which neighbor has the largest value
                if not ((x + 2) >= width_length) and (east > Qvalue):
                    Qvalue = east
                    p_choices.append("EAST")
                elif not ((x + 2) >= width_length) and (east == Qvalue):
                    p_choices.append("EAST")

                if not ((y - 2) < 0) and (south > Qvalue):
                    Qvalue = south
                    p_choices = []
                    p_choices.append("SOUTH")
                elif not ((y - 2) < 0) and (south == Qvalue):
                    p_choices.append("SOUTH")

                if not ((x - 2) < 0) and (west > Qvalue):
                    Qvalue = west
                    p_choices = []
                    p_choices.append("WEST")
                elif not ((x - 2) < 0) and (west == Qvalue):
                    p_choices.append("WEST")

                if not ((y + 2) >= height_length) and (north > Qvalue):
                    Qvalue = north
                    p_choices = []
                    p_choices.append("NORTH")
                elif not ((y + 2) >= height_length) and (north == Qvalue):
                    p_choices.append("NORTH")

                # Decide which direction to choose
                # If there is a tie, select at random
                p_direction = random.choice(p_choices)

                # Obtain the value list for current coord to change and
                # insert into new dictionary
                dict_value = dicts_grid[(x, y)]

                # Insert the correct policy direction
                if p_direction == "SELF":
                    dict_value[4] = (x, y)
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "EAST":
                    dict_value[4] = (x + 2, y)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "SOUTH":
                    dict_value[4] = (x, y - 2)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "WEST":
                    dict_value[4] = (x - 2, y)
                    dict_value[6] = p_direction
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "NORTH":
                    dict_value[4] = (x, y + 2)
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
        for y in range(0, height_length, 2):
            for x in range(0, width_length, 2):

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
    iteration_count = 0

    while not policy_stable and (iteration_count < 2000):
        print("Iteration Number: " + str(iteration_count))
        dicts_grid_copy = copy.deepcopy(dicts_grid)
        new_dicts_grid = policy_evaluation(dicts_grid_copy, width_length, height_length, gamma)
        new_dicts_grid_copy = copy.deepcopy(new_dicts_grid)
        new_dicts_grid_evaluated = policy_generate(new_dicts_grid_copy, width_length, height_length, gamma)
        if dicts_grid_copy == new_dicts_grid_evaluated:
            policy_stable = True
        dicts_grid = new_dicts_grid_evaluated
        iteration_count += 1

    print("Optimal Policy Found!")
    return dicts_grid
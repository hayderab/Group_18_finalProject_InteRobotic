import copy
import random


def policy_generate(maze_dict, width_length, height_length, gamma):
    # Initialise the dictionary with the policy's directions
    policy_generate_dict = {}

    # Loop through all coords
    for y_index in range(0, height_length, 2):
        for x_index in range(0, width_length, 2):

            # Initialize a max variable for storing the best q-value
            q_best = -1000000000

            # a list which will store the available choices for the robot to move (for each state/loop)
            p_choices = []

            # Take the value of the "terminal flag" (boolean flag)
            # coming from the current "key:value" pair of the "maze_dict"
            # which has the current coordinate indexes (x_index, y_index) as a key
            terminal_state_flag = maze_dict[(x_index, y_index)][5]  # returns True or False

            # If the above terminal flag is True (represents the terminal state)
            if terminal_state_flag:
                # maze_dict -> [<key> : <value>]
                # store the <value> which is a list of values, where <key> = (x_index, y_index)
                list_of_maze_dict_values = maze_dict[(x_index, y_index)]
                # update the policy direction coordinates (which is a tuple and value/element of that list)
                list_of_maze_dict_values[4] = (x_index, y_index)
                # append the current values of the list to our policy dictionary
                policy_generate_dict[(x_index, y_index)] = list_of_maze_dict_values

            # Generate a policy direction for the path
            else:
                # Check 4 surrounding coords for highest value
                east_state_value = 0
                south_state_value = 0
                west_state_value = 0
                north_state_value = 0

                # Calculate the state value for each surround state
                # Transition function is assumed to be 1, so it has been omitted for simplicity
                if not ((x_index + 2) >= width_length):
                    east_reward = maze_dict[(x_index + 2, y_index)][2]  # r
                    next_east_state_value = maze_dict[(x_index + 2, y_index)][3]  # V(s')
                    east_state_value = east_reward + gamma * next_east_state_value  # V(s) = r + gamma * V(s')

                if not ((y_index - 2) < 0):
                    south_reward = maze_dict[(x_index, y_index - 2)][2]
                    next_south_state_value = maze_dict[(x_index, y_index - 2)][3]
                    south_state_value = south_reward + gamma * next_south_state_value

                if not ((x_index - 2) < 0):
                    west_reward = maze_dict[(x_index - 2, y_index)][2]
                    next_west_state_value = maze_dict[(x_index - 2, y_index)][3]
                    west_state_value = west_reward + gamma * next_west_state_value

                if not ((y_index + 2) >= height_length):
                    north_reward = maze_dict[(x_index, y_index + 2)][2]
                    next_north_state_value = maze_dict[(x_index, y_index + 2)][3]
                    north_state_value = north_reward + gamma * next_north_state_value

                # Decide which neighbor has the largest value
                if not ((x_index + 2) >= width_length) and (east_state_value > q_best):
                    q_best = east_state_value
                    p_choices.append("EAST")
                elif not ((x_index + 2) >= width_length) and (east_state_value == q_best):
                    p_choices.append("EAST")

                if not ((y_index - 2) < 0) and (south_state_value > q_best):
                    q_best = south_state_value
                    p_choices = ["SOUTH"]
                elif not ((y_index - 2) < 0) and (south_state_value == q_best):
                    p_choices.append("SOUTH")

                if not ((x_index - 2) < 0) and (west_state_value > q_best):
                    q_best = west_state_value
                    p_choices = ["WEST"]
                elif not ((x_index - 2) < 0) and (west_state_value == q_best):
                    p_choices.append("WEST")

                if not ((y_index + 2) >= height_length) and (north_state_value > q_best):
                    q_best = north_state_value
                    p_choices = ["NORTH"]
                elif not ((y_index + 2) >= height_length) and (north_state_value == q_best):
                    p_choices.append("NORTH")

                # Initialise the policy direction (string) - Policy decides where the robot should move
                # If there is a tie, select at random
                p_direction = random.choice(p_choices)

                # maze_dict -> [<key> : <value>]
                # store the <value> which is a list of values, where <key> = (x_index, y_index)
                list_of_maze_dict_values = maze_dict[(x_index, y_index)]

                # Insert the correct policy direction
                if p_direction == "EAST":
                    list_of_maze_dict_values[4] = (x_index + 2, y_index)  # update policy direction (tuple)
                    list_of_maze_dict_values[6] = p_direction  # update policy direction (string)
                    policy_generate_dict[(x_index, y_index)] = list_of_maze_dict_values

                elif p_direction == "SOUTH":
                    list_of_maze_dict_values[4] = (x_index, y_index - 2)
                    list_of_maze_dict_values[6] = p_direction
                    policy_generate_dict[(x_index, y_index)] = list_of_maze_dict_values

                elif p_direction == "WEST":
                    list_of_maze_dict_values[4] = (x_index - 2, y_index)
                    list_of_maze_dict_values[6] = p_direction
                    policy_generate_dict[(x_index, y_index)] = list_of_maze_dict_values

                elif p_direction == "NORTH":
                    list_of_maze_dict_values[4] = (x_index, y_index + 2)
                    list_of_maze_dict_values[6] = p_direction
                    policy_generate_dict[(x_index, y_index)] = list_of_maze_dict_values

    return policy_generate_dict


def policy_evaluation(policy_dict, width_length, height_length, gamma):
    # Initialise variables needed
    policy_evaluation_dict = {}
    theta = 0.01
    delta = 1  # to get inside in the first while loop

    # Perform the value iteration until the changes are insignificant, hence converged
    while delta > theta:
        delta = 0
        # Loop through each coordinate
        for y_index in range(0, height_length, 2):
            for x_index in range(0, width_length, 2):

                # If it is in the terminal state, don't change the value
                terminal_state_flag = policy_dict[(x_index, y_index)][5]
                if terminal_state_flag:
                    policy_evaluation_dict[(x_index, y_index)] = policy_dict[(x_index, y_index)]

                # Update the value
                else:
                    # a list with values of the "policy_dict" which has the current state coordinate indexes as key
                    state_coordinates_list = policy_dict[(x_index, y_index)]

                    # a list with values of the "policy_dict" that has the policy direction coordinate indexes as key
                    policy_coordinate_list = policy_dict[state_coordinates_list[4]]

                    old_value = state_coordinates_list[3]  # u = V(s)

                    # Transition function is assumed to be 1, so it has been omitted for simplicity
                    # Thus, the sum is also not required in the formula
                    reward = policy_coordinate_list[2]  # r
                    next_state_value = policy_coordinate_list[3]  # V(s')
                    new_value = reward + gamma * next_state_value  # V(s) = r + gamma * V(s')

                    difference = abs(old_value - new_value)  # |u - V(s)|

                    # Records the largest value change across the whole grid
                    delta = max(delta, difference)  # max(Delta, |u - V(s)|)

                    state_coordinates_list[3] = new_value  # update the state with a new value
                    policy_evaluation_dict[(x_index, y_index)] = state_coordinates_list

        # Update the policy dictionary with the new values
        new_dicts_grid_copy = copy.deepcopy(policy_evaluation_dict)
        policy_dict = new_dicts_grid_copy

    return policy_dict


def policy_iteration(maze_dict, width_length, height_length, gamma):
    print("Running Policy Iteration...")

    # Generate the initial policy
    policy_dict = policy_generate(maze_dict, width_length, height_length, gamma)

    policy_stable = False
    iteration_count = 0

    while not policy_stable and (iteration_count < 2000):
        print("Iteration Number: " + str(iteration_count))

        # Create a copy of the above "policy_dict" and run the policy evaluation
        policy_dict_copy = copy.deepcopy(policy_dict)
        policy_evaluation_dict = policy_evaluation(policy_dict_copy, width_length, height_length, gamma)

        # Create a copy of the "policy_evaluation_dict" and generate a new policy based on that copy
        policy_evaluation_dict_copy = copy.deepcopy(policy_evaluation_dict)
        new_policy_dict = policy_generate(policy_evaluation_dict_copy, width_length, height_length, gamma)

        # If the previous policy (the copy) is identical with the new policy, policy iteration ends (hence converge)
        if policy_dict_copy == new_policy_dict:
            policy_stable = True

        policy_dict = new_policy_dict
        iteration_count += 1

    print("Optimal Policy Found!")
    return policy_dict

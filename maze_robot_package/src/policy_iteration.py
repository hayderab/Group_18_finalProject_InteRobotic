def policy_generate(dicts_grid, width_length, height_length, gamma, trans):
    # Stores the dictionary with policy directions
    new_dicts_grid = {}

    # Loop through all coords
    for y in range(0, height_length):
        for x in range(0, width_length):
            
            # Reset at the start of each loop
            Qvalue = 0
            # Direction the policy is pointing for given coord
            p_direction = "self"

            # Check if coord is the goal state reference self in policy
            if dicts_grid[(x, y)][5]:
                value = dicts_grid[(x, y)]
                value[4] = (x, y)
                new_dicts_grid[(x, y)] = value

            # Generate a policy direction for the path
            else:
                # Check 4 surrounding coords for highest reward
                # Includes logic to prevent going off the grid
                left = 0
                down = 0
                right = 0
                up = 0

                # Calculate Qvalue for each surround square
                if not ((x + 1) >= width_length):
                    print(dicts_grid[(x + 1, y)][3])
                    a = gamma*dicts_grid[(x + 1, y)][3]
                    b = dicts_grid[(x + 1, y)][2] + a
                    left = trans * b
                if not ((y - 1) < 0):
                    print(dicts_grid[(x, y - 1)][3])
                    a = gamma*dicts_grid[(x, y - 1)][3]
                    b = dicts_grid[(x, y - 1)][2] + a
                    down = trans * b

                if not ((x - 1) < 0):

                    print(list(dicts_grid[(x - 1, y)])[3])
                    print(dicts_grid[(0,0)])
                    a = gamma*dicts_grid[(x - 1, y)][3]
                    b = dicts_grid[(x - 1, y)][2] + a
                    right = trans * b
                if not ((y + 1) >= height_length):
                    a = gamma*dicts_grid[(x, y + 1)][3]
                    b = dicts_grid[(x, y + 1)][2] + a
                    up = trans * b


                if not ((x + 1) >= width_length) and (left > Qvalue):
                    Qvalue = left
                    p_direction = "left"

                if not ((y - 1) < 0) and (down > Qvalue):
                    Qvalue = down
                    p_direction = "down"

                if not ((x - 1) < 0) and (right > Qvalue):
                    Qvalue = right
                    p_direction = "right"

                if not ((y + 1) >= height_length) and (up > Qvalue):
                    Qvalue = up
                    p_direction = "up"

                # Obtain the value list for current coord to change and
                # insert into new dictionary
                dict_value = dicts_grid[(x, y)]

                # Insert the correct policy direction
                if p_direction == "self":
                    dict_value[4] = (x, y)
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "left":
                    dict_value[4] = (x + 1, y)
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "down":
                    dict_value[4] = (x, y - 1)
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "right":
                    dict_value[4] = (x - 1, y)
                    new_dicts_grid[(x, y)] = dict_value

                elif p_direction == "up":
                    dict_value[4] = (x, y + 1)
                    new_dicts_grid[(x, y)] = dict_value

    return new_dicts_grid

def reward_propagation(dicts_grid, width_length, height_length):
    # Stores the dictionary with new rewards
    new_dicts_grid = {}

    # Loop through all coords
    for y in range(0, height_length):
        for x in range(0, width_length):

            if dicts_grid[(x, y)][4]:
                new_dicts_grid[(x,y)] = dicts_grid[(x,y)]

            else:
                value = dicts_grid[(x,y)]
                current_reward = value[2]
                p_coords = value[3]
                p_reward = dicts_grid[p_coords][2]

                new_reward = current_reward + p_reward
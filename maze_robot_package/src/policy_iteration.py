def policy_generate(dicts_grid, width_length, height_length):
    # Stores the dictionary with policy directions
    new_dicts_grid = {}

    # Loop through all coords
    for y in range(0, height_length):
        for x in range(0, width_length):

            # Reset at the start of each loop
            reward = -10000000
            # Direction the policy is pointing for given coord
            p_direction = "self"

            # Check if coord is a wall/goal based if the cell's value is fixed (True/False of the dictionary)
            if dicts_grid[(x, y)][4]:
                value = dicts_grid[(x, y)]
                value[3] = (x, y)
                new_dicts_grid[(x, y)] = value

            # Generate a policy direction for the path
            else:
                # Check 4 surrounding coords for highest reward
                # Includes logic to prevent going off the grid
                if not ((x + 1) >= width_length) and (dicts_grid[(x + 1, y)][2] > reward):
                    reward = dicts_grid[(x + 1, y)][2]
                    p_direction = "left"

                if not ((y - 1) < 0) and (dicts_grid[(x, y - 1)][2] > reward):
                    reward = dicts_grid[(x, y - 1)][2]
                    p_direction = "down"

                if not ((x - 1) < 0) and (dicts_grid[(x - 1, y)][2] > reward):
                    reward = dicts_grid[(x - 1, y)][2]
                    p_direction = "right"

                if not ((y + 1) >= height_length) and (dicts_grid[(x, y + 1)][2] > reward):
                    reward = dicts_grid[(x, y + 1)][2]
                    p_direction = "up"

                # Obtain the value list for current coord to change and
                # insert into new dictionary
                value = dicts_grid[(x, y)]

                # Insert the correct policy direction
                if p_direction == "self":
                    value[3] = (x, y)
                    new_dicts_grid[(x, y)] = value

                elif p_direction == "left":
                    value[3] = (x + 1, y)
                    new_dicts_grid[(x, y)] = value

                elif p_direction == "down":
                    value[3] = (x, y - 1)
                    new_dicts_grid[(x, y)] = value

                elif p_direction == "right":
                    value[3] = (x - 1, y)
                    new_dicts_grid[(x, y)] = value

                elif p_direction == "up":
                    value[3] = (x, y + 1)
                    new_dicts_grid[(x, y)] = value

    return new_dicts_grid

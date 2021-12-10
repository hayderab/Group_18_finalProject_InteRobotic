import os
# Importing math package for square roots, sinus and other calculations
import math


# This created because terminal could not print the dictionary properly
# The file will be created/saved on your desktop
def save_to_text_file(givenDict, filename):
    home_dir = os.path.expanduser('~')
    desktop_dir = os.path.join(home_dir, 'Desktop')

    try:
        textfile = open(os.path.join(desktop_dir, filename), "w+")
        for coordinates, values in givenDict.items():
            textfile.write(
                "(x_index, y_index)" + " : " + "[" + "x-coord, " + "y-coord, " + "reward, " + "value state, " + "policy direction, " + "terminal state?, " + "S/E/N/W?" + "]" + "\n")
            textfile.write(str(coordinates) + " : " + str(values) + "\n")
            textfile.write(" " + "\n")
        textfile.close()
        print("Done! - the .txt file has been saved to your desktop")

    except IOError as e:
        print(e)


# Finds the robot's current heading direction
def find_direction(current_direction, current_yaw):
    # keep just the first 3 digits of the float (for easier comparison)
    formatted_current_yaw = float("{0:.2f}".format(current_yaw))

    if formatted_current_yaw == 0:  # 90° - clockwise
        current_direction = "EAST"
    elif formatted_current_yaw == float("{0:.2f}".format(3 * math.pi / 2)):  # 180° - clockwise
        current_direction = "SOUTH"
    elif formatted_current_yaw == float("{0:.2f}".format(math.pi)):  # 270° - clockwise
        current_direction = "WEST"
    elif formatted_current_yaw == float("{0:.2f}".format(math.pi / 2)):  # 360° - clockwise
        current_direction = "NORTH"

    return current_direction


# Calculates the radians that the robot needs to rotate before move forwards/backwards
def calculate_rotation(target_direction, current_direction):
    # As soon as each rotation will be ±90° or ±180° for EAST/NORTH/SOUTH/WEST
    # Reference: https://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/

    rotate_target_degrees = 0

    # Clockwise
    if target_direction == "EAST":
        if current_direction == "NORTH":
            rotate_target_degrees = -90  # how many degrees the robot will rotate
        elif current_direction == "SOUTH":
            rotate_target_degrees = 90
        elif current_direction == "WEST":
            rotate_target_degrees = 180
    elif target_direction == "NORTH":
        if current_direction == "WEST":
            rotate_target_degrees = -90
        elif current_direction == "EAST":
            rotate_target_degrees = 90
        elif current_direction == "SOUTH":
            rotate_target_degrees = 180
    elif target_direction == "SOUTH":
        if current_direction == "WEST":
            rotate_target_degrees = 90
        elif current_direction == "EAST":
            rotate_target_degrees = -90
        elif current_direction == "NORTH":
            rotate_target_degrees = 180
    elif target_direction == "WEST":
        if current_direction == "NORTH":
            rotate_target_degrees = 90
        elif current_direction == "SOUTH":
            rotate_target_degrees = -90
        elif current_direction == "EAST":
            rotate_target_degrees = -180

    rotate_target_rad = rotate_target_degrees * math.pi / 180  # convert degrees to radians because yaw angle is in radians
    return rotate_target_rad

def test_policy(final_dict):
    start_coord = (20,20)
    values = final_dict[start_coord]
    terminal = values[5]
    while not terminal:
        print(values[6])
        values = final_dict[values[4]]
        terminal = values[5]
    print("DONE!")

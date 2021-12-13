import os
import math  # Importing math package for square roots, sinus and other calculations
import pickle
import time


# This function was created because terminal could not print the dictionary properly
# The file will be saved on your desktop
def save_to_text_file(givenDict, filename):
    home_dir = os.path.expanduser('~')
    desktop_dir = os.path.join(home_dir, 'Desktop')

    try:
        print("Saving the given dictionary to a .txt file...")
        time.sleep(1)  # Show the message for 2 secs

        textfile = open(os.path.join(desktop_dir, filename), "w+")
        for coordinates, values in givenDict.items():
            textfile.write(
                "(x_index, y_index)" + " : " + "[" + "x-coord, " + "y-coord, " + "reward, " + "value state, " + "policy direction, " + "terminal state?, " + "S/E/N/W?" + "]" + "\n")
            textfile.write(str(coordinates) + " : " + str(values) + "\n")
            textfile.write(" " + "\n")
        textfile.close()

        print("Done! - The file" + " '" + str(filename) + "' " + "has been successfully saved to your desktop")
        time.sleep(1)  # Show the message for 2 secs

    except IOError as e:
        print(e)


# This function will find the folder to save/load the pickle files
# Reference: https://stackoverflow.com/a/20826644
def pickles_folder_path():
    # Finding absolute path of the current module
    drive, module_dir = os.path.splitdrive(os.path.abspath(__file__))

    # It's good if we always traverse from the project root directory
    # rather than the relative path
    # So finding the Project's root directory
    paths = module_dir.split(os.sep)[:-2]
    base_dir = os.path.join(drive, os.sep, *paths)
    pickles_dir = base_dir + "/data/pickles"

    return pickles_dir


# Create a pickle in order to do not have to run the policy everytime
# The file will be saved on the project folder
def create_dict_pickle(dict_data, pickle_filename):
    try:
        print("Save the given dictionary to a pickle file...")
        time.sleep(1)  # Show the message for 1 sec

        pickle_folder_dir = pickles_folder_path()
        if not os.path.exists(pickle_folder_dir):
            os.makedirs(pickle_folder_dir)

        pickle_file = open(os.path.join(pickle_folder_dir, pickle_filename), "wb")
        pickle.dump(dict_data, pickle_file)

        pickle_file.close()
        print("Done! - " + "The file" + " '" + str(pickle_filename) + "' " + "has been successfully saved to the project's data folder")
        time.sleep(1)  # Show the message for 1 sec

    except IOError as e:
        print(e)


# Load the requested pickle file
def load_dict_pickle(pickle_filename):
    try:
        pickle_folder_dir = pickles_folder_path()
        if os.path.exists(pickle_folder_dir):
            print("Loading the pickle file...")
            time.sleep(1)  # Show the message for 1 sec

            pickle_file = open(os.path.join(pickle_folder_dir, pickle_filename), "rb")
            pickle_dict = pickle.load(pickle_file)
            pickle_file.close()

            print("Done! - " + "The file" + " '" + str(pickle_filename) + "' " + "was loaded successfully!")
            time.sleep(1)  # Show the message for 1 sec
            return pickle_dict
        else:
            print("Pickle not found!")

    except IOError as e:
        print(e)


# Returns/Finds the robot's current heading direction
def find_direction(current_direction, current_yaw):
    # Keep just the first 3 digits of the float (for easier comparison)
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


# Returns/Calculates the radians that the robot needs to rotate before move to the next state
def calculate_rotation(target_direction, current_direction):
    rotate_target_degrees = 0  # initialise the degrees which we want to robot to rotate

    # Clockwise - As soon as each rotation will be ±90° or ±180° for EAST/NORTH/SOUTH/WEST
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


# Print the path given by the policy to check (manually) if it is the shortest
def test_policy(policy_dict, start_coord_indexes):
    print("The testing policy process has started...")
    time.sleep(1)  # Show the message for 1 sec

    values = policy_dict[start_coord_indexes]  # list with the dict values that have the start point coordinates as key
    terminal = values[5]  # True/False

    while not terminal:  # until to reach the terminal state
        print(values[6])  # print the policy direction/next move (N/S/E/W) for the current state
        values = policy_dict[
            values[4]]  # update list with the dictionary values that have the policy direction coordinates as key
        terminal = values[5]  # take the new terminal flag from the updated list

    print("Done! - the testing policy process has finished")
    time.sleep(1)  # Show the message for 1 sec

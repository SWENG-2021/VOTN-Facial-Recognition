
import os
from os import path
import sys
import face_recognition
import cv2
import new_recognition
from tabulate import tabulate


# To use: python  test_faces.py  Aki-Bundee
# Or alternatively any other player that has a folder in both the known_faces and unknown_faces folder
# The program will show which template pictures succeed and dont succeed in getting a match with an unknown image


def main():
    try:
        player = sys.argv[1]

        if (player == None):
            print("--- Testing on entire known_faces folder not implemented yet ---")
        else:
            test_face(player)

    except IndexError as error:
        print("Incorrect amount of command arguments provided. py test_faces.py player_name ")



def test_face(player):
    #player = "Aki-Bundee"

    known_faces = []
    known_names = []
    found_player = False

    the_country = None
    the_player_name = None

    # First check that this player is in the known_players folder
    for country in os.listdir(f"known_faces"):

        # Now go through every player folder and see if the folders match
        for player_name in os.listdir(f"known_faces/{country}"):

            if player_name == player:
                found_player = True
                the_country = country
                the_player_name = player_name

                for photo in os.listdir(f"known_faces/{country}/{player_name}"):
                    print("Loading in and creating encoding for: ",photo)

                    # Here is where we do some image processing
                    image = face_recognition.load_image_file(f"known_faces/{country}/{player}/{photo}")
                    encoding = face_recognition.face_encodings(image)[0]
                    known_faces.append(encoding)
                    known_names.append(photo)

                break

            else:
                pass



    # Make sure we have found the player we are going to be testing on
    if not found_player:
        print("Player could not be found in the known_faces folder, make sure their name is spelt correctly")

    else:
        # Check to make sure this player has a folder of images we can test on
        if (path.exists(f"unknown_faces/{the_country}/{the_player_name}")):

            # Take in all the test scenario photos for bundee
            for test_photo in os.listdir(f"unknown_faces/{the_country}/{the_player_name}"):
                print("Testing against: ",test_photo)

                image = face_recognition.load_image_file(f"unknown_faces/{the_country}/{the_player_name}/{test_photo}")
                match = new_recognition.detectFacesInImage(image, known_faces, known_names, debug_mode=False)
                no_match = [x for x in known_names if x not in match]

                print("known_faces success: ",match)
                print("known_faces failure: ",no_match)
                print("-------------------------------\n")

        else:
            print("--- The testing directory of photos for {} has not been created yet---".format(the_player_name))




main()

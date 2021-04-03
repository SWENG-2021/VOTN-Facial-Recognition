
""" New code using the face-recognition library for python """

import face_recognition
import cv2
import os
import datetime
import traceback



""" Some Constants for the project """

KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = 0.55            # Lower value for more accuracy
FRAME_THICKNESS = 3        # The number of pixels of the frame will be around detected face
FONT_THICKNESS = 2
MODEL = 'hog'              # Set to cnn if you want to use GPU setup, hog for CPU setup



'''
Function to load in all the faces for different countries
'''
def loadAllFaces():
    print("Attempting to load all faces")
    known_faces = []
    known_names = []

    # Go through every country in the known_faces directory
    for country in os.listdir(KNOWN_FACES_DIR):
        print(country)

        # Go through every player for every country
        for player in os.listdir(f"{KNOWN_FACES_DIR}/{country}"):
            print("\t",player)

            # Go through every photo for this player
            for filename in os.listdir(f"{KNOWN_FACES_DIR}/{country}/{player}"):
                print("\t\t",filename)

                # Here is where we do some image processing
                image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{country}/{player}/{filename}")
                encoding = face_recognition.face_encodings(image)[0]
                known_faces.append(encoding)
                known_names.append(player)

    return known_faces, known_names



'''
Function to detect all faces in an image from a file location
'''
def detectFacesInImageFile(imageLocation, known_faces, known_names):
    # So we get the image that we want want to analyse
    image = face_recognition.load_image_file(imageLocation)

    # Next find all the locations which contain faces
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)

    # Next we want to be able to draw boxes around the faces on the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Now check what indexes we got a detection at to figure out the name for the face
    match = []

    # Now iterate over the encodings and locations
    for face_encoding, face_location in zip(encodings, locations):

        # We want to see if there are any matches that we can find
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        print(results)

        drawn_face = False

        # Check each player loaded into the player database
        for i in range(0, len(results)):
            if results[i] == True:
                print("We found a match: ",known_names[i])
                match.append(known_names[i])

                # To draw a box around a face we need top left coordinate and bottom right coordinate
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])
                cv2.rectangle(image, top_left, bottom_right, (255,0,0), FRAME_THICKNESS)

                # Next draw a little box to have the name of the person
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2]+22)
                cv2.rectangle(image, top_left, bottom_right, (255,0,0), cv2.FILLED)
                cv2.putText(image, known_names[i], (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)

                drawn_face = True

        if (not drawn_face):
            # To draw a box around a face we need top left coordinate and bottom right coordinate
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            cv2.rectangle(image, top_left, bottom_right, (0,0,255), FRAME_THICKNESS)

            # Next draw a little box to have the name of the person
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255), cv2.FILLED)
            cv2.putText(image, "Unknown", (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)



    cv2.imshow("Output",image)
    cv2.waitKey(0)
    cv2.destroyWindow("Output")

    return match



'''
Function to detect all faces in an image from an image object, returns all the matches made
'''
def detectFacesInImage(imageObject, known_faces, known_names, debug_mode):
    image = imageObject

    # Find all the locations in the image which contain faces
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)

    # Next we want to be able to draw boxes around the faces on the image
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Now iterate over the encodings and locations
    match = []

    # For each face on the screen
    for face_encoding, face_location in zip(encodings, locations):

        # We want to see if there are any matches that we can find
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        #print(results)

        draw_face = False

        # Now check what indexes we got a detection at to figure out the name for the face
        for i in range(0, len(results)):
            if results[i] == True:
                match.append(known_names[i])

                if (debug_mode):
                    print("We found a match: ",known_names[i])

                    # To draw a box around a face we need top left coordinate and bottom right coordinate
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    cv2.rectangle(image, top_left, bottom_right, (255,0,0), FRAME_THICKNESS)

                    # Next draw a little box to have the name of the person
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2]+22)
                    cv2.rectangle(image, top_left, bottom_right, (255,0,0), cv2.FILLED)
                    cv2.putText(image, known_names[i], (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)

                    draw_face = True


        if (not draw_face and debug_mode):
            # To draw a box around a face we need top left coordinate and bottom right coordinate
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            cv2.rectangle(image, top_left, bottom_right, (0,0,255), FRAME_THICKNESS)

            # Next draw a little box to have the name of the person
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)
            cv2.rectangle(image, top_left, bottom_right, (0,0,255), cv2.FILLED)
            cv2.putText(image, "Unknown", (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)


    if (debug_mode):
        cv2.imshow("Output",image)
        cv2.waitKey(0)
        cv2.destroyWindow("Output")

    return match



'''
Function to detect all faces in a video
'''
def detectVideoFaces(videoLocation, known_faces, known_names, debug_mode):
    try:
        print("Recognition running on: " + videoLocation)
        
        cap = cv2.VideoCapture(videoLocation)


        # Display some information about the video provided
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if (fps == 0):
            fps = 1

        duration = str(datetime.timedelta(seconds=int(frame_count/fps)))

        print("Video FPS: ",fps)
        print("Frame Count: ",frame_count)
        print("Video Duration: ",duration)

        # Important variable to control the number of frames skiped before face check
        frame_skips = fps

        # Open up the video and go through it frame by frame
        success, image = cap.read()
        difference = fps
        count = 0

        # We create a dictionary to store a player and the frames they appear at
        people_dict = {}

        while success:

            if (difference == frame_skips):

                if (debug_mode):
                    print("Frame: ",count)
                else:
                    # Just a little thing to report on the progress of the detection in the terminal
                    print("Progress:",(count/frame_count), end="\r")


                # See if there was a match with a face
                current_match = detectFacesInImage(image, known_faces, known_names, debug_mode=debug_mode)

                # Make sure it was an actual face that was detected
                if (current_match != []):

                    # For all the people detected in this frame
                    for person in current_match:

                        # Check if they are already in the dictionary
                        if (person in people_dict):
                            # They are in the video so append this frame number to this persons list
                            people_dict[person].append(count)
                        else:
                            # They are not in the video so add them to the dictionary
                            people_dict[person] = []
                            people_dict[person].append(count)


                difference = 0
            else:
                difference += 1

            count += 1
            success, image = cap.read()


        return people_dict

    except Exception as e:
        traceback.print_exc()
        #print("---- Ran into an issue----\n",e)


    return None



if __name__ == "__main__":
    known_faces, known_names = loadAllFaces()
    print(known_names)

    # Detecting faces in Video
    #print(detectVideoFaces('rugby_footage_1.mp4', known_faces, known_names, debug_mode=True))
    print(detectVideoFaces('IrelandVFrance.mp4', known_faces, known_names, debug_mode=True))
    #print(detectVideoFaces('LEINSTERVULSTER TIL.mp4', known_faces, known_names, debug_mode=True))

    # Detect faces in Image
    #print(detectFacesInImage("unknown_faces/whothis.png", known_faces, known_names))

    # Detect faces in image from path
    #print(detectFacesInImageFile("unknown_faces/3_amigos.jpg", known_faces, known_names))

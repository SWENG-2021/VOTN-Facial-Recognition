
""" New code using the face-recognition library for python """

import face_recognition
import cv2
import os



""" Some Constants for the project """

KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = 0.6            # Lower value for more accuracy
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
Function to detect all faces in an image
'''
def detectFacesInImage(imageLocation, known_faces, known_names):
    # So we get the image that we want want to analyse
    image = face_recognition.load_image_file(imageLocation)

    # Next find all the locations which contain faces
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)

    # Next we want to be able to draw boxes around the faces on the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Now iterate over the encodings and locations
    for face_encoding, face_location in zip(encodings, locations):

        # We want to see if there are any matches that we can find
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        #print(results)

        # Now check what indexes we got a detection at to figure out the name for the face
        match = []
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

    cv2.imshow("Output",image)
    cv2.waitKey(0)
    cv2.destroyWindow("Output")

    return match




'''
Function to detect all faces in a video
'''
def detectVideoFaces(videoLocation, known_faces, known_names):
    pass



def main():
    print("\nTesting main() Function")

main()

known_faces, known_names = loadAllFaces()
print(known_names)

# detectFacesInImage("unknown_faces/whothis.png", known_faces, known_names)
#detectFacesInImage("unknown_faces/jsexton-1.png", known_faces, known_names)
#detectFacesInImage("unknown_faces/some_players.jpg", known_faces, known_names)
print(detectFacesInImage("unknown_faces/3_amigos.jpg", known_faces, known_names))


"""
Early Steps (Non anaconda approach)
1) Make sure Python 3.5+ is installed
2) Make sure you pip install opencv-python (4.3.0.36 is the version I am using)
3) Test that the pip install works for opencv (test importing it)


Design Steps
-------------------------------------------------------------------------------
1) Now need to think about how we get the video into the python program
2) What kind of processing do we need to do with the video
3) What do we do with the data generated?


How to use:
-------------------------------------------------------------------------------
1) If you want to do facial recognition on a still image
        py recognition.py picture.png i

2) If you want to do facial recognition on a video
        py recognition.py video.mp4 v
"""

import cv2
import sys
import datetime
import time


# Get user supplied values
imagePath = sys.argv[1]
formatSetting = sys.argv[2]     # i = image, v = video
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)



def imageDetection(show_results):
    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    if (show_results):
        #Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Faces found", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



def videoDetection(show_results):
    cap = cv2.VideoCapture(imagePath)
    #cap = cv2.VideoCapture("rugby_footage_1.mp4")


    # Display some information about the video provided
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = str(datetime.timedelta(seconds=int(frame_count/fps)))

    print("Frame Count: ",frame_count)
    print("Video FPS: ",fps)
    print("Video Duration: ",duration)


    # Next we open the video up and go through frame by frame
    start_time = time.time()

    success, image = cap.read()
    count = 0
    i = 0

    while success:
        success, image = cap.read()

        # Detect if there was a face in the frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Display the faces in the footage
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Faces found", image)
        cv2.waitKey(0)




    print("Time to analyse: --- %s seconds ---" % (time.time() - start_time))
    print("Number of frames with faces: ",faces)







#Here is the main function
def main():
    print("Starting Program")

    if (formatSetting == 'v'):
        # We are taking in a video
        videoDetection(show_results = True)
        print("Finished Video Detection")

    elif (formatSetting == 'i'):
        # We are taking in an image
        imageDetection(show_results = True)
        print("Finished Image Detection")

    else:
        print("Error: invalid format setting provided. Use 'v' for video or 'i' for image.")

main()
print("Exiting out of program")

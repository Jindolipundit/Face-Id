import cv2
import numpy as np
from face_detection import detect_faces
from facial_landmarks import extract_facial_landmarks
from face_analysis import *

# Function to display the detected faces with dots and show the webcam
def display_faces_with_dots(facial_landmarks):
    # Create a VideoCapture object to read from the webcam
    video_capture = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not video_capture.isOpened():
        raise Exception("Could not open video capture device")

    while True:
        # Read a frame from the webcam
        ret, frame = video_capture.read()

        # Check if the frame was read successfully
        if not ret:
            raise Exception("Failed to read frame from video capture")

        # Detect faces in the frame
        faces = detect_faces(frame)

        # Extract facial landmarks for each face
        landmarks = extract_facial_landmarks(frame, faces)

        # Display the detected faces with dots
        for face, points in zip(faces, landmarks):
            for (x, y) in points:
                cv2.circle(frame, (x, y), radius=7, color=(0, 255, 0), thickness=-1)
            (x, y, w, h) = face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Show the frame with detected faces
        cv2.imshow('Face Scan', frame)

        # Check if enough landmarks have been collected
        if len(facial_landmarks) < 70:
            facial_landmarks.extend(landmarks)

        # Check if enough landmarks have been collected
        if len(facial_landmarks) >= 70:
            save_facial_landmarks(facial_landmarks)
            break

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the video capture object and close the windows
    video_capture.release()
    cv2.destroyAllWindows()

    # Prompt the user for testing face ID
    answer = input("Do you want to test the face ID? (y/n): ")

    if answer.lower() in ['y', 'yes']:
        # Load the saved facial landmarks
        saved_landmarks = load_facial_landmarks()

        # Compare the saved landmarks with the current landmarks
        if np.array_equal(facial_landmarks, saved_landmarks):
            print("WORKS: Face ID matches.")
        else:
            print("DID NOT WORK: Face ID does not match.")
    elif answer.lower() in ['n', 'no']:
        print("Program terminated.")
    else:
        print("Invalid response. Program terminated.")

# Function to save the facial landmarks
def save_facial_landmarks(facial_landmarks):
    np.save('facial_landmarks.npy', facial_landmarks)
    print("Done scanning.")

# Function to load the saved facial landmarks
def load_facial_landmarks():
    return np.load('facial_landmarks.npy')

if __name__ == '__main__':
    # Initialize the facial landmarks
    facial_landmarks = []
    display_faces_with_dots(facial_landmarks)

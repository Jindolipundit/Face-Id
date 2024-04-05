import cv2
from face_detection import detect_faces
from facial_landmarks import extract_facial_landmarks

def display_faces_with_dots():
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        raise Exception("Could not open video capture device")

    start_time = cv2.getTickCount()
    
    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            raise Exception("Failed to read frame from video capture")

        current_time = cv2.getTickCount()
        elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
        
        cv2.putText(frame, f"Elapsed Time: {elapsed_time:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        faces = detect_faces(frame)
        landmarks = extract_facial_landmarks(frame, faces)

        for face, points in zip(faces, landmarks):
            for (x, y) in points:
                cv2.circle(frame, (x, y), radius=1, color=(0, 255, 0), thickness=-1)
            (x, y, w, h) = face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('Face Scan', frame)

        if elapsed_time >= 5.0:
            break

        if cv2.waitKey(1) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    answer = input("Do you want to scan? (y/n): ")

    if answer.lower() in ['y', 'yes']:
        # Place the code to scan the face and save the landmarks here
        # Modify the code to collect the necessary number of landmarks
        
        # After scanning, save the facial landmarks using:
        # save_facial_landmarks(facial_landmarks)

        print("Scan completed.")
    elif answer.lower() in ['n', 'no']:
        print("Scan cancelled.")
    else:
        print("Invalid input. Scan cancelled.")

if __name__ == '__main__':
    display_faces_with_dots()

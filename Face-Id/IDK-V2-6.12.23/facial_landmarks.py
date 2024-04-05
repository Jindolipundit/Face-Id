import cv2
import mediapipe as mp

def extract_facial_landmarks(image, faces):
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)
    
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    landmarks = []
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            face_points = []
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                face_points.append((x, y))
            landmarks.append(face_points)
    
    return landmarks

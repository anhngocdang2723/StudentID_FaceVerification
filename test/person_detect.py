import cv2
import face_recognition
import numpy as np

# Load a sample image and learn how to recognize it
try:
    known_image = face_recognition.load_image_file(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\(delete)img\NgocAnh_face.jpg")
    known_encoding = face_recognition.face_encodings(known_image)[0]
except IndexError:
    print("Error: Unable to detect a face in the provided image.")
    exit(1)

# Create arrays of known face encodings and their names
known_face_encodings = [known_encoding]
known_face_names = ["Ngoc Anh"]

# Initialize the webcam
video_capture = cv2.VideoCapture(1)
if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit(1)

print("Press 'q' to exit the program.")

while True:
    # Capture a single frame from the webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break

    # Resize frame for faster processing (optional)
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through each detected face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the detected face matches the known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"

        # Use the known face with the smallest distance if a match was found
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Scale back up face locations since the frame was resized
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        # Label the face with the name
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Press 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()

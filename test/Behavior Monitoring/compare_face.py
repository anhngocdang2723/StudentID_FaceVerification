import cv2
import face_recognition
import threading
from queue import Queue
import time

# Load and encode reference face
reference_image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\(delete)img\NgocAnh_face.jpg"
reference_image = face_recognition.load_image_file(reference_image_path)
reference_encoding = face_recognition.face_encodings(reference_image)[0]

def process_frame(frame, result_queue):
    # Resize frame for faster face detection
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    result_queue.put((face_locations, face_encodings))

# Initialize video capture
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

# Initialize variables
process_this_frame = True
result_queue = Queue()
last_thread = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Only process every other frame
    if process_this_frame:
        if last_thread is not None and last_thread.is_alive():
            last_thread.join()

        # Start processing in a separate thread
        thread = threading.Thread(target=process_frame, args=(frame, result_queue))
        thread.start()
        last_thread = thread

    process_this_frame = not process_this_frame

    # Get results if available
    if not result_queue.empty():
        face_locations, face_encodings = result_queue.get()

        # Scale back face locations
        face_locations = [(top*4, right*4, bottom*4, left*4)
                         for (top, right, bottom, left) in face_locations]

        # Display results
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([reference_encoding],
                                                   face_encoding,
                                                   tolerance=0.5)
            label = "Match" if matches[0] else "Not Match"

            color = (0, 255, 0) if matches[0] else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow('Face Comparison', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
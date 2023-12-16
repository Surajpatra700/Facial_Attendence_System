import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

video_capture = cv2.VideoCapture(0)

elon_image = face_recognition.load_image_file("Photos/elon.jpeg")
elon_encoding = face_recognition.face_encodings(elon_image)[0]

dhoni_image = face_recognition.load_image_file("Photos/dhoni.jpg")
dhoni_encoding = face_recognition.face_encodings(dhoni_image)[0]

jeff_image = face_recognition.load_image_file("Photos/jeff.jpg")
jeff_encoding = face_recognition.face_encodings(jeff_image)[0]

known_face_encoding = [
    elon_encoding,
    dhoni_encoding,
    jeff_encoding
]

known_faces_name = [
    "Elon Musk",
    "Ms Dhoni",
    "Jeff Bezos"
]

students = known_faces_name.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv', 'w+', newline= '')
lnwritter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,:: 1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            
        #for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_name[ best_match_index]

                # Draw a bounding box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Add a label with the recognized name
                cv2.putText(frame, name, (left, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

            # Writing data to CSV fie

            face_names.append(name)  
            if name in known_faces_name:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwritter.writerow([name,current_time])

    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
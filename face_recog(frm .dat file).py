import face_recognition
import cv2
import time 
import numpy as np
import pickle
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
    

with open('aditya_faces.dat', 'rb') as f:
    aditya_face_encoding = pickle.load(f)
    
with open('jatin_faces.dat', 'rb') as f:
    jatin_face_encoding= pickle.load(f)
    
with open('rakshit_faces.dat', 'rb') as f:
    rakshit_face_encoding= pickle.load(f)    
    
with open('komal_faces.dat', 'rb') as f:
    komal_face_encoding= pickle.load(f)
    
    
    
    
# Create arrays of known face encodings and their names
known_face_encodings = [
    aditya_face_encoding,
    jatin_face_encoding,
    rakshit_face_encoding,
    komal_face_encoding    
]
   
known_face_names = [
    "You are Aditya Surana",
    "You are Jatin Sharma",
    "You are Rakshit Porwal",
    "You are Komal Sharma"
]
       

# Initialize some variables

face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #small_frame = cv2.rotate(small_frame,rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_encodings = face_recognition.face_encodings(small_frame)
        #print(face_encodings)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "sorry but can't recognise you"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                first_match_index
                name = known_face_names[first_match_index]

            face_names.append(name)
            #time.sleep(30)
            rtn_recoged = ''.join(str(i) for i in face_names)           
            def rtn_recoged_face():
                return(rtn_recoged)
                
            print(rtn_recoged_face())


process_this_frame = not process_this_frame

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
    

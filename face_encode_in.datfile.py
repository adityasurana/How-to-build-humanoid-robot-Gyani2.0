import face_recognition
import numpy as np
import os
import pickle

# Load a sample picture and learn how to recognize it.
aditya_image = face_recognition.load_image_file("/home/pi/Desktop/adi1.jpg")
aditya_face_encoding= face_recognition.face_encodings(aditya_image)[0]

# Load a sample picture and learn how to recognize it.
jatin_image = face_recognition.load_image_file("/home/pi/Desktop/jatin.jpg")
jatin_face_encoding  = face_recognition.face_encodings(jatin_image)[0]

# Load a sample picture and learn how to recognize it.
rakshit_image = face_recognition.load_image_file("/home/pi/Desktop/raxx.jpg")
rakshit_face_encoding = face_recognition.face_encodings(rakshit_image)[0]

# Load a sample picture and learn how to recognize it.
komal_image = face_recognition.load_image_file("/home/pi/Desktop/komal.jpg")
komal_face_encoding = face_recognition.face_encodings(komal_image)[0]


with open('aditya_faces.dat', 'wb') as f:
    pickle.dump(aditya_face_encoding, f)
 
with open('jatin_faces.dat', 'wb') as f:
    pickle.dump(jatin_face_encoding , f)
    
    
with open('rakshit_faces.dat', 'wb') as f:
    pickle.dump(rakshit_face_encoding , f)
    
    
with open('komal_faces.dat', 'wb') as f:
    pickle.dump(komal_face_encoding , f)    
    
  
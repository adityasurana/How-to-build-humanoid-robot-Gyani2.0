import os
import speech_recognition as sr #speech recognition library for converting speech to text
import dialogflow_v2beta1 as dialogflow #google's apiai
import cv2 #OpenCV library for opening video camera
import RPi.GPIO as GPIO #for connections with GPIO pins
import face_recognition #face_recognition library for recognizing face
import numpy as np
import pickle #to load .dat file which has face_encodings saved in it 
import serial #for connections with serial port
import time

r = sr.Recognizer() 
m = sr.Microphone(device_index=2)  #device_index should be set according from which microphone you want to listen (if more than one microphone)

#running file on system which has credentials of dialogflow, path where file is kept="/home/pi/", file name="botv2-33024-2903d4abace7.json" 
os.system('export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/botv2-33024-2903d4abace7.json"')
project_id='botv2-33024' #project_id is given in your dialogflow bot settings
session_id='abcd' #session_id can be any string
language_code='en-US' 
session_client = dialogflow.SessionsClient()
session_path = session_client.session_path('botv2-33024', 'abcd')
print('Session path: {}\n'.format(session_path))

GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #ignore warning for now
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin 10 to be an input pin and set initial vaue to be pulled low (off)


while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH: #if getting high from GPIO pin no. 10 
        os.system("python3 eye.py") #running eye.py file on system (eye will be displayed on oled displays)
        print('Listening...')
        while True:
            try:
                print("A moment of silence, please...")
                with m as source:
                    r.adjust_for_ambient_noise(source, duration=2)
                while True:
                    print("Say something!")
                    os.system("python3 mic.py") #mic will be displayed on oled displays
                    with m as source:
                        audio = r.record(source, duration=3)
                    
                    try:
            # we need some special handling here to correctly print unicode characters to standard output
                        if str is bytes:
                            print("You said {}".format(value).encode("utf-8"))# this version of Python uses bytes for strings (Python 2)
                            print(os.system('vlc listen.wav vlc://quit'))
                        else:
                            print("You said {}".format(value))#this version of Python uses bytes for strings (Python 3)

                 #recognize speech using Google Speech Recognition
                        texts = r.recognize_google(audio)
                        os.system("python3 wave.py") # wave will be displayed on oled, displaying process is running.
#after converting speech into text, text will be stored in variable 'texts' and will be send to dialogflow agent.
                        text_input = dialogflow.types.TextInput(text=texts, language_code='en-US')
                        query_input = dialogflow.types.QueryInput(text=text_input)
                        output_audio_config = dialogflow.types.OutputAudioConfig(audio_encoding=dialogflow.enums.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16)
                        response = session_client.detect_intent(session=session_path, query_input=query_input,output_audio_config=output_audio_config)

            #above code will return an audio(response of query) which will be saved as 'output.wav'
                        with open('output.wav', 'wb') as out:
                            out.write(response.output_audio)
                        print('Audio content written to file "output.wav"')
                        #audio file('output.wav') will be played using vlc media player
                        print(os.system('vlc output.wav vlc://quit'))
                        print('Query text: {}'.format(response.query_result.query_text))
                        print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
                        print('Action: {}\n'.format(response.query_result.action))
            
                        action = response.query_result.action
                
                        if action=="z":
                            print("bye bye")
                        
                        elif action=="p":# 'p' action will be returned by dialogflow agent if someone said recognise me or related  
                            try:
              #it will first give command to arduino through serial port to lift the head of robot a little bit
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encosde('utf-8'))
                                time.sleep(0.5)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.read
                                arduinoSerialData.write(arduino.encode('utf-8'))
             				#from here face recognition process starts
                                video_capture = cv2.VideoCapture(0) #video camera opens

    #will read the face_encodings already saved on the system with names 'aditya_faces.dat','jatin_faces.dat',etc..         
                                with open('aditya_faces.dat', 'rb') as f:
                                    aditya_face_encoding = pickle.load(f)
                                with open('jatin_faces.dat', 'rb') as f:
                                    jatin_face_encoding= pickle.load(f)
                                with open('rakshit_faces.dat', 'rb') as f:
                                    rakshit_face_encoding= pickle.load(f)    
                                with open('komal_faces.dat', 'rb') as f:
                                    komal_face_encoding= pickle.load(f)
                        
                #Create arrays of known face encodings and their names
                                known_face_encodings = [                                    
                                    aditya_face_encoding,
                                    jatin_face_encoding,
                                    rakshit_face_encoding,
                                    komal_face_encoding   
                                ]
   		   #Names of people for the above face encodings
                                known_face_names = [
                                    "name aditya",
                                    "name jatin",
                                    "name rakshit",
                                    "name komal"
                                ]
		#Initializing some variables
                                face_encodings = []
                                face_names = []
                                process_this_frame = True

			#Grabing a single frame of video
                                ret, frame = video_capture.read()

			#Resizing frame of video to 1/4 size for faster face recognition processing
                                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                                '''THIS CODE IS FOR THE POSITIONING OF CAMERA'''
                                small_frame = cv2.rotate(small_frame, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
                                small_frame = cv2.flip(small_frame, flipCode=1)
                                small_frame= cv2.rotate(small_frame, rotateCode=cv2.ROTATE_180)
                                
                                if process_this_frame:
                                    face_encodings = face_recognition.face_encodings(small_frame)
                                    for face_encoding in face_encodings:
                                   #See if the face is a match for the known face(s)  
                                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                        name = "sorry but can't recognise you"

        				#If a match was found in known_face_encodings, just use the first one.
                                        if True in matches:
                                            first_match_index = matches.index(True)
                                            first_match_index
                                            name = known_face_names[first_match_index]

                                            face_names.append(name)
                                            rtn_recoged = ''.join(str(i) for i in face_names)
                                            print(rtn_recoged)

                                process_this_frame = not process_this_frame
                                video_capture.release()#camera will be closed 
                                cv2.destroyAllWindows()#windows will be destroyed

               #text-'rtn_recoged' will be send to dialogflow agent which contain name of person who's face is recognised. 
                                text_input = dialogflow.types.TextInput(text=rtn_recoged, language_code='en-US')
                                query_input = dialogflow.types.QueryInput(text=text_input)
                                output_audio_config = dialogflow.types.OutputAudioConfig(audio_encoding=dialogflow.enums.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16)
                                response = session_client.detect_intent(session=session_path, query_input=query_input,output_audio_config=output_audio_config)

                        #above code will return an audio(response of query) which will be saved as output.wav2        
                                with open('output2.wav', 'wb') as out:
                                    out.write(response.output_audio)
                                print('Audio content written to file "output2.wav"')
                                #audio file('output2.wav') will be played using vlc media player
                                print(os.system('vlc output2.wav vlc://quit'))
                                print('Query text: {}'.format(response.query_result.query_text))
                                print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
                                break
                            except:
                                break

                        elif action=='h': #action will be 'h' if love emotion is to be shown by answer 
                            try:
                                os.system("python3 heart.py") #heart will be displayed on oled displays
                                os.system("python3 eye.py")   #eye will be displayed on oled displays again
                                break
                            except:
                                break

                        elif action=='g': #action will be 'g' if money emotion is to be shown by answer
                            try:
                                os.system("python3 money.py") #rupee symbol will be displayed on oled displays
                                os.system("python3 eye.py")   #eye will be displayed on oled displays again
                                break
                            except:
                                break

                        elif action=='l': #'l'action will be returned by dialogflow agent if someone asks to play music
                            try:
                                os.system("python3 music.py") #music symbol will be displayed on oled displays
                                os.system("python3 sound.py") #random music already stored on system will be played
                                time.sleep(4)
                                os.system("python3 eye.py")   #eye will be displayed on oled displays again 
                                break
                            except:
                                break       
                            
                        elif action == 'a': #'a'action will be returned if someone asks to move forward
                            try:
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8')) #encoded form of 'a' will be send to arduino
                                time.sleep(4)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))  #after 4 seconds '0' will be send back to arduino
                                break
                            except:
                                break

                        elif action == 'b': #'b'action will be returned if someone asks to move right
                            try:
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8')) #encoded form of 'b' will be send to arduino
                                time.sleep(0.9)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))  #after 0.9 seconds '0' will be send back to arduino
                                break
                            except:
                                break

                        elif action == 'c': #'c'action will be returned if someone asks to move left
                            try:
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8')) #encoded form of 'b' will be send to arduino
                                time.sleep(0.9)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))  #after 0.9 seconds '0' will be send back to arduino
                                break
                            except:
                                break

                        elif action == 'd':  #'d'action will be returned if someone asks to move backward
                            try:
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8'))
                                time.sleep(4)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))
                                break
                            except:
                                break
                            break
                        elif action == 'e':  #'e'action will be returned if 'hello' is said, (robot will shake hand in this action)
                            try:
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8'))
                                time.sleep(4)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))
                                break
                            except:
                                break

                        elif action == 'f':  #'f'action will be returned if 'namaste' is said, (namaste action will be executed)
                            try:
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8'))
                                time.sleep(5)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))
                                break
                            except:
                                break
                
                        elif action == 'i': #'i'action will be returned if someone asked for 'dance', (Robot will perform dance)
                            try:
                            	os.system("python3 music.py") #music symbol will be displayed on oled displays
                                os.system("python3 sound.py") #random music already stored on system will be played
                                arduino='0'
                                response_action = response.query_result.action
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(response_action.encode('utf-8'))  #encoded value of 'i' will be send to arduino
                                time.sleep(10)
                                arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
                                arduinoSerialData.write(arduino.encode('utf-8'))  #after 10 seconds '0' will be send back to arduino 
                                os.system("python3 eye.py")
                                break
                            except:
                                break
                            break
                        else:
                            print("no action")
                            break
                        
                    except sr.UnknownValueError:
                        print("Oops! Didn't catch that")
#an audio 'oops.wav' containing recording "Oops Didn't catch that" will be played, if the speech to text converter didn't recognise the audio 
                        os.system('vlc oops.wav vlc://quit')  

                    except sr.RequestError as e:
                        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                        
            except KeyboardInterrupt:
                            pass
            
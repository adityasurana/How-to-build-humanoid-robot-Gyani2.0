# What is the project about?
This repository contains software design and code of the Humanoid Robot(Gyani 2.0) created by our team. It works as a receptionist for our college and also got featured in National press (Times of India, Danik Bhaskar and live telecast on News 18) of India.

Features of Humanoid Robot(Gyani2.0) :-

-> It can answer all your questions related to our college (works as a receptionist) and can greet you with Namaste, hand shake, etc .

-> Recognizing ability.

-> It can dance, play music and perform simple arithmetic operations.

-> Can answer your knick-knacks (natural questions).

-> Oled displays can display emotions in eyes. 

-> Body parts are made by 3D printing.
# Process flow of the project:-
![process](https://user-images.githubusercontent.com/39646018/58369617-817f6d80-7f1a-11e9-9427-c5bdfd5c733e.png)

# Requirements :-
Hardware used in the project is specified in 'hardware_requirement.docx' of this repository.

Dependencies that should be installed on raspberry pi before starting is listed in 'software_dependencies.docx'of this repository.

# Code Overview:-
In this repository 'maincode.py' consist of the major processing:-

(1) Used google's Speech To Text converter to convert user queries into text from speech.

(2) That text is then sended to Google's apiai(Dialogflow).

Google's apiai([Dialogflow](https://dialogflow.com/)) is an end-to-end, build-once deploy-everywhere development suite for creating conversational interfaces for websites, mobile applications, popular messaging platforms, and IoT devices. You can use it to build interfaces such as chatbots, conversational IVR, etc.

![Dialogflow_Process](https://user-images.githubusercontent.com/39646018/58425639-e6bc9580-80b7-11e9-8924-ba7881194739.png)

(3) After sending the queries to Dialogflow(v2_beta) version in text format an appropriate response comes in the form of audio and we save that to our system(on raspberry pi).

(4) Now the audio is played using VLC media player present in the system.

(5) Actions are also predefined accordingly to the response of any query, if response contain action:-

(5.a) Recognise me - then face recognition code will be executed. For face recognition I have used openCV and face_recognition libraries. The face_encodings in '.dat' format files are pre stored on the system.

(5.b) Emotions - then an emotion on the Oled displays will be displayed. Like for 

Love -> Oled will display 'img/heart.png'

any responses related to Money -> 'img/rs.png'

Music, Dance -> 'img/music.png' etc.

(5.c) Physical actions to be performed - then a data signal will be sent to Arduino through serial port (serial data communication) to instruct servo motors to perform required action.

The code is self explanatory.

 # Body Strcture of Gyani2.0 :-
![gyani_bodystructure](https://user-images.githubusercontent.com/39646018/61180295-f6754680-a631-11e9-9307-05d5c1bd5616.png)

# Action(Movements) Processflow :-
![moveent_processflow](https://user-images.githubusercontent.com/39646018/61180244-66cf9800-a631-11e9-943d-7b0c3312839f.PNG)
   






















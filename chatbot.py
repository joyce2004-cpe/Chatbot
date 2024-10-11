# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 10:37:35 2024

@author: Abija Joyce
"""

import pyttsx3
from datetime import datetime
import speech_recognition as sr
import requests
import face_recognition
import cv2
import numpy as np



opening_text = [
    "I'm on it ma.",
    "I'm working on it.",
    "Hold on a bit ma.",
]


USERNAME = 'Joyce'


def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.say(command)
    #voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"

    engine.runAndWait()


def greet_user():
    hour = datetime.now().hour
    if (hour >= 0) and (hour < 12):
        SpeakText('Good Morning {}'.format(USERNAME))

    elif (hour >= 12) and (hour < 16):
        SpeakText('Good Afternoon {}'.format(USERNAME))

    elif (hour >= 16) and (hour < 20):
        SpeakText('Good Evening Mrs {}'.format(USERNAME))
    SpeakText('I am Jarvis. Your personal assistant. How may I assist you?')




def user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source2:


        # listens for the user's input
        audio2 = r.listen(source2)

        # Using google to recognize audio
    try:
        print('Recognizing...')
        query = r.recognize_google(audio2, language='en-NG')
        if 'exit' in query or 'stop' in query:
            #     SpeakText(choice(opening_text))
            # else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                SpeakText("Good night ma, take care!")
            else:
                SpeakText('Have a good day ma!')
            exit()
    except Exception:
        SpeakText('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query



def chat(query):


    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"
    
    payload = {
    	"messages": [
    		{
    			"role": "user",
    			"content": query
    		}
    	],
    	"system_prompt": "",
    	"temperature": 0.9,
    	"top_k": 5,
    	"top_p": 0.9,
    	"max_tokens": 100,
    	"web_access": False
    }
    headers = {
    	"x-rapidapi-key": "e1be95243fmsh6fc2c663f4774bap18b265jsn92f736a37a5b",
    	"x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    	"Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers).json()


    reply = response['result']
    reply = reply.replace('OpenAI', 'Joyce')

    return reply




if __name__ == '__main__':

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    # joyce_image = face_recognition.load_image_file(r"C:\Users\HP\Pictures\Camera Roll\WIN_20231117_01_52_49_Pro.jpg")
    # joyce_face_encoding = face_recognition.face_encodings(joyce_image)[0]

    # Load a second sample picture and learn how to recognize it.
    Joyce_image = face_recognition.load_image_file(
        r"my_pics.jpg")
    Joyce_face_encoding = face_recognition.face_encodings(Joyce_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        
        Joyce_face_encoding
    ]
    known_face_names = [
        "Joyce"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        # Display the resulting imageK
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if 'Joyce' in face_names:
            greet_user()
            video_capture.release()  # Stop capturing from the webcam
            cv2.destroyAllWindows()  # Close any OpenCV windows
            break  # Exit the while loop to stop the program

    while True:

            query = user_input().lower()
            listening = False
            conversation = chat(query)
            SpeakText(conversation)
            SpeakText(
                "For your convenience, I am printing it on the screen ma.")
            print(conversation)
    # Hit 'q' on the keyboard to quit!
    




# -*- coding: utf-8 -*-


# import libraries
import cv2
import face_recognition
from time import sleep
from ctypes import CDLL
import sys, os
import Quartz
from datetime import datetime
import mac_tag
import subprocess


filepath = "/./"
user_image0 = face_recognition.load_image_file(filepath + "known/.jpg")
user_encoding0 = face_recognition.face_encodings(user_image0)[0]
user_image1 = face_recognition.load_image_file(filepath + "/known/.jpg")
user_encoding1 = face_recognition.face_encodings(user_image0)[0]
user_face_encodings = [
    user_encoding0,
    user_encoding1
]
user_face_names = [
    "abc",
    "def"
]
app_name = " "
camera_name = ' '
defaultcameraindex = 2


def listCameras():
    #requires FFMPEG
    p = subprocess.Popen(['ffmpeg', '-f', 'avfoundation', '-list_devices', 'true', '-i'], stout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    stdout,stderror
    print(stdout)

lc = listCameras

def is_runnning():
    count = int(subprocess.check_output(["osascript",
                "-e", "tell application \"System Events\"",
                "-e", "count (every process whose name is \"" + app_name + "\")",
                "-e", "end tell"]).strip())
    return count

def onoff():

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        #print("checking...")
        # Grab frame
        success, image = video_capture.read()
        if success:
            ret, frame = video_capture.read()
        else:
            sys.exit("error")

        # Convert BGR color to RGB color
        #rgb_frame = frame[:, :, ::-1]
        #rgb_frame = frame[:, :, 1]
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = small_frame[:, :, ::-1]
        #cv2.imshow('RESULT',rgb_frame)
        sleep(3)

        # Find faces in frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(user_face_encodings, face_encoding)
            name = "Unknown"

            #If a match was found in user_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = user_face_names[first_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame

        #print(face_locations)
        if len(face_locations) < 1:
            try:
                #No Face found
                stamp_raw = datetime.now().strftime("%Y-%m-%d %H %M %S")
                stamp = stamp_raw.replace(' ','-')
                filename = filepath + 'invalid_face_' + stamp + ".jpg"
                cv2.imwrite(filename, rgb_frame)
                loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
                result = loginPF.SACLockScreenImmediate()
                sleep(2)
                sys.exit("Face Not Found")
            except Exception as e:
                    print(e)
                    sleep(2)
                    sys.exit("Lock Error")
        else:
            #Face found
            stamp_raw = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            stamp = stamp_raw.replace(' ','-')
            filename = filepath + 'valid_face_' + stamp + ".jpg"
            #Add Text
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.imwrite(filename, rgb_frame)
            grayimage = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            newimage = cv2.cvtColor(grayimage, cv2.COLOR_GRAY2RGB)
            cv2.putText(newimage,stamp,(200,250),font, .5,(255,255,),2,cv2.FILLED)
            cv2.imwrite(filename, newimage)
            sleep(2)
            sys.exit()

# Check if screen already locked
print("🔘")
if is_runnning() > 0:
    appstart = onoff()
else:
    pass

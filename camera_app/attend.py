#For OpenCV
import cv2
import sys
import time
import numpy as np

#For Http request
import requests

#Other python lib
import datetime
import time
import os

import os
import errno

#Global vairables
_img_url = "http://localhost:8000/post"

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cv2.namedWindow("cam")

#Function definition
def showImgFunct( cam_img ):
##This function is just for debug usage
    
    #show the image
    cv2.imshow("cam", cam_img)
    return

def storeImgFunct( img, timeStamp ):
## This function store the camera image with timeStamp
    fm = "./" + timeStamp + ".png"
    
    cv2.imwrite( fm, img)

    print("Image stored in " + fm )

    return fm

def storeMultiFunct( dir, imgs, timeStamp):
## This function store the faces with timeStamp
    file_names = []

    for idx, img in enumerate(imgs):

        fm = dir + "/ppl_" + str(idx) + ".png"
        
        file_names.append( fm )

        cv2.imwrite( fm, img )

        print("Image stored in " + fm )

    return file_names

def postFunct( img , file_name):
## This function send image to server for emotion analysis

    #Open the file to send
    f = {'file': open(file_name, 'rb')}

    #Send out the post request
    server_res = requests.post(_img_url, files=f)

    print("Sending POST request ................... ")

    if( server_res.status_code == 200 ):
        print("Good")
    else:
        raise Exception
    return

def postMultFunct( imgs , file_names ):
## This function send images to server for emotion analysis

    sending_files = []

    if (imgs.count() != file_names.count() ):
        print("image count and file_name count mismatch")
    
    for fm in file_names:
        sending_files.append( 'file', open( fm, 'rb') )

    print( "sending out these files", sending_files )

    #Send out the post request
    server_res = requests.post(_img_url, files=sending_files, size=len(file_names) )
    
    print("Sending POST request ................... ")
    
    if( server_res.status_code == 200 ):
        print("Good")
    else:
        raise Exception
    return


##Main function
print("Usage: press 'c' to capture faces, press 'ese' to quit")

video_capture = cv2.VideoCapture(0)

while True:
    
    ppl_faces = []
    face_x = []
    face_y = []
    face_w = []
    face_h = []
    
    if not video_capture.isOpened():
        print('Unable to load camera.')
        time.sleep(5)
        pass

    #Read in image
    ret, img = video_capture.read()

    #Resize image to 50%
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

    #Change to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        ##Add face coordinate to python list
        face_x.append( np.asscalar(x) ) #Change data type from numpy.uint32 -> python int
        face_y.append( np.asscalar(y) )
        face_w.append( np.asscalar(w) )
        face_h.append( np.asscalar(h) )
        
        print("Face count:", len(face_x), " x:", x, " y:", y, " w:", w, " h:", h)

    #Show image for debug usage
    showImgFunct(img)

    #Read in key input
    cmd = cv2.waitKey(1)

    if (  cmd == 27 ):
        ##Esc exit program
        break
    elif ( cmd == ord('c') and len(faces) >= 1 ):

        #Capture people's faces array
        for idx, val in enumerate(face_x):
            face = img[ face_y[idx] : face_y[idx] + face_h[idx], face_x[idx] : face_x[idx] + face_w[idx] ]
            ppl_faces.append( face )
        
        #Store the image, current time as directory name
        path = str(os.getcwd()) + "/" +  time.strftime("%Y_%m_%d_%H_%M_%S")

        try:
            os.makedirs(path)
        except Exception:
            print( "Fail to create directory" );

        files = storeMultiFunct( path, ppl_faces, str( datetime.datetime.now() ) )
        
        try:
            #Send out the image to server
            postMultFunct( ppl_faces , files)
        except Exception as e:
            print("Http post exception ... ")

#End of the while loop

cv2.destroyAllWindows()
video_capture.release()



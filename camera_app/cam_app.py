#For OpenCV
import cv2
import sys
import time

#For Http request
import requests

#Other python lib
import datetime
import time

#Global vairables
_img_url = "http://localhost:8000/post"

cv2.namedWindow("cam")

#Function definition
def showImgFunct( cam_img ):
##This function is just for debug usage
    
    #show the image
    cv2.imshow("cam", cam_img)
    return

def storeImgFunct( img, timeStamp ):
## This function store the camera image with timeStamp
    fm = "./" + timeStamp + ".jpg"
    
    cv2.imwrite( fm, img)

    print("Image stored in " + fm )

    return fm

def postFunct( img , file_name):
##This function send image to server for emotion analysis

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

print("Usage: press 'c' to capture an image, press 'ese' to quit")

video_capture = cv2.VideoCapture(0)

while True:
    
    if not video_capture.isOpened():
        print('Unable to load camera.')
        time.sleep(5)
        pass

    #Read in image
    ret, img = video_capture.read()

    #Resize image to 50%
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

    #Show image for debug usage
    showImgFunct(img)

    #Read in key input
    cmd = cv2.waitKey(1)
    if (  cmd == 27 ):
        break
    elif ( cmd == ord('c') ):

        #Store the image
        file_name = storeImgFunct(img, str( datetime.datetime.now() ) )

        try:
            #Send out the image to server
            postFunct(img, file_name)
        except Exception as e:
            print("Http post exception ... ")
            
            #Retry in 10 sec
            #time.sleep(10)

#End of the while loop

cv2.destroyAllWindows()
video_capture.release()



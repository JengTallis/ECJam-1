#For opencv face recognition
import cv2
import sys

#For Mircosoft emotion API
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import numpy as np
import operator

#File name variable
pathToFileInDisk = sys.argv[1]

#Emotion API Variables
_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = '04578e189b6f45c0842acf276495e256'
_maxNumRetries = 10

#Emotion API process request function
def processRequest( json, data, headers, params ):
    
    """
        Parameters:
        json: Used when processing images from its URL. See API Documentation
        data: Used when processing image read from disk. See API Documentation
        headers: Used to pass the key information and the data type request
    """
    
    retries = 0
    result = None
    
    while True:
        
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        
        if response.status_code == 429:
            
            print( "Message: %s" % ( response.json()['error']['message'] ) )
            
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
    
        elif response.status_code == 200 or response.status_code == 201:
        
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )
        break
    
    return result

#Emotion API Render function
def renderResultOnImage( result, img ):
    
    """Display the obtained results onto the input image"""
    
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
                      (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                      color = (255,255,0), thickness = 3 )
    
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]
        
        textToWrite = "%s" % ( currEmotion )
        cv2.putText( img, textToWrite, (faceRectangle['left'],faceRectangle['top']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1 )

#Read in image
img = cv2.imread( pathToFileInDisk )

#Load raw image file into memory
with open( pathToFileInDisk, 'rb' ) as f:
    data = f.read()

#Emotion API headers
headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'
json = None
params = None

#Send out the request
result = processRequest( json, data, headers, params )

if result is not None:
    # Load the original image from disk
    data8uint = np.fromstring( data, np.uint8 ) # Convert string to an unsigned int array
    disk_img = cv2.cvtColor( cv2.imdecode( data8uint, cv2.IMREAD_COLOR ), cv2.COLOR_BGR2RGB )
    
    #Render the result on the image
    renderResultOnImage( result, img )
    print(result)
else:
    print("NULL result")

# Display the resulting frame
cv2.imshow('image', img)

cv2.waitKey(-1)

# When everything is done, release the capture
cv2.destroyAllWindows()

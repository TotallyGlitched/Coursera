import face_recognition as fr
from os import listdir
import requests 
from mtcnn.mtcnn import MTCNN
import json
import numpy as np
import cv2
import pickle

detector = MTCNN()

URL = "http://127.0.0.1:5000/getface"

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,1)
    imencoded = cv2.imencode(".jpg", frame)[1]
    response = requests.get("http://127.0.0.1:5000/getface", data= imencoded.tostring())
    print(response.text)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

##r = requests.get(url ='http://127.0.0.1:5000/getface',json={'face': np.array(face_encodings).tolist()})

##  face_locations = fr.face_locations(frame);
##    face_encodings = fr.face_encodings(frame,face_locations)
##    print(np.array(face_encodings).shape)


##    pil_im = Image.fromarray(frame_im)
##    stream = StringIO()
##    pil_im.save(stream, format="JPEG")
##    stream.seek(0)
##    img_for_post = stream.read()    
##    files = {'image': img_for_post}
##    response = requests.post(
##        url='/api/path-to-your-endpoint/',
##        files=files
##    )

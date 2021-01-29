# import face_recognition as fr
# from os import listdir
import requests 
from mtcnn.mtcnn import MTCNN
import json
import cv2
import pickle

detector = MTCNN()

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    if(len(detector.detect_faces(frame))==1):
        imencoded = cv2.imencode(".jpg", frame)[1]
        response = requests.get("http://192.168.43.107:5000/getface/2", data= imencoded.tostring())
        print(response.text)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

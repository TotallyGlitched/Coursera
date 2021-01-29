from flask import Flask,redirect, url_for, request,render_template,flash,jsonify
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import cv2
import numpy as np
from pymongo import MongoClient
import face_recognition
import json
from os import listdir


csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = 'zr@i-*k6gq6n=6xktv56tcmfcbyf^ck1wh=fyf155p#1j(-&g0'

UPLOAD_FOLDER = '/frimg/known/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
csrf.init_app(app)
Bootstrap(app)

client = MongoClient('mongodb://localhost:27017')
db = client.frecogniton
fr=db.fr
known_face_encodings=[]
known_face_name=[]

# print(x['fa'])
# known_face_encodings.append(x['faceencoding'])
# known_face_name.append(x['imgname'])

a=[f for f in listdir('./frimg')]
for i in a:
   qw=i.split('.')
   zxc='./frimg/'+i
   known_face_encodings.append(np.load(zxc))
   known_face_name.append(qw[0])

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@app.route('/getface', methods=['POST','GET'])
def facemp():
   # x=request.get_json()
   # x=request.files['file']
   x=request
   nparr = np.fromstring(x.data, np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   face_locations = face_recognition.face_locations(img)
   name='unknown'
   if(len(face_locations)>=1):
      fn = face_recognition.face_encodings(img)[0]
      matches = face_recognition.compare_faces(known_face_encodings, fn)
      face_distances = face_recognition.face_distance(known_face_encodings, fn)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
         name = known_face_name[best_match_index]
      return json.dumps({'suc':name})
   else:
      return json.dumps({'suc':name})
   return json.dumps({'suc':'asdf'})
@app.route('/')
def hello_world():
   return render_template('home.html')

@app.route('/register')
def register():
   form = RegistrationForm()
   return render_template('register.html',form=form)

@app.route('/registeruser', methods=['POST'])
def registeruser():
   phno=request.form['phno']
   email= request.form['email']
   name= request.form['name']
   # if(checkrep('phno',phno)==0 and checkrep('email',email)==0):
   f = request.files['photo']
   asd=email.split('@')
   f.save('/home/praveen/Desktop/python/flask/img/'+asd[0]+'.jpg')     
   face = face_recognition.load_image_file('./img/'+asd[0]+'.jpg')
   faceencoding=face_recognition.face_encodings(face)[0]
   known_face_encodings.append(faceencoding)
   known_face_name.append(asd[0])
   post_data = {
      'name': name,
      'email': email,
      'phno': phno,
      'imgname':asd[0],
      'facestorloc':'/home/praveen/Desktop/python/flask/img/'+asd[0]+'.jpg'
   }
   fr.insert_one(post_data)
   np.save('./frimg/'+asd[0],faceencoding)

   return "hi"


if __name__ == '__main__':
   app.run(debug = True)

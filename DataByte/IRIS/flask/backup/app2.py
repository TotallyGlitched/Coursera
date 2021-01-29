from flask import *
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import cv2
import numpy as np
from pymongo import MongoClient
import face_recognition
import json
from os import listdir
import bcrypt
from datetime import datetime, timedelta 
from bson.objectid import ObjectId
import time

from pusher import Pusher

csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = 'zr@i-*k6gq6n=6xktv56tcmfcbyf^ck1wh=fyf155p#1j(-&g0'
UPLOAD_FOLDER = '/frimg/known/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
csrf.init_app(app)


client = MongoClient('mongodb://localhost:27017')
db = client.frecogniton
fr=db.fr
usr=db.usr
known_face_encodings=[]
known_face_name=[]

pusher = Pusher(
   app_id='1009200',
   key='532ab91db0edb9b0876b',
   secret='9c46388d4d69e4dc4d10',
   cluster='ap2',
   ssl=True
)



a=[f for f in listdir('./frimg')]
for i in a:
   qw=i.split('.')
   zxc='./frimg/'+i
   known_face_encodings.append(np.load(zxc))
   known_face_name.append(qw[0])
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
class registerformman(FlaskForm):
   name = StringField('Name', validators=[DataRequired()])
   email = StringField('Email', validators=[DataRequired()])
   locationid = StringField('LocationID', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])
class loginForm(FlaskForm):
   email = StringField('Email', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])

members=[]


def membersdel():
   global members
   now = datetime.now()
   y=[]
   for i in range(len(members)):
      if(members[i]['time']<=now):
         y.append(i)
   for i in range(len(y)-1,-1,-1):
      del members[y[i]]
      if(len(members)==0):
         members=[]
         break

@app.route('/getface/<id>', methods=['POST','GET'])
def facemp(id):
   membersdel()
   x=request
   nparr = np.fromstring(x.data, np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   face_locations = face_recognition.face_locations(img)
   name='unknown'
   if(len(face_locations)>=1 and len(known_face_encodings)>=1):
      fn = face_recognition.face_encodings(img)[0]
      matches = face_recognition.compare_faces(known_face_encodings, fn)
      face_distances = face_recognition.face_distance(known_face_encodings, fn)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
         name = known_face_name[best_match_index]
         data=fr.find_one({'imgname': name})
         asd="a"+id
         qwe=0
         if(len(members)>0):
            for i in range(len(members)):
               if(members[i]['name']==name):
                  qwe=1
                  break
            if(qwe==0):
               zx={'name':name,'time':datetime.now()+timedelta(seconds = 10)}
               pusher.trigger(asd, "hi",{
                  'name':data['name'],
                  'email':data['email'],
                  'phno':data['phno'],
                  'fstore':data['facestorloc'],
                  'id':str(data['_id'])
                  })
               
               members.append(zx)
               qwe=0
         else:
            zx={'name':name,'time':datetime.now()+timedelta(seconds = 10)}
            pusher.trigger(asd, "hi",{
               'name':data['name'],
               'email':data['email'],
               'phno':data['phno'],
               'fstore':data['facestorloc'],
               'id':str(data['_id'])
               })
            
            members.append(zx)
      return json.dumps({'suc':name})
   else:
      return json.dumps({'suc':name})
   return json.dumps({'suc':'asdf'})


@app.route('/')
def index():
   membersdel()
   return render_template('index.html')




@app.route('/login',methods=['GET','POST'])
def login():
   membersdel()
   form=loginForm(request.form)
   if request.method == 'POST' and form.validate_on_submit():
      currentuser=usr.find_one({'email':request.form['email']})
      if currentuser:
         if bcrypt.checkpw(request.form['password'].encode('utf-8'),currentuser['password']):
            session['email']=request.form['email']
            session['name']=currentuser['name']
            session['loc']=currentuser['loc']
            session['type']=currentuser['type']
            return redirect('home') 
         else:
            return "wrongpass"
      else:
         return "sorry not registered"
   if('name' in session):
      return redirect('home')
   else:
      return render_template('login.html',form=form)


@app.route('/logout')
def logout():

   membersdel()
   if(session['name']):
      session.clear()
   return redirect('login')

def adminhome():
   x={'usrcount':usr.find().count(),
      'usr':usr.find().sort([("addeddate",-1)]),
      'customer':fr.find().sort([("addeddate",-1)]),
      'custcount':fr.find().count()
      }
   return x


@app.route('/home')
def home():

   membersdel()
   if(session['type']!=0):
      y= adminhome() 
      return render_template('admin/home.html',y=y)
   else:
      return render_template('Manager/home.html')

#manage
@app.route('/admin/manager')
def manager():

   membersdel()
   if('type' in session and session['type']==1):
      manager=usr.find({"type":{'$ne':1}})
      return render_template('admin/Manager/manager.html',manager=manager)
   else:
      return redirect('/')

@app.route('/manager/register',methods=['GET','POST'])
def regman():

   membersdel()
   form = registerformman(request.form)
   if request.method == 'POST' and form.validate_on_submit():
      currentuser=usr.find_one({'email':request.form['email']})
      if currentuser is None:
         hashpas=bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
         usr.insert({
            'name':request.form['name'],
            'email':request.form['email'],
            'password':hashpas,
            'loc':int(request.form['locationid']),
            'type':0,
            'addeddate':time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            })
   elif request.method=='GET':
      return render_template('admin/Manager/add.html',form=form)
   return redirect(url_for('index'))
@app.route('/manager/view/<id>')
def viewcust(id):
   membersdel()
   value=usr.find_one({"_id": ObjectId(id)})
   return  render_template('admin/Manager/view.html',value=value)


#customer
@app.route('/admin/customer')
def admincustomer():
   membersdel()
   if('type' in session and session['type']==1):
      cust=fr.find()
      return render_template('admin/Customer/customer.html',cust=cust)
   else:
      return redirect('/')

@app.route('/customer/view/<id>')
def viewman(id):
   membersdel()
   value=fr.find_one({"_id": ObjectId(id)})
   return  render_template('admin/Customer/view.html',value=value)



#customer register
@app.route('/register')
def register():
   membersdel()
   form = RegistrationForm()
   return render_template('register.html',form=form)

@app.route('/registeruser', methods=['POST'])
def registeruser():
   membersdel()
   phno=request.form['phno']
   email= request.form['email']
   name= request.form['name']
   f = request.files['photo']
   asd=email.split('@')
   
   f.save('/home/praveen/Desktop/python/flask/static/img/img/'+asd[0]+'.jpg')     
   face = face_recognition.load_image_file('static/img/img/'+asd[0]+'.jpg')
   faceencoding=face_recognition.face_encodings(face)[0]
   known_face_encodings.append(faceencoding)
   known_face_name.append(asd[0])
   post_data = {
      'name': name,
      'email': email,
      'phno': phno,
      'imgname':asd[0],
      'facestorloc':'img/img/'+asd[0]+'.jpg',
      'addeddate':time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
   }
   fr.insert_one(post_data)
   np.save('./frimg/'+asd[0],faceencoding)
   return "hi"


if __name__ == '__main__':
   app.run()
# Pyqt5 implementation:
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QMainWindow,QPushButton
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import dbdetails,db
import mysql.connector
import requests, json
import warnings
from requests.exceptions import ConnectionError
import numpy as np
import cv2
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd=r'D:\tesseract\tesseract.exe'

from datetime import datetime
import time
'''MariaDB [library]> select * from login_info
    -> ;
+-----------+-----------+----------+
| name      | username  | password |
+-----------+-----------+----------+
| Biancaa.R | Bia       | biancaa  |
| Biancaa   | bian      | biancaa  |
| Biancaa.R | Biancaa   | biancaa  |
| Biancaa   | Biancaa.R | 123      |
| Biancaa.R | bia_123   | biancaa  |
+-----------+-----------+----------+'''

def custom_excepthook(type, value, traceback):
    # Handle exceptions and warnings here
    # You can display a message or log the issue
    print("Exception or warning occurred:", type, value)


# Install the custom excepthook
sys.excepthook = custom_excepthook

def show_warning():
    warnings.warn("This is a sample warning!")

#Image capturing

import cv2
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input #For etracting features from the images
from tensorflow.keras.preprocessing.image import load_img, img_to_array #for img conversion to array of num
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.sequence import pad_sequences


from tensorflow import keras
model=keras.models.load_model("model1.h5")
vgg_model = VGG16() 
# restructure the model


vgg_model = Model(inputs=vgg_model.inputs,             
                  outputs=vgg_model.layers[-2].output)
#--------------------------------------------------------------
#Removing the final layer alone from the model : transfer learning

import os
base_dir='C:\\Users\\Biancaa. R\\lumin_eye'
#Reading the value of the captions:
with open(os.path.join(base_dir, 'captions.txt'), 'r') as f:
    next(f) #ignoring the first line of data
    captions_doc = f.read()
# Creating a mapping from the image to the captions:

mapping={}

#processing the lines:
for line in (captions_doc.split("\n")):
    tokens=line.split(",")
    #splitting the line available to words
    if len(line)<2:
        continue
        # If the len of line<2 it means the line has no img name,caption parts
    image_id,caption=tokens[0],tokens[1:]
    #As there are multiple caps
    image_id=image_id.split(".")[0]
    #no one wants the extension
    caption=" ".join(caption)
    """Since there are single images with multiple captions we dont want multiple keys with the same image name """
    if image_id not in mapping:
        mapping[image_id]=[]
    mapping[image_id].append(caption)

def clean(mapping):
    for key,captions in mapping.items():
        for i in range(len(captions)): #plural here
            caption=captions[i]
            #taking them 1 at a time
            caption=caption.lower()
            #removing special characters,numbers
            caption=caption.replace('[^A-Za-z]'," ")
            caption=caption.replace("\s+"," ")
            #Removing possible changes
            caption=caption.replace("<start>","")
            caption=caption.replace("<stop>","")
            caption=caption.replace('startseq','')
            caption=caption.replace('endseq','')
            #Adding starts and end tags to the model
            caption='startseq '+" ".join([word for word in caption.split() if len(word)>1]) +' endseq'
            captions[i]=caption
clean(mapping)


all_captions=[]
for key in mapping:
    for caption in mapping[key]:
        all_captions.append(caption)

#tokenizing the text:
tokenizer=Tokenizer()
tokenizer.fit_on_texts(all_captions)
vocab_size=len(tokenizer.word_index)+1
print(vocab_size)

#Finding the maximum length of line in the data for padding in the model
max_length=max(len(caption.split())for caption in all_captions)
print(max_length)

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# generate caption for an image
def predict_caption(model, image, tokenizer, max_length):
    # add start tag for generation process
    in_text = 'startseq'
    # iterate over the max length of sequence
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)#[0]
        # predict next word
        yhat = model.predict([image, sequence], verbose=0)
        # get index with high probability
        yhat = np.argmax(yhat)
        # convert index to word
        word = idx_to_word(yhat, tokenizer)
        # stop if word not found
        if word is None:
            break
        # append word as input for generating next word
        in_text += " " + word
        # stop if we reach end tag
        if word == 'endseq' or word==' endseq':
            break
    return in_text

vgg_model = VGG16() 
# restructure the model
vgg_model = Model(inputs=vgg_model.inputs,             
                  outputs=vgg_model.layers[-2].output)


import time
import pyttsx3



#creating database and new table in mysql 
dbuser, dbpass = dbdetails.execute()
db.exec(dbuser,dbpass)

#Connecting to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = dbuser,            
    password = dbpass,
    database = "envision"
    )
         
cursor = mydb.cursor()
cursor = mydb.cursor(buffered=True)

vid=False
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("welcomescreen.ui",self)
        self.username.setPlaceholderText("Username")
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.sign.clicked.connect(self.gotosignup)
        self.login.clicked.connect(self.gotodash)

    def gotosignup(self):
        signup=SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotodash(self):
        global username
        username = self.username.text()
        password = self.passw.text()

        if len(username)==0 or len(password)==0:
            self.error.setText("Please fill in all fields")
        
        else:
            query = "SELECT password FROM login_info WHERE username = '"+username+"'"
            cursor.execute(query)    
            result_pass = cursor.fetchone()

            if result_pass is not None:
                if result_pass[0] == password:
                    print("Successfully logged in.")
                    dash=DashScreen()
                    widget.addWidget(dash)
                    widget.setCurrentIndex(widget.currentIndex()+1)


                else:
                    self.error.setText("Invalid username or password")
            else:
                self.error.setText("Invalid username or password")
class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen,self).__init__()
        loadUi("signup.ui",self)
        self.signupname.setPlaceholderText("Enter your name")
        self.signupuser.setPlaceholderText("Enter your user name")
        self.signuppass.setPlaceholderText("Enter your password")
        self.confirmpass.setPlaceholderText("confirm your password")

        self.signuppass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.signup2.clicked.connect(self.gotosignup)
        self.backtologin.clicked.connect(self.gotowelcome)

        #self.signup1.setText("user added successfully, please login")

    def gotosignup(self):
        global newname, newuser, newpass
        newname = self.signupname.text()
        newuser = self.signupuser.text()
        newpass1 = self.signuppass.text()
        newpass2 = self.confirmpass.text()

        if len(newname)== 0 or len(newuser) == 0 or len(newpass1) == 0 or len(newpass2) == 0:
            self.signup1.setText("Please fill in all fields")

        elif newpass1 != newpass2:
            self.signup1.setText("The passwords do not match")

        else:
            cursor.execute("SELECT * FROM login_info WHERE username = '"+newuser+"'")
            data = cursor.fetchall()
            if data:
                self.signuperror.setText("Username already exists")
            else:
                addnewquery = "INSERT IGNORE INTO login_info VALUES\
                    ('"+newname+"','"+newuser+"','"+newpass1+"')"
                cursor.execute(addnewquery)
                mydb.commit()
                self.signup1.setText("Added new user to database. Successful! please login")

    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

class DashScreen(QDialog):
    def __init__(self):
        super(DashScreen,self).__init__()
        loadUi("dashboard.ui",self)
        cursor.execute("SELECT name FROM login_info WHERE username = '"+username+"'")
        greetname = cursor.fetchone()[0]
        self.name.setText("Hello "+greetname+"!")

        self.logout.clicked.connect(self.gotowelcome)
        self.new2.clicked.connect(self.gotostoppred)
        self.new1.clicked.connect(self.gotopred)
        self.register2.clicked.connect(self.gotosignup)
        self.rec1.clicked.connect(self.gotorec)
        self.rec2.clicked.connect(self.gotostoprec)
        self.ocr_1.clicked.connect(self.gotoocr)
        self.ocr_2.clicked.connect(self.gotostopocr)
    def gotosignup(self):
        signup=SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotorec(self):
        global vid
        vid=False
        self.label.setText("camera object is started")

        cap = cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)

        fourcc = cv2.VideoWriter_fourcc(*'MP4V') #MP4V codec,
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))

        while(True):
            ret, frame = cap.read()
            out.write(frame)
            cv2.imshow('frame', frame)
            #c = cv2.waitKey(1)
            #if c & 0xFF == ord('q'):
            if cv2.waitKey(1)==ord('q') or vid==True:
                cap.release()
                cv2.destroyAllWindows()
                break
        cap.release()
        out.release() #closes the output video file
        cv2.destroyAllWindows()

    def gotostoprec(self):
            global vid
            self.label.setText("camera object is stopped")
            vid=True
                
    def gotopred(self):
        global vid
        vid=False
        #Making python speak your desired text
        node = pyttsx3.init()#invoke function
        cap = cv2.VideoCapture(0)
        image_path = "C:\\Users\\Biancaa. R\\Downloads\\1.jpg"
        #"C:\Users\Biancaa. R\Downloads\WhatsApp Image 2023-11-09 at 4.02.42 PM.jpeg"
        # load image
        iterations=1
        while True :
            ret, image = cap.read()
            cv2.imshow('Processed Image', image)
            cv2.imwrite(image_path, image)
            #time.sleep(10)
            image = load_img(image_path, target_size=(224, 224))
            # convert image pixels to numpy array
            image = img_to_array(image)
            # reshape data for model
            image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
            # preprocess image from vgg
            image = preprocess_input(image)
            # extract features
            feature = vgg_model.predict(image, verbose=0)
            # predict from the trained model
            value=predict_caption(model, feature, tokenizer, max_length)
            print(value)
            #cv2.imshow('Processed Image', image)
            if(iterations%2==0):
                try:
                    node.say(value)
                    node.runAndWait()
                    node.stop()
                    print("Successful")
                except:
                    print("something went wrong")

            # Break the loop if 'q' is pressed
            iterations+=1
            if cv2.waitKey(1) & 0xFF == ord('q') or vid==True:
                break

            

        # Release the video stream and close all windows
        cap.release()
        cv2.destroyAllWindows()
    def gotostoppred(self):

        global vid
        self.label.setText("camera object is stopped")
        vid=True

    def gotowelcome(self):
        welcome=WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoocr(self):
        out_file = open("output.txt" , "w") 
        out_file.close()
        global vid
        vid=False
        cap = cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)

        out_file = open("output.txt" , "a+")
        while(True):
            
            ret, frame = cap.read()
            scanned_text = pytesseract.image_to_string(frame)
            scanned_text=scanned_text[:-2] #STORES TEXT
            print(scanned_text)
            #OUTPUT DIRECTORY FOR TEXT FILE STORAGE
 
            out_file.write(scanned_text)
            cv2.imshow('frame', frame)
            #c = cv2.waitKey(1)
            #if c & 0xFF == ord('q'):
            if cv2.waitKey(1)==ord('q') and vid==True: 
                break
            
        cap.release()
        cv2.destroyAllWindows()
        out_file.close()
        
    def gotostopocr(self):

        global vid
        self.label.setText("camera object is stopped")
        vid=True






app=QApplication(sys.argv)
welcome=WelcomeScreen()
widget=QStackedWidget()
widget.addWidget(welcome)
#widget.setFixedHeight(800)
#widget.setFixedWidth(1200)
widget.resize(1400, 750)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exitting")


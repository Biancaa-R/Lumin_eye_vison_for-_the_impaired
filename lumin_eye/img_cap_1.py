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

image_path = "C:\\Users\\Biancaa. R\\Downloads\\1.jpg"
#"C:\Users\Biancaa. R\Downloads\WhatsApp Image 2023-11-09 at 4.02.42 PM.jpeg"
# load image
iterations=1
import time
import pyttsx3
#Making python speak your desired text
node = pyttsx3.init()#invoke function
cap = cv2.VideoCapture(0)
while True:
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
    #print(value)
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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close all windows
cap.release()
cv2.destroyAllWindows()

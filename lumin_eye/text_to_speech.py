import pyttsx3
#Making python speak your desired text
node = pyttsx3.init()#invoke function
value=input("Enter your text here")
try:
    node.say(value)
    node.runAndWait()
    node.stop()
    print("Successful")
except:
    print("something went wrong")
import RPi.GPIO as GPIO
import time


s2 = 23
s3 = 24
# for setting up the mode
signal = 25
#output value
NUM_CYCLES = 5


def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")
  
def main_loop():
  temp = 0
  while(True):  

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    # Low low is red
    time.sleep(0.3)
    start = time.time()
    for i in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.BOTH)
    duration = time.time() - start 
    red  = NUM_CYCLES / duration   
   
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for i in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.BOTH)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for i in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.BOTH)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    
    if temp==0:
        print("Place the object")
    if green<red and red>blue:
      print("red")
      temp=1
    elif red<green and green>blue:
      print("green")
      temp=1
    elif green<blue and blue>red:
      print("blue")
      temp=1
    else:
      print("place the object.....")
      temp=0
    #The GPIO.wait_for_edge function is used to block the program's execution until a specified edge is detected 
    #Where it can be set to rising ,falling or both so that the new input is taken only when there is some change..

def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        main_loop()

    except KeyboardInterrupt:
        print("end of program")
        endprogram()
        ''' since both the S0 and S1 inputs of the TCS3200 Color Sensor are connected to +5V, the output frequency is scaled to 100% i.e. the output frequency will be in the range of 500 KHz to 600 KHz.

        As S2 and S3 pins of the TCS3200 Color Sensor are used to select the Photo Diode, they are set in three different combination one after the other to get the RAW data of the Red, Blue and Green values.'''

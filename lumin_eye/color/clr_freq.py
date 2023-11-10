#Program to show the frequency value measured for different colors rgb using colour sensor :
#TCS3200 
#Setting the s2 s3 output is crucial to select the colour of mode in photodiode
# 00 r 01 b 11 g

import RPi.GPIO as GPIO
import time

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")
  
def main_loop():
  temp = 1
  while(1):  

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for i in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz
    print("red value - ",red) #output as frequency
    # total number of iterations/time for change

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for i in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    print("blue value - ",blue)

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for i in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    print("green value - ",green)
    time.sleep(2)  


def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        main_loop()

    except KeyboardInterrupt:
        endprogram()
#values set for s0 and s1
#L	L	Power Down	———-
#L	H	2%	10 – 12 KHz
#H	L	20%	100 – 120 KHz
#H	H	100%	500 – 600 KHz
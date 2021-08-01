from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

# first led (red light)
sleep (1)
GPIO.output(11,1)
sleep (2)
GPIO.output(11,0)
sleep (0.5)

#second led (green light)
for i in range(1):
    GPIO.output(13,1)
    sleep (2)
    GPIO.output(13,0)
    sleep (0.5)
        
#third led (yellow light)
for i in range(1):
    GPIO.output(11,1)
    GPIO.output(13,1)
    sleep (2)
    GPIO.output(11,0)
    GPIO.output(13,0)
    sleep (0.5)   
            

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.annotate_text = "Calculator!"
camera.annotate_text_size = 50
sleep(10)
camera.capture('/home/pi/Desktop/Calculator.jpg')
camera.stop_preview()
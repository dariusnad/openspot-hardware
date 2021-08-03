from threading import Timer
from picamera import PiCamera
from time import sleep
import uuid
import os.path
import paramiko
import requests
from time import sleep
import RPi.GPIO as GPIO


camera = PiCamera()

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        
def light(lightNum):
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)


    if lightNum == 3:
        GPIO.output(11,0)
        GPIO.output(15,0)
        GPIO.output(13,1)
    elif lightNum == 2:
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(11,1)
    elif lightNum == 1:
        GPIO.output(13,0)
        GPIO.output(11,0)
        GPIO.output(15,1)
    else:
        GPIO.output(13,0)
        GPIO.output(11,0)
        GPIO.output(15,0)
            

def camera_pic():
    
    unique_filename = str(uuid.uuid4())
    filename = "%s.jpg" % unique_filename
    final_path = os.path.join('/home/pi/Desktop/CameraPics', filename)

    camera.start_preview()
    sleep(3)
    print ("Taking a Pic")
    camera.capture(final_path)
    camera.stop_preview()
    
    #pictures  = {'myfile': final_path}
    #filename1 = pictures['myfile']
    
    url = 'http://192.168.150.200:8000/cv/'
    files = {'myfile': open(final_path, 'rb')}
    
    #image = open(filename1, 'rb').read()
    res = requests.post(url, files=files)
    # 0 - off, 1 - red, 2 - yellow, 3-green
    
    print(res.json())
    print(type(res))
    lightNum = res.json()['light_colour']
    
    light(lightNum)
    
   # ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   # ssh.connect('192.168.1.76', username = 'gurmeshshergill', password = 'hr634431')
   # sftp = ssh.open_sftp()
    
    
   # sftp.put(final_path, os.path.join('/Users/gurmeshshergill/desktop/Rasp', filename))
   # sftp.close()
   # ssh.close()
   
    

#print ("Smile")
rt = RepeatedTimer(5, camera_pic) # it auto-starts, no need of rt.start()
try:
    sleep(10) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
    


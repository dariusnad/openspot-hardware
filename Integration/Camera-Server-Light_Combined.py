from threading import Timer
from picamera import PiCamera
from time import sleep
import uuid
import os.path
import requests
from time import sleep
import RPi.GPIO as GPIO
import array
import sys

from ola.ClientWrapper import ClientWrapper

#camera = PiCamera()

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

    #data = array.array('B', [0, 0, 0])
    universe = 1

    if lightNum == 3:
        data = array.array('B', [0, 255, 0])
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.SendDmx(universe, data)
        wrapper.Run()
    elif lightNum == 2:
        data = array.array('B', [255, 90, 0, 0])
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.SendDmx(universe, data)
        wrapper.Run()
    elif lightNum == 1:
        data = array.array('B', [255, 0, 0, 0])
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.SendDmx(universe, data)
        wrapper.Run()
    elif lightnum == 4:
        data = array.array('B', [0, 0, 255, 0])
        wrapper = ClientWrapper()
        client = wrapper.Client()
        client.SendDmx(universe, data)
        wrapper.Run()            

def camera_pic():
    
    unique_filename = str(uuid.uuid4())
    #filename = "%s.jpg" % unique_filename
    filename = "download3.jpg" 
    final_path = os.path.join('/home/pi/Desktop/CameraPics', filename)

    #camera.resolution = (2592, 1944)
    #camera.framerate = 15

    #camera.start_preview()
    #sleep(3)
    #print ("Taking a Picture")
    #camera.capture(final_path)
    #camera.stop_preview()
    
    
    #url = 'http://192.168.150.200:8000/cv/'
    url = 'http://10.0.0.120:8080/cv/'
    files = {'myfile': open(final_path, 'rb')}
    modInfo = {"modNum" : 0, "parkingLotName": "Kensington"}
    
    res = requests.post(url, files=files, data=modInfo )
    # 0 - off, 1 - red, 2 - yellow, 3-green
    
    print(res.json())
    print(type(res))
    lightNum = res.json()['light_colour']
    
    light(lightNum)
    

#print ("Smile")
rt = RepeatedTimer(5, camera_pic) # it auto-starts, no need of rt.start()
try:
    sleep(5) # your long-running job goes here...
    #continue
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
    


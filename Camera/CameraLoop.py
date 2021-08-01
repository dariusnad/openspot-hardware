from threading import Timer
from picamera import PiCamera
from time import sleep
import uuid
import os.path
import paramiko

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



def camera_pic():
    
    unique_filename = str(uuid.uuid4())
    filename = "%s.jpg" % unique_filename
    final_path = os.path.join('/home/pi/Desktop/CameraPics', filename)

    camera.start_preview()
    sleep(3)
    print ("Taking a Pic")
    camera.capture(final_path)
    camera.stop_preview()
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.76', username = 'gurmeshshergill', password = 'hr634431')
    sftp = ssh.open_sftp()
    
    
    sftp.put(final_path, os.path.join('/Users/gurmeshshergill/desktop/Rasp', filename))
    sftp.close()
    ssh.close()
   
    

#print ("Smile")
rt = RepeatedTimer(5, camera_pic) # it auto-starts, no need of rt.start()
try:
    sleep(20) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
    
from threading import Timer
from picamera import PiCamera
from time import sleep
import uuid
import os.path
import requests
from time import sleep
import RPi.GPIO as GPIO
import array
import threading
import sys
#microphone
import pyaudio
import wave


from ola.ClientWrapper import ClientWrapper

camera = PiCamera()
j = 0   
    
def light(lightNum):

    def DMXSent(state):
        wrapper.Stop()
    #data = array.array('B', [0, 0, 0])
    universe = 1
    wrapper = ClientWrapper()
    client = wrapper.Client()
    if lightNum == 3:
        data = array.array('B', [0, 255, 0])
        client.SendDmx(universe, data,DMXSent)
        wrapper.Run()
    elif lightNum == 2:
        data = array.array('B', [255, 90, 0, 0])
        print("Sending light data")
        client.SendDmx(universe, data,DMXSent)
        print("Sent light data")
        wrapper.Run()
        print("Done Running")
    elif lightNum == 1:
        data = array.array('B', [255, 0, 0, 0])
        print("Sending light data")
        client.SendDmx(universe, data,DMXSent)
        print("Sent light data")
        wrapper.Run()
        print("Done Running")
    elif lightNum == 4:
        i = 0
        print("In lightNum==4")
        while (i != 40000):
            print("Send Blue")
            data = array.array('B', [10, 50, 255])
            client.SendDmx(universe, data, DMXSent)
            wrapper.Run()
            data2 = array.array('B', [0, 0, 0])
            print("Send white")
            client.SendDmx(universe, data2, DMXSent)
            wrapper.Run()
            i += 1
            
        print("DONE LOOP")
       
def microphone():
    print ("Inside microphone")
    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 30 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'test1.mp3' # name of .wav file

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)
    print("recording")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    
    #AudioSegment.from_wav
    #url = 'http://10.0.0.120:8080/audio_rec/'
    url = 'http://34.105.43.250:8000/audio_rec/'
    files = {'myfile': open(wav_output_filename, 'rb')}
    modInfo = {"modNum" : 0, "parkingLotName": "test"}
        
    res = requests.post(url, files=files, data=modInfo)
    lightNum = res.json()['light_colour']
    print(res.json())
    print(type(res))
    light(lightNum)
    

def camera_pic():
    print("Inside camera pic function")
    #threading.Timer(50, camera_pic).start()
    
    unique_filename = str(uuid.uuid4())
    
    filename = "%s.jpg" % unique_filename
   # if (j == 0):
   #     filename = "2car.jpg"
   # elif (j == 1):
   #     filename = "3car.jpg"
    #else:
   #     filename = "5car.jpg"
        
    #final_path = os.path.join('/home/pi/Desktop/CameraPics', filename)
    #camera.resolution = (2592, 1944)
    #camera.framerate = 15
    #camera.exposure_mode = 'night'
    #camera.brightness = 60
    #camera.start_preview()
    #sleep(10)

    camera.capture(final_path)
    camera.stop_preview()
    
    #url = 'http://192.168.150.200:8000/cv/'
    #url = 'http://10.0.0.120:8080/cv/'
    url = 'http://34.105.43.250:8000/cv/'
    files = {'myfile': open(final_path, 'rb')}
    modInfo = {"modNum" : 0, "parkingLotName": "test"}
    
    res = requests.post(url, files=files, data=modInfo)
    print("Done waiting")
    
    # 0 - off, 1 - red, 2 - yellow, 3-green
    
    print(res.json())
    print(type(res))
    lightNum = res.json()['light_colour']
    
    print("Calling the light function")
    light(lightNum)
    print("Light function called")
    microphone()
    print("Microphone function called")

while True:
    #camera_pic(j)
    camera_pic()
    #j += 1
    sleep(5)



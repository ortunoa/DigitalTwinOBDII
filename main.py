#Import Python modules
import time
import json
import RPi.GPIO as GPIO
import os

script_dir = os.path.dirname(os.path.abspath("main.py"))
config_file_path = os.path.join(script_dir, "config.json")

#Import custom packages

from Utilities.Obd2 import getObd2Data
from Utilities.Setup import channels, dummyGyroscopeRecord, dummyObdData

#Load configuration
with open(config_file_path, 'r') as f:
    # Load the contents of the file as a dictionary..
    programConfig = json.load(f)
    
    
#Initialize LEDs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT, initial=GPIO.LOW) #red
GPIO.setup(35, GPIO.OUT, initial=GPIO.LOW) #green
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW) #blue
    

#Initialize text file
timestampForTextfile = str(time.time()).split('.')[0]
textFile = open(r"DATA/{}.txt".format(timestampForTextfile), "a") # "a" means we want to append to the file


if programConfig["Platform"] == "RPi":
    from Utilities.Gyroscope import getGyroscopeData

serialAddress = programConfig['SerialAddress']

i = 0
GPIO.output(35, GPIO.HIGH) #set power green light on

while True: 
    GPIO.output(37, GPIO.HIGH) #set activity blue light on
    thisRecord = {}

    timestamp = time.time()

    try:
        obdRecord = {"ObdData":getObd2Data(channels)}
    except:
        obdRecord = {"ObdData":dummyObdData}

    if programConfig["Platform"] == "RPi":
        gyroscopeRecord = {"GyroscopeData":getGyroscopeData()}
    else: 
        gyroscopeRecord = {"GyroscopeData":dummyGyroscopeRecord}
    

    thisRecord.update(obdRecord)
    thisRecord.update(gyroscopeRecord)

    print(thisRecord)
    textFile.write('{}\n'.format(thisRecord))
    
    

    i+=1
    if i > programConfig["LineLimit"]:
        i=0
        timestampForTextfile = str(time.time()).split('.')[0]
        textFile = open(r"DATA/{}.txt".format(timestampForTextfile), "a") # "a" means we want to append to the file

  
    time.sleep(0.1)
    GPIO.output(37, GPIO.LOW) #set activity blue light off
    time.sleep(0.9)
    print(i)


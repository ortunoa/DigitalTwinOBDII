#Import Python modules
import time
import json

#Import custom packages

from Utilities.Obd2 import getObd2Data
from Utilities.Setup import channels, dummyGyroscopeRecord, dummyObdData

#Load configuration
with open('config.json', 'r') as f:
    # Load the contents of the file as a dictionary
    programConfig = json.load(f)


#Initialize text file
timestampForTextfile = str(time.time()).split('.')[0]
textFile = open(r"DATA/{}.txt".format(timestampForTextfile), "a") # "a" means we want to append to the file


if programConfig["Platform"] == "RPi":
    from Utilities.Gyroscope import getGyroscopeData

serialAddress = programConfig['SerialAddress']

while True: 
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

    time.sleep(1)


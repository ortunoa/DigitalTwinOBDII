#Import Python modules
import time

#Import custom packages
from Utilities.Gyroscope import getGyroscopeData
from Utilities.Obd2 import
from Utilities.Config import programConfig, channels

serialAddress = programConfig['SerialAddress']

while True: 
    finalRecord = {}

    timestamp = time.time()

    if programConfig["Platform"] == "RPi":
        finalRecord.update(getGyroscopeData())

    finalRecord.update(getObd2Data(channels, serialAddress))

    print(finalRecord)

    time.sleep(1)


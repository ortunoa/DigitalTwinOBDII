#Import Python modules
import time

#Import custom packages

from Utilities.Obd2 import getObd2Data
from Utilities.Config import programConfig, channels

if programConfig["Platform"] == "RPi":
    from Utilities.Gyroscope import getGyroscopeData

serialAddress = programConfig['SerialAddress']

while True: 
    finalRecord = {}

    timestamp = time.time()

    if programConfig["Platform"] == "RPi":
        finalRecord.update(getGyroscopeData())

    record = getObd2Data(channels)

    print(record)

    time.sleep(1)


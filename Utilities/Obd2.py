#Imprort dependencies
import obd
import time
from .config import channels

#This function returns an OBD connection to be used by the main getObd2Data function
def getSerialConnection(serialAddress):
    return obd.OBD(serialAddress)


#This is the function that the main loop calls to get serial data every loop iteration
def getObd2Data(channels, serialAddress):
    
    connection = getSerialConnection(serialAddress)

    obd2Record = {}

    #Loop over the channel names in the imported dictionary
    for channelName in channels.keys():
        try:
            cmd = channels[channelName]
            response = connection.query(cmd)   

            #Build record dict per channel     
            channelRecord = {'Timestamp': timestamp,
                        'ChannelName':channelName,
                        'Value': float(str(response).split(' ')[0]),
                        'Units': str(response).split(' ')[1],
                        'Cmd':str(cmd).split(': ')[1]}

            obd2Record.update(channelRecord)
        except:
            print('{} is not supported'.format(channelName))

    return obd2Record



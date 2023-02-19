#Imprort dependencies
import obd
import json
import time

with open('config.json', 'r') as f:
    # Load the contents of the file as a dictionary
    programConfig = json.load(f)


#This function returns an OBD connection to be used by the main getObd2Data function
def getSerialConnection(serialAddress):
    return obd.OBD(serialAddress)


connection = getSerialConnection(programConfig["SerialAddress"])

#This is the function that the main loop calls to get serial data every loop iteration
def getObd2Data(channels):

    obd2Record = []

    #Loop over the channel names in the imported dictionary
    for channelName in channels.keys():
        try:
            cmd = channels[channelName]
            response = connection.query(cmd)   

            timestamp = time.time()

            #Build record dict per channel     
            channelRecord = {'Timestamp': timestamp,
                        'ChannelName':channelName,
                        'Value': float(str(response).split(' ')[0]),
                        'Units': str(response).split(' ')[1],
                        'Cmd':str(cmd).split(': ')[1]}

            obd2Record.append(channelRecord)
        except Exception as e:
            pass
            # print('{} is not supported'.format(channelName))
            # print(e)

    return obd2Record



#Imprort dependencies
import obd
import time
from .config import channels

#This will need to get automated, for now I know that on my laptop it's going on CON6
connection = obd.OBD("COM6")

#Main while loop
while True:
    timestamp = time.time()
    
    for channelName in channels.keys():
        try:
            cmd = channels[channelName]
            response = connection.query(cmd)        
            record = {'Timestamp': timestamp,
                      'ChannelName':channelName,
                      'Value': float(str(response).split(' ')[0]),
                      'Units': str(response).split(' ')[1],
                      'Cmd':str(cmd).split(': ')[1]}

            print(record)
        except:
            print('{} is not supported'.format(channelName))


    time.sleep(1)



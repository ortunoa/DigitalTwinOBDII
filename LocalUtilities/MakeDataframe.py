import pandas as pd
import json
import datetime

def makeDataframe(dataList):
    df = pd.DataFrame()
    i = 0
    for dataStr in dataList:
        try:
            dataDict = json.loads(dataStr.replace("'", "\""))
            dfo = pd.DataFrame.from_dict(dataDict['ObdData'])[['Timestamp','ChannelName','Value']]
    #         dfo['Timestamp'] = dfo['Timestamp'].apply(lambda x:int(str(x).split('.')[0]))
    #         dfo['Timestamp'] = dfo['Timestamp'].iloc[-1]
            dfo['DateTime'] = dfo['Timestamp'].apply(lambda x:datetime.datetime.fromtimestamp(x))
            dfo = dfo.pivot(index='Timestamp',columns='ChannelName',values='Value')
            dfg = pd.DataFrame(dataDict['GyroscopeData'], index=[0])
            for c in dfg.columns:
                dfo[c] = dfg[c].iloc[0]
    #         print(dfo.shape)
            dfo.reset_index(inplace=True)
            df = df.append(dfo)
            i+=1
    #         print(i)
        except Exception as e:
            i+=1
#             print('Failed with: {}'.format(i))
#             print(e)
        
    df = df.groupby(['Timestamp']).mean().ffill()
    df.reset_index(inplace=True)
    
    df['Datetime'] = df['Timestamp'].apply(lambda x:datetime.datetime.fromtimestamp(x))
    df.set_index('Datetime', inplace=True)
    df = df.resample('1S').mean()
    df.ffill(inplace=True)
    df.dropna(inplace=True)
    
    return df
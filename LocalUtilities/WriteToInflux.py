import os
import json
import requests

INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN')
MEASUREMENT = 'telemetry'
url = "http://localhost:8086/api/v2/write"

params = {
    "org": "localinflux",
    "bucket": "digitaltwin",
    "precision": "s"
}

headers = {
    "Content-Type": "text/plain",
    "Authorization": "Token {}".format(INFLUX_TOKEN)
}


vehicles = [
    {'id':'1', 'make':'toyota', 'model':'rav4', 'year': '2022'},
    {'id':'2', 'make':'volkswagen', 'model':'tiguan', 'year': '2021'},
    {'id':'3', 'make':'kia', 'model':'optima', 'year': '2015'},
]

def avgTimestamp(timestampList):
    try:
        return int(sum(timestampList) / len(timestampList))
    except:
        pass 

def getInfluxPayload(ID, make, model, year, dataList):
    influxPayload = ''
    for i in range(len(dataList)-1):
        try:
            dataStr = dataList[i]
            dataDict = json.loads(dataStr.replace("'", "\""))

            influxPayload = influxPayload + createInfluxEntry(ID, make, model, year, dataDict)

        except Exception as e: 
            print(e)
            
    return influxPayload

def createInfluxEntry(ID, make, model, year, dataDict):
    header = '{},id={},make={},model={},year={} '.format('telemetry', ID, make, model, year)
    s = ''
    for k in list(dataDict.keys()):
        if k == 'ObdData':
            for d in dataDict[k]:
                s+= "{}={},".format(d['ChannelName'],d['Value'])
        elif k == 'GyroscopeData':
            for gk in list(dataDict[k]):
                s+= "{}={},".format(gk, dataDict[k][gk])

    s = s[:-1]
    ts = avgTimestamp([j['Timestamp'] for j in dataDict['ObdData']])

    s += ' {}\n'.format(ts)

    finalString = header + s

    return finalString


def writeToInflux(influxPayload):
    response = requests.post(url, params=params, headers=headers, data=influxPayload)
    
    if response.ok:
        print('Succesfully written records to Influx!')
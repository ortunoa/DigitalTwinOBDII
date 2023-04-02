import pandas as pd
import datetime
import requests
import os
import time

def makeLineProtocol(engineLoad, airFlow, rpm, speed, throttle, ay):
    baseString = "telemetry,id=1,make=toyota,model=rav4,year=2022 EngineLoad={},AirFlowRate={},RPM={},Speed={},ThrottlePosition={},Ay={} {}"
    now = datetime.datetime.now()
    timestamp = int(now.timestamp())
    return baseString.format(engineLoad, airFlow, rpm, speed, throttle, ay, timestamp)

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


df = pd.read_csv('dataToWrite.csv')
df = df[['EngineLoad','AirFlowRate','RPM','Speed','ThrottlePosition','Ay']]

for i in range(df.shape[0]):  
    engineLoad = df.iloc[i]['EngineLoad']
    airFlow = df.iloc[i]['AirFlowRate']
    rpm = df.iloc[i]['RPM']
    speed = df.iloc[i]['Speed']
    throttle = df.iloc[i]['ThrottlePosition']
    ay = df.iloc[i]['Ay']
    
    payload = makeLineProtocol(engineLoad, airFlow, rpm, speed, throttle, ay)
    response = requests.post(url, params=params, headers=headers, data=payload)
    # print(payload)
    print('Wrote record {}/{}    -    {}'.format(i, df.shape[0], response.status_code))
    time.sleep(1)
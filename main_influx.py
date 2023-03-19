import os
import warnings

from LocalUtilities.WriteToInflux import vehicles, createInfluxEntry, getInfluxPayload,writeToInflux
warnings.filterwarnings('ignore')

rootPath = r"C:\Users\ortun\OneDrive\PURDUE\CLASSES\ECE695\PROJECT\CODE\DATA"
MEASUREMENT = 'telemetry'

j = 0

ID = vehicles[j]['id']
make = vehicles[j]['make']
model = vehicles[j]['model']
year = vehicles[j]['year']

header = '{},id={},make={},model={},year={} '.format(MEASUREMENT, ID, make, model, year)

path = "{}\{} {} {}".format(rootPath, make, model, year)
files = os.listdir(path)

for i in range(len(files)):
    with open(path + '\{}'.format(files[i]), 'r') as myFile:
        dataList = myFile.read().split('\n')
        influxPayload = getInfluxPayload(ID, make, model, year, dataList)
        try:
            writeToInflux(influxPayload)
        except:
            pass
from Utilities.InfluxToolkit import queryInflux, plotCorrelationMatrix, trainModel
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid

cred = credentials.Certificate("digitaltwinobdii-firebase-adminsdk-dob8j-cbf5404441.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://digitaltwinobdii-default-rtdb.firebaseio.com/'
})

model_id =  str(uuid.uuid4()).upper()

def write_data(path, data):
    ref = db.reference(path)
    ref.set(data)
    print(f"Data saved at path '{path}': {data}")

startDate = '2023-01-01'
endDate = '2023-04-01'
vehicle_id = "1"
vehicle_make = "Toyota"
vehicle_model = "Rav4"
vehicle_year = "2022"
tags = ['EngineLoad','AirFlowRate','RPM', 'Speed', 'ThrottlePosition','Ay']

vehicle_identifiers = {
    "Id":vehicle_id,
    "Make":vehicle_make, 
    "Model":vehicle_model,
    "Year":vehicle_year
}

df = queryInflux(startDate, endDate, vehicle_id, tags)

# plotCorrelationMatrix(df)

model = trainModel(df)
model['Identifiers'] = vehicle_identifiers
model['DateTime'] = str(datetime.datetime.now())


path = "digitalTwinModels/{}".format(model_id)

write_data(path, model)
print('Model succesfully written to Firebase!')


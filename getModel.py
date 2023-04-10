import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

vehicle_id = '1'
website_config_path = "C:\Users\ortun\OneDrive\PURDUE\CLASSES\ECE695\PROJECT\CODE\digitalTwinFrontEnd\vehicle-telematics-dashboard\src\config.json"

cred = credentials.Certificate("digitaltwinobdii-firebase-adminsdk-dob8j-cbf5404441.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://digitaltwinobdii-default-rtdb.firebaseio.com/'
})

def get_latest_model_with_highest_r2(vehicle_id):
    ref = db.reference('digitalTwinModels')
    query = ref.order_by_child('Identifiers/Id').equal_to(vehicle_id)
    result = query.get()

    if result:
        latest_model_key, latest_model_data = max(result.items(), key=lambda x: (x[1]['DateTime'], x[1]['Scores']['R2']))
        print(f"Latest model with the highest R2 score for vehicle ID '{vehicle_id}':\n{latest_model_data}")
        return latest_model_data
    else:
        print(f"No model found for vehicle ID '{vehicle_id}'")
        return None
    

model = get_latest_model_with_highest_r2(vehicle_id)

print(model)
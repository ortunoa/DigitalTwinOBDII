import obd

channels = {
    'RPM':obd.commands.RPM,
    'Speed':obd.commands.SPEED,
    'EngineLoad':obd.commands.ENGINE_LOAD,
    'CoolantTemp':obd.commands.COOLANT_TEMP,
    'IntakeTemp':obd.commands.INTAKE_TEMP,
    'FuelLevel':obd.commands.FUEL_LEVEL,
    'AmbientTemp':obd.commands.AMBIANT_AIR_TEMP,
    'EngineOilTemp':obd.commands.OIL_TEMP,
    'ThrottlePosition':obd.commands.THROTTLE_POS,
    'Airflowrate':obd.commands.MAF
    # 'FuelRate':obd.commands.FUEL_RATE,
    
#     'FuelInjectorTiming':obd.commands.DTC_FUEL_INJECT_TIMING,
#     'FuelInjectorTiming':obd.commands.FUEL_INJECT_TIMING,
#     'FuelRate':obd.commands.FUEL_RATE,
#     'FuelPressure':obd.commands.FUEL_PRESSURE
}


dummyGyroscopeRecord = {
    "Ax":0,
    "Ay":0,
    "Az":0,
    "Gx":0,
    "Gy":0,
    "Gz":0
}

dummyObdData = [{'Timestamp': 1676751191.0242572, 'ChannelName': 'RPM', 'Value': 704.5, 'Units': 'revolutions_per_minute', 'Cmd': 'Engine RPM'}, {'Timestamp': 1676751191.0410995, 'ChannelName': 'Speed', 'Value': 0.0, 'Units': 'kph', 'Cmd': 'Vehicle Speed'}, {'Timestamp': 1676751191.0533361, 'ChannelName': 'EngineLoad', 'Value': 18.431372549019606, 'Units': 'percent', 'Cmd': 'Calculated Engine Load'}, {'Timestamp': 1676751191.0730417, 'ChannelName': 'CoolantTemp', 'Value': 67.0, 'Units': 'degC', 'Cmd': 'Engine Coolant Temperature'}, {'Timestamp': 1676751191.0876324, 'ChannelName': 'IntakeTemp', 'Value': 20.0, 'Units': 'degC', 'Cmd': 'Intake Air Temp'}, {'Timestamp': 1676751191.1033802, 'ChannelName': 'FuelLevel', 'Value': 66.27450980392157, 'Units': 'percent', 'Cmd': 'Fuel Level Input'}, {'Timestamp': 1676751191.116859, 'ChannelName': 'AmbientTemp', 'Value': 20.0, 'Units': 'degC', 'Cmd': 'Ambient air temperature'}, {'Timestamp': 1676751191.1360648, 'ChannelName': 'EngineOilTemp', 'Value': 51.0, 'Units': 'degC', 'Cmd': 'Engine oil temperature'}]



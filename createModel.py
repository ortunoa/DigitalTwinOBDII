from Utilities.InfluxToolkit import queryInflux, plotCorrelationMatrix, trainModel

startDate = '2023-01-01'
endDate = '2023-04-01'
vehicle_id = "1"
tags = ['EngineLoad','AirFlowRate','RPM', 'Speed', 'ThrottlePosition','Ay']


df = queryInflux(startDate, endDate, vehicle_id, tags)

plotCorrelationMatrix(df)

model = trainModel(df)

print(model)
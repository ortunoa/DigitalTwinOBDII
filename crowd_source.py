from Utilities.InfluxToolkit import queryInflux, plotCorrelationMatrix, trainModel
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

startDate = '2023-04-23'
endDate = '2023-04-24'
vehicle_ids = ["1","2"]
#vehicle_ids = ["0", "1", "2", "3"]
tags = ['EngineLoad']

# Query data for each vehicle ID
vehicle_data = {}
for vehicle_id in vehicle_ids:
    try:
        vehicle_data[vehicle_id] = queryInflux(startDate,endDate,vehicle_id, tags)
    except:
        print(f"No available data for vehicle {vehicle_id} in the date range.")
        exit()
    

# Create a plot of engine load data for each vehicle
fig, ax = plt.subplots()
for vehicle_id, data in vehicle_data.items():
    ax.plot(data.index, data['EngineLoad'], label=f"Vehicle {vehicle_id}")

# Set x-axis formatter and locator
date_fmt = '%m-%d-%Y'
months = mdates.MonthLocator()
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(DateFormatter(date_fmt))


# Calculate average and standard deviation of engine load data for all vehicles
average_engine_load = {}
std_engine_load = {}
for vehicle_id, data in vehicle_data.items():
    average_engine_load[vehicle_id] = data['EngineLoad'].mean()
    std_engine_load[vehicle_id] = data['EngineLoad'].std()

# Print average and standard deviation of engine load data for all vehicles
print("Average engine load for each vehicle:")
for vehicle_id, avg in average_engine_load.items():
    print(f"Vehicle {vehicle_id}: {avg:.2f}")
print("\nStandard deviation of engine load for each vehicle:")
for vehicle_id, std in std_engine_load.items():
    print(f"Vehicle {vehicle_id}: {std:.2f}")

# Create a list of labels for the legend, including the vehicle ID and average engine load
legend_labels = []
for vehicle_id in vehicle_ids:
    legend_labels.append(f"Vehicle {vehicle_id} (avg.: {average_engine_load[vehicle_id]:.2f}) (stdev.: {std_engine_load[vehicle_id]:.2f})")


# Add axis labels and legend
ax.set_xlabel('Timestamp')
ax.set_ylabel('Engine Load')
#ax.legend()
ax.legend(labels=legend_labels, fontsize=8)
ax.set_title('Engine Load Comparison')

# Add average and standard deviation of engine load data for all vehicles to the plot
ax.axhline(y=sum(average_engine_load.values()) / len(average_engine_load), linestyle='--', color='black', label='Average')
ax.axhspan((sum(average_engine_load.values()) - sum(std_engine_load.values())) / len(average_engine_load), 
           (sum(average_engine_load.values()) + sum(std_engine_load.values())) / len(average_engine_load),
           alpha=0.2, color='grey', label='Standard deviation')

# Show the plot
plt.show()
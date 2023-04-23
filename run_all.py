import subprocess

# List of Python scripts to run
script_names = ["main_influx.py", "createModel.py", "getModel.py","updateWebsiteModel.py"]

# Loop through the list of script names and run each one using subprocess
for script_name in script_names:
    subprocess.run(["python", script_name])
    print('Completed: ', script_name)

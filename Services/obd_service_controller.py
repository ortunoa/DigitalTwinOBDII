import RPi.GPIO as GPIO
import time
import systemd

# Set the mode of the GPIO library to use Broadcom SOC channel numbers
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin number to read from
pin_number = 18

# Set up the GPIO pin as an input
GPIO.setup(pin_number, GPIO.IN)

def start_service(service_name):
    systemd.manager.Manager().start_unit(service_name, 'replace')

def stop_service(service_name):
    systemd.manager.Manager().stop_unit(service_name, 'replace')

def restart_service(service_name):
    stop_service(service_name)
    start_service(service_name)

while(True):
    # Read the current state of the GPIO pin
    pin_state = GPIO.input(pin_number)

    if pin_state:
        print("Setting WLAN")
        # Enter function calls here to start services for WLAN setup
    elif not pin_state:
        print("Cloud Sync")
        # Enter function calls here to revert and stop WLAN
    
    # Runs every second, but can be chnaged to go faster/slower
    time.sleep(1)

# Clean up the GPIO library
GPIO.cleanup()

import RPi.GPIO as GPIO
import time
import systemd
import os
import subprocess

# Set the mode of the GPIO library to use Broadcom SOC channel numbers
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin number to read from
pin_number = 18 #physically pin 12

# Set up the GPIO pin as an input
GPIO.setup(pin_number, GPIO.IN)

def start_service(service_name):
    systemd.manager.Manager().start_unit(service_name, 'replace')

def stop_service(service_name):
    systemd.manager.Manager().stop_unit(service_name, 'replace')

def restart_service(service_name):
    stop_service(service_name)
    start_service(service_name)

def unmask_service(service_name):
    systemd.mask(service_name, mask=False)

def enable_service(service_name):
    systemd.Manager.enable(service_name)

currentUser = os.getlogin()
while(True):
    # Read the current state of the GPIO pin
    pin_state = GPIO.input(pin_number)

    if pin_state:
        print("Setting WLAN")
        # Enter function calls here to start services for WLAN setup
        #stop all services in case of switching from cloud sync and have to change files
        services = {'dhcpcd','dnsmasq','hostapd'}
        # turn off DHCPCD
        try:
            for service in services:
                stop_service(service)
        
            # swap DHCPCD conf file
            os.rename('etc/dhcpcd.conf','etc/dhcpcd-wlanOn.conf')
            os.rename('etc/dhcpcd-wlanOff.conf','etc/dhcpcd.conf')
            
            # restart dhcpcd
            start_service('dhcpcd')
            #unmask, enable, start hostapd
            unmask_service('hostapd')
            enable_service('hostapd')
            start_service('hostapd')
            start_service('dnsmasq')

            #start apache -> website will be linked via build inside the server
            start_service('apache2')
        except Exception as err:
            print(err)
            

    elif not pin_state:
        print("Cloud Sync")
        # Enter function calls here to revert and stop WLAN
        services = {'dhcpcd','dnsmasq','hostapd'}
    
        try:

            for service in services:
                stop_service(service)
            os.rename('etc/dhcpcd.conf','etc/dhcpcd-wlanOff.conf')
            os.rename('etc/dhcpcd-wlanOn.conf','etc/dhcpcd.conf')

            #restart dhcpcd to get WiFi Connectivity
            start_service('dhcpcd')

            #force connection to specific wifi?
        
        except Exception as err:
            print(err)
    
    # Runs every second, but can be chnaged to go faster/slower
    time.sleep(1)

# Clean up the GPIO library
GPIO.cleanup()

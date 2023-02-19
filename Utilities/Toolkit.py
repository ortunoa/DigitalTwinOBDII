from serial.tools import list_ports

def getPortName():
    ports = list(set([item for item in list_ports.comports()]))
    for port in ports:
        if port.manufacturer == 'FTDI':
            return str(port.device)
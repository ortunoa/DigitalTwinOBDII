from serial.tools import list_ports
import obd

def getPortName():
    ports = list(set([item for item in list_ports.comports()]))
    ports = [str(x.name) for x in ports]
    
    for port in ports:
        connection = obd.OBD(port)
        if "ELM327" in str(connection.interface):
            return port
import nidaqmx
from nidaqmx.constants import ExcitationSource, ForceUnits, TerminalConfiguration
import matplotlib.pyplot as plt
import socket
import time
import sys
import csv
import os

#print(item, sep=' ', end='', flush=True) to print dynamically

#You will have to change to the correct working directory, this was just mine
os.chdir(r"C:\Users\Claudia\Documents\LBNL_Working\DILLON MACHINE")

#create an INET, STREAMing socket (IPv4, TCP/IP)
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('Socket Created')

#Connect the socket object to the robot using IP address (str) and port (int)

HOST= "192.168.10.30"
PORT = 5002
delayTime = 0.5

#Connect the socket object to the robot using IP address (string) and port (int)
client.connect((HOST,PORT))

print('Socket Connected to ' + HOST)
# #Read the response sent by robot upon connecting
# msg = client.recv(1024).decode('ascii')
# print(msg)

#Send cmd to Activate the robot
cmd = 'TNT:' #can also try \n
# Add ASCII NULL character at the end of the cmd string
try:
    client.send(bytes((cmd), 'ascii')) #is this the correct way to do it?
    msg = client.recv(1024).decode('ascii')
    print(msg)
    
except Exception as e:
    print('Failed to send data')
    print(e)

#Automatically loops through configuration file
with open(r"DILLON_CONFIG.csv", 'r') as f:
    mycsv = csv.reader(f)
    for row in mycsv:
        text = row[0]
        client.send(bytes((text), 'ascii')) #Check if this works
        time.sleep(delayTime) #Wait between line sends

#Create DAQ task channel
task = nidaqmx.Task()
ai_channel = task.ai_channels.add_ai_voltage_chan_with_excit("Dev2/ai0",
name_to_assign_to_channel= "Load Cell", 
terminal_config= TerminalConfiguration.DIFFERENTIAL,
voltage_excit_source= ExcitationSource.EXTERNAL,
voltage_excit_val= 10.0)

# task.read()
# data = task.read(number_of_samples_per_channel = 1)
loadLimit = 0.12

while True:
    
    try:
        newCommand = input('Type Command: ')

        client.send(bytes((newCommand), 'ascii'))
        newMsg = client.recv(1024).decode('ascii')
        print(newMsg)
        print(data)

        #Breaks the loop if a kill command is issuedV0.1:
        if newCommand == '!K:':
            print('Kill motor command sent, ending program...')
            client.shutdown(1)
            client.close()
            break
        elif newCommand == 'GO1:':
            while True:
                #task.read()
                data = task.read(number_of_samples_per_channel = 1)
                if data[0] >= loadLimit:
                    print('Load Cell limit exceeding, shutting down motor...')
                    client.send(bytes(('!K:'), 'ascii'))
                    print('Load Cell reading: ', data[0])

                time.sleep(delayTime)  

    except Exception as e:
        print(e)

task.stop()
task.close()
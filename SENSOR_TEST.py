#Author: Claudia Bird

import nidaqmx
from nidaqmx.constants import ExcitationSource, ForceUnits, TerminalConfiguration
import matplotlib.pyplot as plt
import os

os.chdir(r'C:\Users\Claudia\Documents\LBNL_Working\DILLON MACHINE')

#Enables interactive mode, such that plot doesn't close btwn sets
#This also shows figures automatically
plt.ion() 

i = 0

with nidaqmx.Task() as task:

    print('Load Cell Sensor Test ')

    ai_channel = task.ai_channels.add_ai_voltage_chan_with_excit("Dev2/ai0",
    name_to_assign_to_channel= "Load Cell", 
    terminal_config= TerminalConfiguration.DIFFERENTIAL,
    voltage_excit_source= ExcitationSource.EXTERNAL,
    voltage_excit_val= 10.0)

    task.read()
    
    while i < 100:
     data = task.read(number_of_samples_per_channel = 1)
     lbV_scale = 2959
     scaledData = (lbV_scale)*(data[0])
     plt.scatter(i, (2959*data[0]), c = 'r')
     plt.pause(0.05)
     i += 1
     #print(data)

     if data[0] <= 0.14:
        print('Data holding within range...', data[0])
     else:
        print('Data has gone over selected range, stopping', data[0])

        break

    #plt.savefig("Load_Cell_DILLON2.png")
     
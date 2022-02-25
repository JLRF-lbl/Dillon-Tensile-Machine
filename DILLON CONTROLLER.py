#DILLON Controller Program
#Author: Claudia Bird, Jose Luis Rudeiros Fernandez

import sys
import os
import time
import nidaqmx
from nidaqmx.constants import ExcitationSource, ForceUnits, TerminalConfiguration
import csv
import threading
import socket
import numpy as np
import matplotlib.pyplot as plt

#Set working directory, for file/data read and write
os.chdir(r"C:\Users\CMBird\Documents\Dillon-Tensile-Machine")

HOST = '192.168.10.30' #CompuMotor IP Address
PORT = 5002 #Transmit/receive the standard 6K ASCII command set

#Socket creation -> compuMotor = socket object
try:
    compuMotor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

#Attempt connection to the socket (compuMotor)
compuMotor.connect((HOST,PORT))

#Main function********************************************************
def main():

    connectCheck()

#*********************************************************************
#Connection check
def connectCheck():
    checkMsg = 'TNT:'

    try:
        compuMotor.send(bytes((checkMsg), 'ascii')) #is this the correct way to do it?
        msg = compuMotor.recv(1024).decode('ascii')
        print(msg)
    
    except Exception as e:
        print(e)
        print('Failed to send data, closing socket...')
        compuMotor.shutdown(1)
        compuMotor.close()
    
    else:
        configureMotor()
        time.sleep(0.5)
        mainMenu()

#Configures the motor, which must be done to enable motion            
def configureMotor():
    print("Configuring motor...")

    with open(r"DILLON_CONFIG.csv", 'r') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            text = row[0]
            compuMotor.send(bytes((text), 'ascii'))
            time.sleep(0.1) #Wait between line sends 

#User facing terminal menu, for use without a GUI                     #Create TKinter GUI?
def mainMenu():
    print("")
    print("     DILLON MECHANICAL TESTING MACHINE")

    userChoice = input("""
    [1] Move Motor
    [2] Test A Sample
    [3] Settings
    [4] Exit Program

    [Enter your choice]: """)

    #user choice error handling
    if userChoice == "[1]" or userChoice == "1":
        moveMotor()
    elif userChoice == "[2]" or userChoice == "2":
        sampletest()
    elif userChoice == "[3]" or userChoice == "3":
        settingsMenu()
    elif userChoice == "[4]" or userChoice == "4":
        compuMotor.shutdown(1)
        compuMotor.close()
        
        print("""
        Socket closed.
        Program exiting...""")

    else:
        print("     You must select from menu!")
        mainMenu() #Reinitiate main menu

#Intended to move motor without data collection
def moveMotor():                                                     
    print("Please select option")
    print(""" 
    [1] Move
    [2] Main Menu
    [3] End Program""")

    userChoice = input("Option: ")

    if userChoice == "[1]" or userChoice == "1":
        print("""
        MOVE MENU INSTRUCTIONS:

        To move the motor*, enter move distance, velocity**,
            and initiate drive
        
        Format: D(value): or V(value):
        Example: Moving the motor 5.0 mm at 0.2 mm/s
                 D5.0: [ENTER] 
                 V0.2: [ENTER]
                 DRIVE1: [ENTER]
                 GO1: [ENTER]

        *Issue '!K:' command to kill motors
        **Velocity must not exceed a value of 0.4
        
        To return to the main menu, type: RETURN TO MAIN MENU""")

        while True:
            try:
                newCommand = input('Type Command:')

                if newCommand == '!K:':
                    compuMotor.send(bytes((newCommand), 'ascii'))
                    newMsg = compuMotor.recv(1024).decode('ascii')
                    print(newMsg)
                    print('Kill motor command sent, killing motors')
                    endCMD = input('End program? Enter END')
                    if endCMD == 'END':
                        print('Closing program...')
                        compuMotor.shutdown(1)
                        compuMotor.close()
                        break
                elif newCommand == 'RETURN TO MAIN MENU':
                    mainMenu()
                else:
                    compuMotor.send(bytes((newCommand), 'ascii'))
                    newMsg = compuMotor.recv(1024).decode('ascii')
                    print('CompuMotor: ', newMsg)

            except Exception as e:
                #Handle exception+safety disconnect
                print(e)
                print('Disconnecting from Compumotor...')
                compuMotor.shutdown(1)
                compuMotor.close()

    elif userChoice == "[2]" or userChoice == "2":
        print("Returning to main menu...")
        time.sleep(0.5)
        mainMenu()

    elif userChoice == "[3]" or userChoice == "3":
        print("Program ended, socket closing...")
        compuMotor.shutdown(1)
        compuMotor.close()
        time.sleep(0.5)
        print("Socket closed.")

    else:
        print("Proper option was not selected, reinitiating submenu...")
        time.sleep(0.5)
        moveMotor()

#Mechanical sample testing, still under development
def sampletest():
    #startTime = time.time() #Time enoch
    print("""
    Function under development...
    Returning to main menu...""")
    
    #endTime = time.time()
    #timeElapsed = (endTime- startTime)
    #print("Testing time elapsed: " + timeElapsed)

    #Formatting for NIDAQMX Load Cell Channel
    # plt.ion() 

    # i = 0

    # with nidaqmx.Task() as task:

    #     ai_channel = task.ai_channels.add_ai_voltage_chan_with_excit("Dev2/ai2",
    #     name_to_assign_to_channel= "Load Cell", 
    #     terminal_config= TerminalConfiguration.DIFFERENTIAL,
    #     voltage_excit_source= ExcitationSource.EXTERNAL,
    #     voltage_excit_val= 10.0)

    #     task.read()
    
    #     while i < 100:
    #         data = task.read(number_of_samples_per_channel = 1)
    #         plt.scatter(i, data[0], c = 'r')
    #         plt.pause(0.05)
    #         i += 1
    #         print(data)

    #         plt.savefig("Load_Cell2.png")

    mainMenu()

def settingsMenu():
    print("""
    Function under development...
    Returning to main menu...""")

    #This portion is intended for use in writing to the csv file which
    #contains all of the sensor data, and then save it

    mainMenu()

#*********************************************************************
main()
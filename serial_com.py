#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:33:20 2017

@author: hanihussein
"""

import warnings #warning library to show warning messages
import serial #import serial library for seril comunication
import serial.tools.list_ports #import serial tool for list serial ports


i=0 #counter
serial_ports=[] #declare array for serial ports

print("Available serial ports: \n")

#list of avalaible Arduino ports
for p in serial.tools.list_ports.comports(): #loop on serial ports list
    serial_ports.append( p.device)  #Add the serial port to the serial ports array
    print (str(i) +") "+ p.device + "  >>  " +p.description )   #Display the serial port and its description for the user in console
    i+=1   #increment i by one



if not serial_ports:    #showing warning if there is no Arduino port available
    availableArduino = False
    warnings.warn("No Arduino port found")  
    
    #Ask user for Running anyway without Connection to Arduino port or Stop
    if(input("Run anyway?[y/n]") is "n"):   
        run = False
        raise IOError("No Arduino found")
    else:   #if user choose not running, showing "No arduino found" error and stop
        run = True

        
else:
    #If there are more than one serial port
    if len(serial_ports) > 1:
        chosen_port = int(input("\n Enter the index of the Arduino port >> "))  # Ask user to choose the required Serial port to communicat with
        availableArduino = True 
        
    else:   #else if there is only one serial port, Choosing it by default 
        chosen_port=0
        availableArduino = True 

if(availableArduino):   #Displaying the chosen port to communicate with
    print("\n ##Connecting to ", serial_ports[chosen_port])


#function for sending serial data
def send_data(coordinates):
    
        if(availableArduino):   #if there is an arduino port available and chosen by user
            
            #declare new serial communication and set its parameters
            ser = serial.Serial(
            port=serial_ports[chosen_port],  # set arduino port
            baudrate=9600,  #set Transfer rate           
            timeout=1
             )
            
            
            print("sending: ", coordinates, " to: ", ser.portstr)  # Showing data that send to the arduino
            ser.reset_input_buffer()
            ser.write(bytes(coordinates,'utf-8'))  # sending the coordinates

            
        



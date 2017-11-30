#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:33:20 2017

@author: hanihussein
"""

import warnings #warning library to show warning messages
import serial #import serial library for seril comunication
import serial.tools.list_ports #import serial tool for list serial ports

#list of avalaible Arduino ports
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports() #loop on serial ports list
    if 'Arduino' in p.description   #search for arduino ports
]

#showing warning if there is no Arduino port
if not arduino_ports:
    raise IOError("No Arduino found")
#showing warning if there are more than one Arduino port
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first one')


print("connect to", arduino_ports[0])


#function for sending serial data
def send_data(coordinates):
	ser = serial.Serial(arduino_ports[0])  # open Arduino serial port
	print("sending Data to: ", ser.portstr)  # check which port was really used
	ser.write(coordinates)  # sending the coordinates
	ser.close()    #close port serial
    


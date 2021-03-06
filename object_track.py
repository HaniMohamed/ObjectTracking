
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 21:51:01 2017

@author: hanihussein
"""

import cv2   #import openCV library for the computer vision
import numpy as np   #import numpy library for arrays usages
import serial


port = "/dev/ttyACM1"
baud = 9600
 
#ser = serial.Serial(port, baud, timeout=1)

upperBound = np.array([30,255,255])   #upper bound of the object's color in HSV  -> look at [1]
kernelOpen = np.ones((10, 10))    #Max. array of pixels that cosider as noise pixels  -> look at [2]
kernelClose = np.ones((20, 20)) #array of pixels which will fill in -> look at [3]

cam = cv2.VideoCapture(0)    #capture video from camera index 1


def nothing(x):
    pass

cv2.namedWindow('Camera', cv2.WINDOW_GUI_NORMAL)

cv2.namedWindow('HSV', cv2.WINDOW_GUI_NORMAL)

cv2.namedWindow('Mask', cv2.WINDOW_GUI_NORMAL)

cv2.namedWindow('Mask Open', cv2.WINDOW_GUI_NORMAL)

cv2.namedWindow('Mask Close', cv2.WINDOW_GUI_NORMAL)


# Creating track bar for the lowBound
cv2.createTrackbar('h', 'Camera', 0, 255, nothing)
cv2.createTrackbar('s', 'Camera', 0, 255, nothing)
cv2.createTrackbar('v', 'Camera', 0, 255, nothing)

def reset_trackBars():
    cv2.setTrackbarPos('h', 'Camera', 20)
    cv2.setTrackbarPos('s', 'Camera', 100)
    cv2.setTrackbarPos('v', 'Camera', 100)

reset_trackBars()

#start the process loop
while True:
    ser.reset_input_buffer()
    ret, img = cam.read()   #read the captured video
    img = cv2.resize(img,(340,220)) #resize img window
    height, width = img.shape[:2] #get width and height of the frame
    #draw the center of the frame
    cv2.rectangle(img, (int(width/2),int(height/2)), (int(width/2),int(height/2)),(255,0,0), 5)


    #Convert BGR color to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h', 'Camera')
    s = cv2.getTrackbarPos('s', 'Camera')
    v = cv2.getTrackbarPos('v', 'Camera')

    lowerBound = np.array([h,s,v])   #lower bound of the object's color in HSV  -> look at [1]

    #Create Mask, Showing only rquired color using the HSV range of the color
    mask = cv2.inRange(imgHSV,lowerBound, upperBound)   # -> [1]

    
    #Clear noise pixels
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen) # -> [2]
    
        
    #Fill in the object tracked
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose) # -> [3]
    
    
    finalMask = maskClose #define the final mask to work on
    
    #Get the contour of the object
    _, conts, _ = cv2.findContours(finalMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    
    #Draw Rectangle on the object
    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i]) #get dimensions of the bounding rectangle arround the object
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2) #draw the rectangle with green color
        centerX = (x+(w/2)) #center of regtangle in X-axis
        centerY = (y+(h/2)) #center of regtangle in Y-axis
        #draw the center of the rectangle on the frame
        cv2.rectangle(img, (int(centerX),int(centerY)), (int(centerX),int(centerY)),(0,0,255), 2) 
       
        originCenterX = int(width / 2) - int(centerX)    #center of object in X-axis with respect to origin
        originCenterY = int(height / 2) - int(centerY)   #center of object in Y-axis with respect to origin
        coordintates2origin = "(" + str(originCenterX) + ", " + str(originCenterY)+")" #convert the coordintates to string
        #showing coordintates2origin on the camera frame
        cv2.putText(img, coordintates2origin, (x+w+5,y+h+5), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 0, 255), 1)
        
        
        ser.write(bytes(coordintates2origin,'utf-8'))

        
    
    
    #Showing Camera frame
    cv2.imshow("Camera", img) 
    #Showing Camera frame in HSV color
    cv2.imshow("HSV", imgHSV)
    #Showing mask frame
    cv2.imshow("Mask",mask)
    #Showing maskOpen frame
    cv2.imshow("Mask Open", maskOpen)
    #Showing maskClose frame
    cv2.imshow("Mask Close", maskClose)
    
    #wait for key pressed
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop (Exit)
    if key == ord("q"):
        break
    elif key == ord("c"):
        cv2.imwrite("test.jpg",img)
    elif key == ord("r"):
        reset_trackBars()

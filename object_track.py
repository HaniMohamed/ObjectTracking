#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 21:51:01 2017

@author: hanihussein
"""

import cv2   #import openCV library for the computer vision
import numpy as np   #import numpy library for arrays usages


lowerBound = np.array([33,80,40])   #lower bound of the object's color in BGR  -> look at [1]
upperBound = np.array([64,255,255])   #upper bound of the object's color in BGR  -> look at [1]
kernelOpen = np.ones((10, 10))    #Max. array of pixels that cosider as noise pixels  -> look at [2]
kernelClose = np.ones((20, 20)) #array of pixels which will fill in -> look at [3]

cam = cv2.VideoCapture(1)   #capture video from camera index 1


#start the process loop
while True:
    ret, img = cam.read()   #read the captured video
    img = cv2.resize(img,(340,220)) #resize img window
    cv2.imshow("Camera", img) #Showing Camera frame


    #Convert BGR color to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
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
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2) #draw the rectangle
        centerX = (x+w) / 2 #center of regtangle in X-axis
        centerY = (y+h) / 2 #center of regtangle in Y-axis
        print(centerX , centerY)    #Print coordinates of the center of the object
    
    

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
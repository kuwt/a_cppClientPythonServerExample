#
# Written by kuwingto, 15 Nov 2019
#

import os
import math
import random
import numpy as np
import cv2
import importlib.util

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import time

import zmq
import segment_service_input_pb2

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


class segmentationServer:
    def __init__(self):
        self.setupNetwork()
        print("Ready")
    def setupNetwork(self):
        # setup your network here. 
        self.a = 1
        
        
if __name__ == '__main__' :
    from time import time
    ser = segmentationServer()
    
     # Here For demonstration, we read a image to the buffer and will send back to CLient
    outimage = cv2.imread("./segmentation.bmp", cv2.IMREAD_GRAYSCALE)
    
    while True:
        print("waiting connection")
        message = socket.recv()
        print("message recv")
        if (message):
            start = time()
            
            #input 
            segment_service_input = segment_service_input_pb2.segment_service_input()
            segment_service_input.ParseFromString(message)
            print("class_id = " , segment_service_input.class_id)
            print("image width = ", segment_service_input.img.width)
            print("image height = ", segment_service_input.img.height)
            #print(type(segment_service_input.img.image_data))
            nparr = np.frombuffer(segment_service_input.img.image_data,dtype=np.ubyte)
            print("data shape = ",nparr.shape)
            img = nparr.reshape(segment_service_input.img.height,segment_service_input.img.width)
            print("image shape = ",img.shape)
            
            #uncomment show the image
            #print(img.shape)
            #stacked_img = np.stack((img,)*3, axis=-1)
            #imgplot = plt.imshow(stacked_img)
            #plt.show()
            
            #handling 
            
            
            #output
            segment_service_output = segment_service_input_pb2.segment_service_input()
            segment_service_output.class_id = segment_service_input.class_id
            segment_service_output.img.width = segment_service_input.img.width
            segment_service_output.img.height = segment_service_input.img.height
            segment_service_output.img.image_data = outimage.tobytes() 
            str = segment_service_output.SerializeToString()
            socket.send(str)
        else:
            print("error message")
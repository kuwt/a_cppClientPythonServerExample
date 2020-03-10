#
# Written by kuwingto, 10 March 2020
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
import my_message_multi_pb2

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
    outimage = cv2.imread("../data/segmentation.bmp", cv2.IMREAD_GRAYSCALE)
    
    while True:
        print("waiting connection")
        message = socket.recv()
        print("message recv")
        if (message):
            start = time()
            
            #input images
            my_message_input = my_message_multi_pb2.my_message_multi()
            my_message_input.ParseFromString(message)
            for i in range(len(my_message_input.imgs) ):
                print("received image width = ", my_message_input.imgs[i].width)
                print("received image height = ", my_message_input.imgs[i].height)
                #print(type(my_message_input.imgs[i].image_data))
                nparr = np.frombuffer(my_message_input.imgs[i].image_data,dtype=np.ubyte)
                print("data shape = ",nparr.shape)
                img = nparr.reshape(my_message_input.imgs[i].height,my_message_input.imgs[i].width)
                print("image shape = ",img.shape)
                
                #uncomment show the image
                #print(img.shape)
                #stacked_img = np.stack((img,)*3, axis=-1)
                #imgplot = plt.imshow(stacked_img)
                #plt.show()
            
            #handling 
            #???
                
            #output
            my_message_output = my_message_multi_pb2.my_message_multi()
            class_id = my_message_input.class_id
            height = outimage.shape[0]
            width = outimage.shape[1]
            sendimage = outimage
            
            #prepare message
            my_message_output.class_id = my_message_input.class_id
            
            # 1st image
            img = my_message_output.imgs.add()
            img.width = width
            img.height = height
            img.image_data = sendimage.tobytes() 

             # 2nd image
            img = my_message_output.imgs.add()
            img.width = width
            img.height = height
            img.image_data = sendimage.tobytes() 
            
            #serialize message
            str = my_message_output.SerializeToString()
            socket.send(str)
        else:
            print("error message")
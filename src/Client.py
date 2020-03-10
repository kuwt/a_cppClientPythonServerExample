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
import my_message_pb2

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


if __name__ == '__main__' :
    from time import time
    
    # Here For demonstration, we read a image to the buffer and will send back to CLient
    sendimage = cv2.imread("../data/test.bmp", cv2.IMREAD_GRAYSCALE)
    class_id = 0
    
    #prepare message
    height, width = sendimage.shape
    my_message_output = my_message_pb2.my_message()
    my_message_output.class_id = class_id
    my_message_output.img.width = width
    my_message_output.img.height = height
    my_message_output.img.image_data = sendimage.tobytes() 
    str = my_message_output.SerializeToString()
    
    # send message
    socket.send(str)
    
    # receive message
    message = socket.recv()
    print("message recv")
    
    my_message_input = my_message_pb2.my_message()
    my_message_input.ParseFromString(message)
    print("received class_id = " , my_message_input.class_id)
    print("received image width = ", my_message_input.img.width)
    print("received image height = ", my_message_input.img.height)
    #print(type(my_message_input.img.image_data))
    nparr = np.frombuffer(my_message_input.img.image_data,dtype=np.ubyte)
    print("data shape = ",nparr.shape)
    img = nparr.reshape(my_message_input.img.height,my_message_input.img.width)
    print("image shape = ",img.shape)
    
    #uncomment show the image
    print(img.shape)
    stacked_img = np.stack((img,)*3, axis=-1)
    imgplot = plt.imshow(stacked_img)
    plt.show()

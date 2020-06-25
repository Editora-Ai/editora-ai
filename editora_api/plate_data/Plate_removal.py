#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 18:04:06 2020

@author: parhamsadri
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import detect_lp
from os.path import splitext,basename
from keras.models import model_from_json
import glob
from PIL import Image


def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)

wpod_net_path = "wpod-net.json"
wpod_net = load_model(wpod_net_path)

def preprocess_image(image,resize=False):
    img = np.asarray(image)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

def remove_plate(image):
    try :
        Dmax = 608
        Dmin = 288
        vehicle = preprocess_image(image)
        ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    
    
    
        pts=[]  
        x_coordinates=cor[0][0]
        y_coordinates=cor[0][1]
        # store the top-left, top-right, bottom-left, bottom-right 
        # of the plate license respectively
        for i in range(4):
            pts.append([int(x_coordinates[i]),int(y_coordinates[i])])
        
        pts = np.array(pts, np.int32)
        pts = pts.reshape((-1,1,2))
        vehicle_image = np.asarray(image)
        
        cv2.fillPoly(vehicle_image,[pts],color=[255,255,255])
        return vehicle_image
    except :
        return image
# rawcars= './car3'


def get_plate(image_path):
        Dmax = 608
        Dmin = 288
        vehicle = preprocess_image(image_path)
        ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.4)
        return LpImg, cor

# for f in os.listdir(rawcars):
#     img = cv2.imread(os.path.join(rawcars , f))
#     # try :
#     aaa = remove_plate(img)
#     cv2.imwrite(f , aaa)
    # except :
    #     pass
# img = cv2.imread('./car2/2020-06-15_17-52-56_UTC_3.jpg')
# multiple_plates_image = "./car2/2020-06-15_18-22-07_UTC.jpg"
# LpImg,cor = get_plate(img)
# plt.figure(figsize=(10,5))
# plt.axis(False)
# plt.imshow(preprocess_image(img))
# for i in range(20):
#     plt.imshow(LpImg[i])
#     plt.show()
# # Visualize the obtained plates
# plt.figure(figsize=(10,5))
# plt.subplot(1,2,1)
# plt.axis(False)
# plt.imshow(LpImg[1])
# plt.subplot(1,2,2)
# plt.axis(False)
# plt.imshow(LpImg[0])
def multi_plate(array_image):
    img = np.array(array_image , np.uint8)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    try :
        LpImg,cor = get_plate(img)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        vehicle_image = np.asarray(array_image)
        # print(LpImg)
        for i in range(len(LpImg)):
            print(len(LpImg))
            pts=[]  
            x_coordinates=cor[i][0]
            y_coordinates=cor[i][1]
            print(x_coordinates)
            print(y_coordinates)
            for j in range(4):
                pts.append([int(x_coordinates[j]),int(y_coordinates[j])])
            pts = np.array(pts, np.int32)
            print(pts)
            pts = pts.reshape((-1,1,2))
                # vehicle_image = np.asarray(array_image)
            cv2.fillPoly(vehicle_image,[pts],color=[255,255,255])
        return vehicle_image
    except :
        return array_image
# aaa= multi_plate(img)
# plt.imshow(aaa)
# plt.imshow(aaa)

def fixchannels(img):
	imw = img.shape[0]
	imh = img.shape[1]
	imd = img.shape[2]
	bed = np.zeros(shape = (imw, imh , imd))
	b = img[:,:,0]
	g = img[:,:,1]
	r = img[:,:,2]
	bed[:,:,0] = r
	bed[:,:,1] = g
	bed[:,:,2] = b
	return bed
####################################### use remove_plate as final function ##############################

import os
import cv2
import numpy as np
from .utils import detect_lp
from os.path import splitext,basename
from tensorflow.compat.v1.keras.models import model_from_json
import glob


def load_model(path):
    path = splitext(path)[0]
    with open('%s.json' % path, 'r') as json_file:
        model_json = json_file.read()
    model = model_from_json(model_json, custom_objects={})
    model.load_weights('%s.h5' % path)
    return model
    

wpod_net_path = os.path.realpath("wpod-net.json")
head, tail = os.path.split(wpod_net_path)
wpod_net_path = head + "/editora_api" + "/plate_data/" + tail
wpod_net = load_model(wpod_net_path)
print(wpod_net)

def preprocess_image(image,resize=False):
    img = np.asarray(image)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

def remove_plate(image):
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


def get_plate(image_path):
        Dmax = 608
        Dmin = 288
        vehicle = preprocess_image(image_path)
        ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.4)
        return LpImg, cor

def multi_plate(array_image):
    img = np.array(array_image , np.uint8)
    try :
        LpImg,cor = get_plate(img)
        vehicle_image = np.asarray(array_image)
        for i in range(len(LpImg)):
            pts=[]  
            x_coordinates=cor[i][0]
            y_coordinates=cor[i][1]
            for j in range(4):
                pts.append([int(x_coordinates[j]),int(y_coordinates[j])])
            pts = np.array(pts, np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.fillPoly(vehicle_image,[pts],color=[255,255,255])
        return vehicle_image
    except :
        return array_image

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

import os
import cv2
from PIL import Image
import math
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

def preprocess_image(image,resize=False):

    img = np.asarray(image)
    img = np.array(image , np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img /= 255
    
    return img

def watermarker(img,logo_img , pts):
    bed2 = np.full(shape = (img.shape[0] ,img.shape[1]  ,3) , fill_value = 0)
    Xes =[]
    Yes = []
    for i in range(4):
        Xes.append(pts[i][0][0])
        Yes.append(pts[i][0][1])
    Xes = np.array(Xes)
    Yes = np.array(Yes)
    rep_img_x = pts[0][0][0]
    if pts[3][0][0]> pts[0][0][0]:
        rep_img_x = pts[3][0][0]
    rep_img_X = pts[1][0][0]
    if pts[2][0][0]< pts[1][0][0]:
        rep_img_X = pts[2][0][0]
    
    rep_img_y = pts[0][0][1]
    if pts[3][0][0]> pts[0][0][1]:
        rep_img_y = pts[3][0][1]
    rep_img_Y = pts[1][0][1]
    if pts[2][0][0]< pts[1][0][1]:
        rep_img_Y = pts[2][0][1]
    x_mean = Yes.mean()
    y_mean = Xes.mean()

    resize_number = pts[2][0][1]-pts[1][0][1]
    resize_number2 = pts[1][0][0]-pts[0][0][0]

    
    if (resize_number*logo_img.shape[1]/logo_img.shape[0])< (pts[1][0][0] - pts[0][0][0]) :
        logoimg = cv2.resize(logo_img , dsize = (int(resize_number*logo_img.shape[1]/logo_img.shape[0]) , resize_number),interpolation =  cv2.INTER_AREA)

    if (resize_number*logo_img.shape[1]/logo_img.shape[0])> (pts[1][0][0] - pts[0][0][0]) :
        logoimg = cv2.resize(logo_img , dsize = (int(resize_number2) , int(resize_number2*logo_img.shape[0]/logo_img.shape[1])),interpolation =  cv2.INTER_AREA)
    logo_height = logoimg.shape[0]
    logo_width = logoimg.shape[1]
    logoimg = np.array(logoimg)

    bed2[int((x_mean-logo_height//2)):int((x_mean+(logo_height-logo_height//2))) ,int((y_mean-logo_width//2)):int((y_mean+(logo_width-logo_width//2)))] = logoimg

    bed2 = np.array(bed2 , np.uint8)
    bed2 = Image.fromarray(bed2)
    angle = 180*(math.atan(((pts[0][0][1]-pts[1][0][1])/(pts[1][0][0]-pts[0][0][0]))))/3.141692
    bed2 = bed2.rotate(angle , resample = 0,center = (y_mean , x_mean))

    bed2 = np.array(bed2 , np.uint8)
    img[bed2!=0] =bed2[bed2!=0]
    return img

def get_points(image):
    try :
        X_IMG_SIZE = image.shape[0] 
        Y_IMG_SIZE = image.shape[1]
        Dmax = 608
        Dmin = 288
        vehicle = preprocess_image(image)
        ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.4)
        
        const1,const2 = image.shape[0] , image.shape[1]
        pts=[]  
        x_coordinates=cor[0][0]
        y_coordinates=cor[0][1]
        for i in range(4):
            pts.append([int(x_coordinates[i]),int(y_coordinates[i])])
        pts = np.array(pts, np.int32)
        pts = pts.reshape((-1,1,2))
        
        
        ST = True
    
        return  pts , ST
    except :
        ST = False
        return image , ST

def remove_plate_W(img):
    pts , st = get_points(img)
    if st == True :
        cv2.fillConvexPoly(img,pts,color=[255,255,255])
        
        cv2.polylines(img,pts,True,(255,255,255),thickness=1,lineType=cv2.LINE_AA)
        return img
    else :
        return img
 
def replace_LOGO_on_white_plate(img , logo):
    ptss , st = get_points(img)
    if st == True :
        cv2.fillConvexPoly(img,ptss,color=[255,255,255])
        cv2.polylines(img = img,pts=[ptss],isClosed= True,color = (255,255,255),thickness=1,lineType=cv2.LINE_AA)
        img = watermarker(img , logo, ptss)
        return img
    else :
        return img
def replace_JUST_LOGO(img , logo):
    pts , st = get_points(img)
    if st == True :
        img = watermarker(img , logo, pts)
        return img
    else :
        return img
####################################### use remove_plate as final function ##############################

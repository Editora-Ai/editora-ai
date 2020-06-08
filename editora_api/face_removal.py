import cv2
import numpy as np

prototxt_path = "/home/ragnar/Desktop/editora-ai/editora_api/fr_data/deploy.prototxt.txt"
model_path = "/home/ragnar/Desktop/editora-ai/editora_api/fr_data/res10_300x300_ssd_iter_140000_fp16.caffemodel"

def face_removal(image):
    model = cv2.cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    h, w = image.shape[:2]
    image = np.array(image,np.uint8)
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1
    blob = cv2.cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 130.0, 123.0))
    model.setInput(blob)
    output = np.squeeze(model.forward())
    for i in range(0, output.shape[0]):
        confidence = output[i,2]
        if confidence > 0.4:
            box = output[i, 3:7] * np.array([w, h, w, h])
            print(box)
            start_x, start_y, end_x, end_y = box.astype(np.int)
            face = image[start_y: end_y, start_x: end_x]
            face2 = cv2.cv2.GaussianBlur(face, (kernel_width, kernel_height), 8)
            aaa = np.zeros(shape =(face.shape[0] , face.shape[1] , face.shape[2]))
            center_coordinates = (face.shape[1]//2 , face.shape[0]//2)
            axesLength = (face.shape[1]//2 , face.shape[0]//2)
            angle = 0
            color = (255,255,255)
            thickness = -1
            endAngle = 360
            startAngle = 0
            imagee = cv2.ellipse(aaa, center_coordinates, axesLength, angle, startAngle, endAngle , color, thickness) 
            face[imagee== [255,255,255]] = face2[imagee== [255,255,255]]
            image[start_y: end_y, start_x: end_x] = face
    return image
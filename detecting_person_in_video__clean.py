import torch
from cv2 import cv2
import numpy as np
# import pandas
import time
# torch.set_default_tensor_type('torch.cuda.FloatTensor')

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

model.cuda() if torch.cuda.is_available else model.cpu()
print("running on gpu") if torch.cuda.is_available else (print("running on cpu"))


video="test_videos/test3.mp4"
# video=1


model.conf=0.6
model.classes = [0] # 0 for person class






def getPedestrianCoordinates(frame):
    print(".",end="")
    # start=time.time()
    res=model(frame)
    # end=time.time()
    # print(end-start)
    # print(res)
    framedata=res.pandas().xyxy[0]
    # print(framedata)
    pedestrianbottommids=[]
    for detection in range(len(framedata)):
        xmin,ymin,xmax,ymax=framedata["xmin"][detection],framedata["ymin"][detection],framedata["xmax"][detection],framedata["ymax"][detection]
        drawbox(frame,xmin,ymin,xmax,ymax)
        pedestrianbottommids.append([int((xmin+xmax)//2),int(ymax//1)])
        drawpoint(frame,pedestrianbottommids[-1])
            


    cv2.imshow("image",frame)
    
    return pedestrianbottommids

def drawbox(image,xmin,ymin,xmax,ymax):
    cv2.rectangle(image,(int(xmin//1),int(ymin//1)),(int(xmax//1),int(ymax//1)),(255,255,255),1)

def drawpoint(image,center):
    cv2.circle(image, center, 1, (255,255,255), 6)
    cv2.circle(image, center, 1, (100,255,100), 2)


cap=cv2.VideoCapture(video)
ret,img=cap.read()
start=time.time()
while ret:

    img=cv2.resize(img,None,fx=0.5,fy=0.5)
    coord=getPedestrianCoordinates(img)
    print(coord)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    end=time.time()
    print(end-start)
    ret,img=cap.read()
    # ret,img=cap.read()
    start=time.time()



import torch
from cv2 import cv2
import numpy as np
# import pandas
import time
# torch.set_default_tensor_type('torch.cuda.FloatTensor')

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# model.cpu()
model.cuda()

# video="test_videos/test3.mp4"
video="test_videos/TownCentre.mp4"

confidencescore=0.0







def getPedestrianCoordinates(frame):
    print(".",end="")
    res=model(frame)
    # print(res)
    framedata=res.pandas().xyxy[0]
    print(framedata)
    pedestrianbottommids=[]
    for detection in range(len(framedata)):
        if framedata["class"][detection]==0:
            if framedata["confidence"][detection]>confidencescore:
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
    # cv2.circle(image, center, 1, (0,255,0), 4)
    # cv2.circle(image, center, 1, (255,100,100), 2)
    cv2.circle(image, center, 1, (100,255,100), 2)
    # cv2.circle(image, center, 1, (100,100,255), 2)

    # cv2.circle(image, center, 1, (0,0,255), 3)


cap=cv2.VideoCapture(video)
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps= ",fps)
currentframe=cap.get(cv2.CAP_PROP_POS_FRAMES)
print("currentframe= ",currentframe)
cap.set(cv2.CAP_PROP_POS_FRAMES, 150)
ret,img=cap.read()
start=time.time()
while ret:

    img=cv2.resize(img,None,fx=0.5,fy=0.5)
    coord=getPedestrianCoordinates(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    end=time.time()

    print("************************************************")
    print("time=",end-start)
    print("************************************************")

    ret,img=cap.read()
    start=time.time()



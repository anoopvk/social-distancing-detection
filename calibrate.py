
import cv2
import numpy as np


def savetofile(points):
    pass

# mouse callback function
def handle_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv2.circle(img,(x,y),5,(0,0,255),-1)
        param[0]=x
        param[1]=y
def draw_points(image,points,color):
    for p in points:
        cv2.circle(image,p,5,color,-1)




video="test_videos/TownCentre.mp4"

cap=cv2.VideoCapture(video)

ret,img=cap.read()
ret,img=cap.read()

p=[-1,-1]

cv2.namedWindow('image')
cv2.setMouseCallback('image',handle_click,p)
current_point_number=0
points_dict={}


while(1):
    plotted_image=img.copy()
    draw_points(plotted_image,[p],(0,0,255))
    draw_points(plotted_image,points_dict.values(),(0,255,0))
    
    cv2.imshow('image',plotted_image)
    k = cv2.waitKey(1) & 0xFF
    print(p,current_point_number,points_dict)

    if current_point_number>3:
        savetofile(points_dict)
        break
    if k == 13:
        points_dict[current_point_number]=p.copy()
        current_point_number+=1
    if k == 27: #escape key
        break
print(points_dict)
cv2.destroyAllWindows()
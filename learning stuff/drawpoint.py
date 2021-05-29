# from cv2 import cv2
# import matplotlib.pyplot as plt
# img = cv2.imread("test_images/people.jpg")
# # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # scaled_image = cv2.resize(rgb_img,(0,0), rgb_img, 0.4, 0.4)

# def just_print_for_all(event, x, y, flags, param):
#     print("x,y,event,flags,param",x,y,"events=",event,"flags=",flags,param)

# # set when to have a call back
# cv2.namedWindow("Title of Popup Window")

# #what to happen on call back
# cv2.setMouseCallback("Title of Popup Window", just_print_for_all)

# #show image to user with title
# cv2.imshow("Title of Popup Window", img)
# cv2.waitKey()
# cv2.destroyAllWindows()



import cv2
import numpy as np



# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv2.circle(img,(x,y),5,(0,0,255),-1)
        param[0]=x
        param[1]=y
video="test_videos/TownCentre.mp4"

cap=cv2.VideoCapture(video)
ret,img=cap.read()
# img = np.zeros((512,512,3), np.uint8)
p=[0,0]
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle,p)
current_point_number=0
points_dict={}
while(1):
    plotted_image=img.copy()
    cv2.circle(plotted_image,(p[0],p[1]),5,(0,0,255),-1)
    for x,y in points_dict.values():
        cv2.circle(plotted_image,(x,y),5,(0,255,0),-1)
    
    cv2.imshow('image',plotted_image)
    k = cv2.waitKey(1) & 0xFF
    print(p,current_point_number,points_dict)
    if current_point_number>3:
        break
    if k == 13:
        points_dict[current_point_number]=p.copy()
        current_point_number+=1
    if k == 27: #escape key
        break
print(points_dict)
cv2.destroyAllWindows()
# to do 
# gui
# 
# 
import cv2 as cv2
from detecting_person_in_video__clean import getPedestrianCoordinates
# from utilties import getFilename
from utilties import *
from sd_calc import get_sd_violation_pairs
import numpy as np

video=getFilename()
speedup=1
cap=cv2.VideoCapture(video)
ret=True
while ret:
    for i in range(speedup):
        ret,img=cap.read()

    # print(getPedestrianCoordinates(img))
    top_left,bottom_right,bottom_mid_coord=getPedestrianCoordinates(img)
    sd_violation_pairs_indexes=get_sd_violation_pairs(bottom_mid_coord)
    # print(org_coord)
    # print(org_vioations,"******")
    # print(transformed_violations,"------")
    org_img=img.copy()

    h_matrix=np.array(getTranslationMatrix())
    outputsize=getOutputsize()
    transformed_image=cv2.warpPerspective(img,h_matrix,outputsize)

    for i in range(len(bottom_mid_coord)):
        cv2.rectangle(org_img,(int(top_left[i][0]//1),int(top_left[i][1]//1)),(int(bottom_right[i][0]//1),int(bottom_right[i][1]//1)),(255,255,255),1)
        cv2.circle(org_img, bottom_mid_coord[i], 1, (255,255,255), 10)
        cv2.circle(org_img, bottom_mid_coord[i], 1, (100,255,100), 5)

    for i in sd_violation_pairs_indexes:
        cv2.line(org_img,bottom_mid_coord[i[0]],bottom_mid_coord[i[1]],(0,0,255),3)

    # for i in org_vioations:
    #     # org_img=cv2.circle(org_img,i,5,(0,0,255),5)
    #     # cv2.circle(org_img, i, 1, (255,255,255), 10)
    #     cv2.circle(org_img,i,1,(100,100,255),5)
    #     print(i)

    
    # for i in transformed_violations:
    #     print(i)
    #     cv2.circle(transformed_image,(int((i[0])//1),int((i[1])//1)),5,(0,0,255),5)
    #     # transformed_image=cv2.circle(transformed_image,i,5,(0,0,255),5)

    print(len(sd_violation_pairs_indexes))  
    org_img=cv2.putText(org_img,str(len(sd_violation_pairs_indexes)),(100,100),cv2.FONT_HERSHEY_SIMPLEX,5,(0,0,255),4)

    org_img=cv2.resize(org_img,None,fx=0.5,fy=0.5)
    # transformed_image=cv2.resize(transformed_image,None,fx=0.4,fy=0.4)


    cv2.imshow("orig_image",org_img)
    # cv2.imshow("transformed_image",transformed_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

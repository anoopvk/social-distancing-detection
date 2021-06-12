
import cv2 as cv2
from google.auth.crypt import Signer
from detecting_person_in_video__clean import getPedestrianCoordinates
# from utilties import getFilename
from utilties import *
from sd_calc import get_sd_violation_pairs
import numpy as np
from display import get_output_image
import time
from action import *

# output_screen_width=1024
# output_screen_height=720
output_screen_width=1366
output_screen_height=768


video=getFilename()
speedup=1
cap=cv2.VideoCapture(video)
ret=True
transformation_matrix=getTranslationMatrix()
h_matrix=np.array(transformation_matrix)
outputsize=getOutputsize()
minDistance=getSdDistance()
showOutput=True
sd_threshold_iot=getSdThresholdIOT()
sd_threshold_email=getSdThresholdEmail()
critical_density=getCriticalDensity()
last_mail_time=getLastMailTime()
mail_interval=getMailInterval()
save_data_is_on=getSaveDataIsOn()

if save_data_is_on:
    resetSavedData()
turnOffSign()
sign_status="off"


for i in range(200):
    ret,img=cap.read()
while ret:
    start=time.time()
    for i in range(speedup):
        ret,img=cap.read()

    top_left,bottom_right,bottom_mid_coord=getPedestrianCoordinates(img)
    sd_violation_pairs_indexes=get_sd_violation_pairs(bottom_mid_coord,minDistance)
    
    sd_count=len(sd_violation_pairs_indexes)
    pedestrian_count=len(bottom_mid_coord)



# --------------------------------------------------------
    if critical_density!=-1 and pedestrian_count>critical_density:
        # critical_density crossed
        criticaldensitycrossed=True
    else:
        criticaldensitycrossed=False
    
    if sd_count>sd_threshold_iot and sign_status=="off":
        # turn on light
        print("\n\n\nturning on sign-----------")
        turnOnSign()
        sign_status="on"
         
    if sd_count<sd_threshold_iot and sign_status=="on":
        # turn off light
        print("\n\n\nturning off sign---------------")
        turnOffSign()
        sign_status="off"



    if sd_count>sd_threshold_email:
        # print(last_mail_time,time.time())
        curtime=time.time()
        if last_mail_time+mail_interval<curtime:
            print(last_mail_time)
            print(mail_interval)
            print(last_mail_time+mail_interval)
            print(curtime)
            print("------------------------sending email--------------------")
            sendEmail(sd_count,pedestrian_count)
            print("------------------------email sent--------------------")

            setMailTime(curtime)
            last_mail_time=curtime
        else:
            print("email in cooldown ",round(last_mail_time+mail_interval-curtime)," remaining")

# --------------------------------------------------------
    if save_data_is_on:
        saveData(sd_count,pedestrian_count)
    


    if showOutput:
        start2=time.time()
        output_image=get_output_image(img,h_matrix,outputsize,[top_left,bottom_right,bottom_mid_coord],sd_violation_pairs_indexes,output_screen_width,output_screen_height)
        # print("time to calc output frame = ",time.time()-start2)
        

        cv2.imshow("output",output_image)
        
        # print("time per frame = ",time.time()-start)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

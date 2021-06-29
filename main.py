
import cv2 as cv2
# from google.auth.crypt import Signer
from modules.detecting_person_in_video__clean import getPedestrianCoordinates
# from utilties import getFilename
from modules.utilties import *
from modules.sd_calc import get_sd_violation_pairs
import numpy as np
from modules.display import get_output_image, get_output_image_light
import time
from modules.action import *
import threading

# output_screen_width=1024
# output_screen_height=720
# output_screen_width=1366
# output_screen_height=768

output_screen_width,output_screen_height=getOutputScreenResolution()
video=getFilename()
speedup=2
cap=cv2.VideoCapture(video)
ret=True
transformation_matrix=getTranslationMatrix()
h_matrix=np.array(transformation_matrix)
outputsize=getOutputsize()
minDistance=getSdDistance()
showOutputFlag=getShowOutputFlag()
showOutputLightFlag=getShowOutputLightFlag()
sd_threshold_iot=getSdThresholdIOT()
sd_threshold_email=getSdThresholdEmail()
critical_density=getCriticalDensity()
last_mail_time=getLastMailTime()
mail_interval=getMailInterval()
save_data_is_on=getSaveDataIsOn()
turnOffSign()
sign_status="off"
turnOffSign2()
cd_sign_status="off"
last_shown_email_cooldown_time=0




if save_data_is_on:
    resetSavedData()

frameskips=200
for i in range(frameskips):
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
    # if critical_density>0 and pedestrian_count>critical_density and cd_sign_status=="off":
    #     # critical_density crossed
    #     # criticaldensitycrossed=True
    #     turnOnSign2()
    #     cd_sign_status="on"
    # else:
    #     # criticaldensitycrossed=False
    #     if cd_sign_status=="on":
    #         turnOffSign2()
    #         cd_sign_status="off"


    if critical_density>0:
        if pedestrian_count>critical_density:
            if cd_sign_status=="off":
                turnOnSign2()
                cd_sign_status="on"
        else:
            if cd_sign_status=="on":
                turnOffSign2()
                cd_sign_status="off"
                
    # --------------------------------------------------------

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
            # sendEmail(sd_count,pedestrian_count)
            mailthread=threading.Thread(target=sendEmail,args=[sd_count,pedestrian_count])
            mailthread.start()
            # print("------------------------email sent--------------------")

            setMailTime(curtime)
            last_mail_time=curtime
        else:
            cooldown_time_remaining=round(last_mail_time+mail_interval-curtime)
            if last_shown_email_cooldown_time!=cooldown_time_remaining:
                print("email in cooldown ",cooldown_time_remaining,"seconds remaining")
                last_shown_email_cooldown_time=cooldown_time_remaining
    # --------------------------------------------------------
    if save_data_is_on:
        saveData(sd_count,pedestrian_count)
    


    if showOutputFlag:
        start2=time.time()
        if showOutputLightFlag:
            output_image=get_output_image_light(img,[top_left,bottom_right,bottom_mid_coord],sd_violation_pairs_indexes,sign_status,cd_sign_status,last_mail_time,critical_density,output_screen_width,output_screen_height)
        else:
            output_image=get_output_image(img,h_matrix,outputsize,[top_left,bottom_right,bottom_mid_coord],sd_violation_pairs_indexes,sign_status,cd_sign_status,last_mail_time,critical_density,output_screen_width,output_screen_height)
        # print("time to calc output frame = ",time.time()-start2)
        

        cv2.imshow("output",output_image)
        
        # print("time per frame = ",time.time()-start)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('v'):
            print("---------v pressed------------")
            showOutputLightFlag= not showOutputLightFlag

        if k==27 or k == ord('q'):
            break
        
        
print("exiting main")
cv2.destroyAllWindows()
# exit()
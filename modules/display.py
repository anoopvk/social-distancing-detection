import cv2
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.lib.arraypad import pad
from numpy.lib.type_check import imag
# from utilties import image_resize
from modules.utilties import *
# from utilties import *

import time
from datetime import datetime

def get_output_image(input_image,transformationMatrix,transformationOutputsize,pedestrianPos,sdViolationPairs,sign_status,cd_sign_status,last_mail_time,critical_density,width,height):
    font_size=0.8
    
    # start=time.time()
    # print(transformationMatrix,pedestrianPos,sdViolationPairs,width,height)
    top_left,bottom_right,bottom_mid_coord=pedestrianPos
    # height,width=720,1024
    padding=5
    output_image = np.zeros((height,width,3), np.uint8)
    output_image[:,:] = (255,255,255)
    # output_image[:,0:width//2] = (255,255,0)
    # output_image[(height*(padding)//100):(height*(75-padding)//100),(width*padding//100):(width*(50-padding)//100)] = (255,0,255)
    org_img=input_image.copy()

    # plotting rectangle for each pedestrian
    for i in range(len(bottom_mid_coord)):
        # cv2.rectangle(org_img,(int(top_left[i][0]//1),int(top_left[i][1]//1)),(int(bottom_right[i][0]//1),int(bottom_right[i][1]//1)),(255,255,255),1)
        cv2.rectangle(org_img,(int(top_left[i][0]//1),int(top_left[i][1]//1)),(int(bottom_right[i][0]//1),int(bottom_right[i][1]//1)),(0,255,0),2)
        cv2.circle(org_img, bottom_mid_coord[i], 2, (255,255,255), 10)
        cv2.circle(org_img, bottom_mid_coord[i], 2, (100,255,100), 5)
    
    # draw lines between sd violators and red circle
    for i in sdViolationPairs:
        cv2.rectangle(org_img,(int(top_left[i[0]][0]//1),int(top_left[i[0]][1]//1)),(int(bottom_right[i[0]][0]//1),int(bottom_right[i[0]][1]//1)),(0,0,255),2)
        cv2.rectangle(org_img,(int(top_left[i[1]][0]//1),int(top_left[i[1]][1]//1)),(int(bottom_right[i[1]][0]//1),int(bottom_right[i[1]][1]//1)),(0,0,255),2)
        cv2.line(org_img,bottom_mid_coord[i[0]],bottom_mid_coord[i[1]],(0,0,255),3)
        cv2.circle(org_img, bottom_mid_coord[i[0]], 3, (0,0,255), 15)
        cv2.circle(org_img, bottom_mid_coord[i[1]], 3, (0,0,255), 15)







    # old_width=org_img.shape[1] +
    new_width=(output_image.shape[1]//2)-(2*padding)
    # old_height=org_img.shape[0]
    # new_height=((org_img.shape[0]*(output_image.shape[1]//2))//org_img.shape[1])-(2*padding)

    # org_img = cv2.resize(org_img, (new_width, new_height))
    org_img=square_image(org_img)
    org_img=image_resize(org_img,width=new_width)
    output_image[padding:org_img.shape[0]+padding,padding:(org_img.shape[1])+padding]=org_img

    transformed_image=cv2.warpPerspective(input_image,transformationMatrix,transformationOutputsize)
    
    # draw red circles and lines in bird eye view
    transformed_points=cv2.perspectiveTransform(np.float32(bottom_mid_coord).reshape(-1, 1, 2),transformationMatrix)
    if not (transformed_points is None):
        transformed_points=transformed_points.reshape(-1,2)
        transformed_points=transformed_points.tolist()
        transformed_points=[[int(i) for i in j] for j in transformed_points]
        for i in transformed_points:
            cv2.circle(transformed_image, i, 3, (0,255,0),15)
            # cv2.circle(transformed_image, (int(i[0]),int(i[1])), 1, (0,0,255), 15)
        for i in sdViolationPairs:
            cv2.circle(transformed_image,transformed_points[i[0]], 3, (0,0,255), 15)
            cv2.circle(transformed_image,transformed_points[i[1]], 3, (0,0,255), 15)

            cv2.line(transformed_image,transformed_points[i[0]],transformed_points[i[1]],(0,0,255),3)


    

    # print("output_image",output_image.shape,"transformed_image",transformed_image.shape,new_width)
    
    
    transformed_image=square_image(transformed_image)
    transformed_image=image_resize(transformed_image,width=new_width)
    # print("output_image",output_image.shape,"transformed_image",transformed_image.shape,new_width)

    # print("----------------------------")
    # print("output_image",output_image.shape,"transformed_image",transformed_image.shape,new_width)
    # print("----------------------------")
    
    output_image[padding:transformed_image.shape[0]+padding,(output_image.shape[1]//2)+padding:(output_image.shape[1]//2)+padding+transformed_image.shape[1]]=transformed_image

    # cv2.imshow("img",output_image)
    # cv2.waitKey(0)
    # print(time.time()-start)
    # cv2.putText(output_image,"number of sd violations = "+str(len(sdViolationPairs)),(padding,new_width+(50)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)
    cv2.putText(output_image,"number of sd violations = "+str(len(sdViolationPairs)),(padding,new_width+(5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)
    cv2.putText(output_image,"number of pedestrians detected = "+str(len(bottom_mid_coord)),(padding,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)
    if critical_density>0:
        cv2.putText(output_image,"critical density = "+str(critical_density),(padding,new_width+(15*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)
    


    signcolor=(0,255,0) if sign_status=="on" else (0,0,255)
    cv2.putText(output_image,"sign status = ",(output_image.shape[1]//2,new_width+(5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)
    # cv2.putText(output_image,str(sign_status),(output_image.shape[1]//2 + 235,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    cv2.putText(output_image,str(sign_status),(output_image.shape[1]//2 + 185,new_width+(5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,signcolor,2)

    cd_signcolor=(0,255,0) if cd_sign_status=="on" else (0,0,255)
    cv2.putText(output_image,"cd_sign status = ",(output_image.shape[1]//2,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)
    # cv2.putText(output_image,str(cd_sign_status),(output_image.shape[1]//2 + 235,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),3)
    cv2.putText(output_image,str(cd_sign_status),(output_image.shape[1]//2 + 235,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,cd_signcolor,2)

    
    if last_mail_time>0:
        # cv2.putText(output_image,"last mail sent = "+str(datetime.utcfromtimestamp(last_mail_time+19800).strftime('%Y/%m/%d %H:%M:%S')),(output_image.shape[1]//2,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)
        cv2.putText(output_image,"last mail sent = "+str(datetime.utcfromtimestamp(last_mail_time+19800).strftime('%d/%m/%y %H:%M:%S')),(output_image.shape[1]//2,new_width+(15*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,(0,0,0),1)

    
    return output_image


def get_output_image_light(input_image,pedestrianPos,sdViolationPairs,sign_status,cd_sign_status,last_mail_time,critical_density,width,height):
    font_size=1
    
    top_left,bottom_right,bottom_mid_coord=pedestrianPos
    padding=5
    # output_image = np.zeros((height,width,3), np.uint8)
    # output_image[:,:] = (255,255,255)
    # org_img=input_image.copy()
    org_img=input_image


    # plotting rectangle for each pedestrian
    for i in range(len(bottom_mid_coord)):
        # cv2.rectangle(org_img,(int(top_left[i][0]//1),int(top_left[i][1]//1)),(int(bottom_right[i][0]//1),int(bottom_right[i][1]//1)),(255,255,255),1)
        cv2.rectangle(org_img,(int(top_left[i][0]//1),int(top_left[i][1]//1)),(int(bottom_right[i][0]//1),int(bottom_right[i][1]//1)),(0,255,0),2)
        cv2.circle(org_img, bottom_mid_coord[i], 2, (255,255,255), 10)
        cv2.circle(org_img, bottom_mid_coord[i], 2, (100,255,100), 5)
    
    # draw lines between sd violators and red circle
    for i in sdViolationPairs:
        cv2.rectangle(org_img,(int(top_left[i[0]][0]//1),int(top_left[i[0]][1]//1)),(int(bottom_right[i[0]][0]//1),int(bottom_right[i[0]][1]//1)),(0,0,255),2)
        cv2.rectangle(org_img,(int(top_left[i[1]][0]//1),int(top_left[i[1]][1]//1)),(int(bottom_right[i[1]][0]//1),int(bottom_right[i[1]][1]//1)),(0,0,255),2)
        cv2.line(org_img,bottom_mid_coord[i[0]],bottom_mid_coord[i[1]],(0,0,255),3)
        cv2.circle(org_img, bottom_mid_coord[i[0]], 3, (0,0,255), 15)
        cv2.circle(org_img, bottom_mid_coord[i[1]], 3, (0,0,255), 15)







    # old_width=org_img.shape[1] +
    r1=width/org_img.shape[1]
    r2=height/org_img.shape[0]
    if r1<r2:
        org_img=image_resize(org_img,width=width)
    else:
        org_img=image_resize(org_img,height=height)


    line_number=1
    text_thickness=2
    black=(0,0,0)
    white=(255,255,255)
    outsidecolor=black
    cv2.putText(org_img,"number of sd violations = "+str(len(sdViolationPairs)),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,outsidecolor,text_thickness)
    line_number+=1
    cv2.putText(org_img,"number of pedestrians detected = "+str(len(bottom_mid_coord)),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,outsidecolor,text_thickness)
    line_number+=1
    if critical_density>0:
        cv2.putText(org_img,"critical density = "+str(critical_density),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,outsidecolor,text_thickness)
        line_number+=1
    # signcolor=(0,255,0) if sign_status=="on" else (0,0,255)
    cv2.putText(org_img,"sign status = ",(padding,line_number*5*padding),cv2.FONT_HERSHEY_DUPLEX,font_size,outsidecolor,text_thickness)
    # cv2.putText(org_img,str(sign_status),(padding + 185,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,signcolor,text_thickness)
    line_number+=1
    cv2.putText(org_img,"cd sign status = ",(padding,line_number*5*padding),cv2.FONT_HERSHEY_DUPLEX,font_size,outsidecolor,text_thickness)
    # cv2.putText(org_img,str(sign_status),(padding + 185,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,signcolor,text_thickness)
    line_number+=1
    if last_mail_time>0:
        cv2.putText(org_img,"last mail sent = "+str(datetime.utcfromtimestamp(last_mail_time+19800).strftime('%d/%m/%y %H:%M:%S')),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,outsidecolor,text_thickness)
        line_number+=1

    line_number=1
    text_thickness=1

    insidecolor=white

    cv2.putText(org_img,"number of sd violations = "+str(len(sdViolationPairs)),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,insidecolor,text_thickness)
    line_number+=1
    cv2.putText(org_img,"number of pedestrians detected = "+str(len(bottom_mid_coord)),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,insidecolor,text_thickness)
    line_number+=1
    if critical_density>0:
        cv2.putText(org_img,"critical density = "+str(critical_density),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,insidecolor,text_thickness)
        line_number+=1
    signcolor=(0,255,0) if sign_status=="on" else (0,0,255)
    cv2.putText(org_img,"sign status = "+str(sign_status),(padding,line_number*5*padding),cv2.FONT_HERSHEY_DUPLEX,font_size,insidecolor,text_thickness)
    cv2.putText(org_img,str(sign_status),(padding + 235,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,signcolor,text_thickness+1)
    line_number+=1
    cd_signcolor=(0,255,0) if cd_sign_status=="on" else (0,0,255)
    cv2.putText(org_img,"cd sign status = "+str(cd_sign_status),(padding,line_number*5*padding),cv2.FONT_HERSHEY_DUPLEX,font_size,insidecolor,text_thickness)
    cv2.putText(org_img,str(cd_sign_status),(padding + 290,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,cd_signcolor,text_thickness+1)
    line_number+=1
    if last_mail_time>0:
        cv2.putText(org_img,"last mail sent = "+str(datetime.utcfromtimestamp(last_mail_time+19800).strftime('%d/%m/%y %H:%M:%S')),(padding,(line_number*5*padding)),cv2.FONT_HERSHEY_DUPLEX,font_size,insidecolor,text_thickness)
        line_number+=1
    
    return org_img

    









if __name__=="__main__":
    
    video=getFilename()
    cap=cv2.VideoCapture(video)
    ret,img=cap.read()
    transformation_matrix=getTranslationMatrix()
    h_matrix=np.array(transformation_matrix)


    tl=[[217.125, 820.5], [815.25, 236.25], [1596.0, 619.5], [1647.0, 115.125], [891.0, 67.6875], [1803.0, 182.625], [987.75, 0.46875], [1153.5, 2.6484375], [850.5, 402.75], [1578.0, 938.25], [643.875, 980.25], [732.375, 221.625], [1456.5, 27.9375]] 
    br=[[330.375, 1077.0], [881.25, 418.875], [1719.0, 877.5], [1713.0, 283.875], [945.0, 228.9375], [1878.0, 342.0], [1047.75, 126.09375], [1189.5, 75.9375], [958.5, 624.0], [1725.0, 1079.25], [790.5, 1080.0], [808.5, 406.5], [1543.5, 193.5]] 
    mid=[[273, 1077], [848, 418], [1657, 877], [1680, 283], [918, 228], [1840, 342], [1017, 126], [1171, 75], [904, 624], [1651, 1079], [717, 1080], [770, 406], [1500, 193]]

    sd_viol=[[0, 10], [1, 11], [2, 9], [3, 5]]

    # a=get_output_image(img,h_matrix,getOutputsize(),[tl,br,mid],sd_viol,1024,720)
    start=time.time()

    # a=get_output_image(img,h_matrix,getOutputsize(),[tl,br,mid],sd_viol,"off",12,14,1366,768)
    a=get_output_image(img,h_matrix,getOutputsize(),[tl,br,mid],sd_viol,"off","on",12,14,1024,720)

    # b=get_output_image_light(img,[tl,br,mid],sd_viol,"off","on",12,14,2000,500)
    cv2.imshow("a",a)
    # cv2.imshow("b",b)
    # print(time.time()-start)

    cv2.waitKey(0)
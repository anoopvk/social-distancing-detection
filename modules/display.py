import cv2
import numpy as np
from numpy.lib.arraypad import pad
from numpy.lib.type_check import imag
# from utilties import image_resize
from utilties import *
import time

def get_output_image(input_image,transformationMatrix,transformationOutputsize,pedestrianPos,sdViolationPairs,width,height):
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
        cv2.rectangle(org_img,(int(top_left[i][0]//1),int(top_left[i][1]//1)),(int(bottom_right[i][0]//1),int(bottom_right[i][1]//1)),(255,255,255),1)
        cv2.circle(org_img, bottom_mid_coord[i], 2, (255,255,255), 10)
        cv2.circle(org_img, bottom_mid_coord[i], 2, (100,255,100), 5)
    
    # draw lines between sd violators and red circle
    for i in sdViolationPairs:
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
    cv2.putText(output_image,"number of sd violations = "+str(len(sdViolationPairs)),(padding,new_width+(10*padding)),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),1)
    cv2.putText(output_image,"number of pedestrians detected = "+str(len(bottom_mid_coord)),(padding,new_width+(15*padding)),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),1)

    return output_image




    









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
    a=get_output_image(img,h_matrix,getOutputsize(),[tl,br,mid],sd_viol,1366,768)

    cv2.imshow("a",a)
    cv2.waitKey(0)

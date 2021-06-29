from cv2 import cv2
import numpy as np 

# homography.py>

def find_homography_matrix(img,points,measurements):
    height=img.shape[0]
    width=img.shape[1]

    #input from user
    projected_width=measurements[0]
    projected_height=measurements[1]

    # tl=[351,390]
    # tr=[984,249]
    # br=[1102,414]
    # bl=[400,610]



    pts1=np.float32(points)
    xmin=0
    ymin=0
    xmax=projected_width
    ymax=projected_height
    pts2=np.float32(([xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]))

    m=cv2.getPerspectiveTransform(pts1,pts2)

    outputimg11=cv2.warpPerspective(img,m,(2000,2000))

    # outputimg11=cv2.resize(outputimg11,(700,700))
    # cv2.imshow("outputimg11",outputimg11)

    list_points_to_detect = np.float32([[0,0],[width,0],[0,height],[width,height]]).reshape(-1, 1, 2)
    transformed_points = cv2.perspectiveTransform(list_points_to_detect, m)
    # print(transformed_points)
    minvals=np.amin(transformed_points,axis=0).reshape(-1)
    maxvals=np.amax(transformed_points,axis=0).reshape(-1)
    # print(minvals,maxvals)
    x_translate=int(minvals[0])
    y_translate=int(minvals[1])
    outputsize=list(map(int,maxvals))
    outputsize[0]-=x_translate
    outputsize[1]-=y_translate
    # outputsize_y=maxvals[1]
    # print("outputsize=",outputsize)

    #recalculate destination corner points
    xmin=-x_translate
    ymin=-y_translate
    xmax=-x_translate+projected_width
    ymax=-y_translate+projected_height
    pts2=np.float32(([xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]))
    # print("pts1=",pts1)
    # print("pts2=",pts2)

    m2=cv2.getPerspectiveTransform(pts1,pts2)
    # print(type(m2))
    # m2_list = m2.tolist()
    # return m2_list

    # print("m2=  \n",m2)
    # outputimg=cv2.warpPerspective(img,m2,outputsize)
    # outputimg=cv2.resize(outputimg,(700,700))
    # cv2.imshow("outputimg",outputimg)
    # img=cv2.resize(img,(700,700))
    # cv2.imshow("img",img)

    # cv2.waitKey(0)

    return [m2,outputsize]

if __name__=="__main__":
    image=cv2.imread("test_images/people.jpeg")
    projected_height=250
    projected_width=500

    tl=[351,390]
    tr=[984,249]
    br=[1102,414]
    bl=[400,610]
    measurements=[projected_width,projected_height]
    
    points=[tl,tr,br,bl]

    print(find_homography_matrix(image,points,measurements))
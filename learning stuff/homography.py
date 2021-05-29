from cv2 import cv2
import numpy as np 


img=cv2.imread("photos/paper.jpeg")
height=img.shape[0]
width=img.shape[1]

#input from user
projected_height=250
projected_width=500

#calculate these (idk how)

tl=[351,390]
tr=[984,249]
br=[1102,414]
bl=[400,610]


pts1=np.float32([tl,tr,br,bl])
xmin=0
ymin=0
xmax=projected_width
ymax=projected_height
pts2=np.float32(([xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]))

m=cv2.getPerspectiveTransform(pts1,pts2)


list_points_to_detect = np.float32([[0,0],[width,0],[0,height],[width,height]]).reshape(-1, 1, 2)
transformed_points = cv2.perspectiveTransform(list_points_to_detect, m)
print(transformed_points)
minvals=np.amin(transformed_points,axis=0).reshape(-1)
maxvals=np.amax(transformed_points,axis=0).reshape(-1)
print(minvals,maxvals)
x_translate=int(minvals[0])
y_translate=int(minvals[1])
outputsize=list(map(int,maxvals))
outputsize[0]-=x_translate
outputsize[1]-=y_translate
# outputsize_y=maxvals[1]
print("outputsize=",outputsize)

#recalculate destination corner points
xmin=-x_translate
ymin=-y_translate
xmax=-x_translate+projected_width
ymax=-y_translate+projected_height
pts2=np.float32(([xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]))
print("pts1=",pts1)
print("pts2=",pts2)

m2=cv2.getPerspectiveTransform(pts1,pts2)

outputimg=cv2.warpPerspective(img,m2,outputsize)

outputimg=cv2.resize(outputimg,(700,700))
cv2.imshow("outputimg",outputimg)

cv2.waitKey(0)
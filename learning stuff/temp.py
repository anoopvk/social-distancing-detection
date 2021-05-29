# import torch
# from cv2 import cv2
# import numpy as np
# # import pandas
# import time


# # Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


# # cap=cv2.VideoCapture("test_videos/test3.mp4")
# cap=cv2.VideoCapture(1)

# fps = cap.get(cv2.CAP_PROP_FPS)
# print("fps=",fps)

# ret, img = cap.read()
# print("ret=",ret)

# while ret:
 
#     img=cv2.resize(img,None,fx=0.5,fy=0.5)
#     # img=cv2.resize(img,(640,640))

#     start=time.time()
#     res=model(img)
#     # res.print()
#     # framedata=res.pandas().xyxy[0]
#     # print(framedata,len(framedata))

#     # for detection in range(len(framedata)):
#     #     print(framedata.name[detection])
#     end=time.time()

#     print("----end of frame---",end-start)


#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     ret, img = cap.read()
























# #     #!/usr/bin/env python

# # import cv2
# # import time

# # if __name__ == '__main__' :

# #     # Start default camera
# #     video = cv2.VideoCapture(0);

# #     # Find OpenCV version
# #     (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

# #     # With webcam get(CV_CAP_PROP_FPS) does not work.
# #     # Let's see for ourselves.

# #     if int(major_ver)  < 3 :
# #         fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
# #         print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
# #     else :
# #         fps = video.get(cv2.CAP_PROP_FPS)
# #         print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

# #     # Number of frames to capture
# #     num_frames = 120;

# #     print("Capturing {0} frames".format(num_frames))

# #     # Start time
# #     start = time.time()

# #     # Grab a few frames
# #     for i in range(0, num_frames) :
# #         ret, frame = video.read()

# #     # End time
# #     end = time.time()

# #     # Time elapsed
# #     seconds = end - start
# #     print ("Time taken : {0} seconds".format(seconds))

# #     # Calculate frames per second
# #     fps  = num_frames / seconds
# #     print("Estimated frames per second : {0}".format(fps))

# #     # Release video
# #     video.release()










import cv2
img = cv2.imread('test_images/people.jpg') # load a dummy image
while(1):
    cv2.imshow('img',img)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value

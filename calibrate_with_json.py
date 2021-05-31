
from tkinter.constants import NO
import cv2
import numpy as np
from learning_stuff.homography import find_homography_matrix
import json
from width_and_height import get_width_height



def savetofile(filename,points,measurements,h_matrix,outputsize):
    h_matrix2=h_matrix.tolist()
    # print(points,measurements,h_matrix)
    mydict={
        "filename":filename,
        "points":{
            "tl":points[0],
            "tr":points[1],
            "br":points[2],
            "bl":points[3]
        },
        "measurements":{
            "width":measurements[0],
            "height":measurements[1]
        },
        "translationMatrix":h_matrix2,
        "outputsize":outputsize
        }
    print(mydict)
    json_object = json.dumps(mydict,indent=1)
  
    # Writing to sample.json
    with open("calibration_values.json", "w") as outfile:
        outfile.write(json_object)
    # pass

# mouse callback function
def handle_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # cv2.circle(img,(x,y),5,(0,0,255),-1)
        param[0]=x
        param[1]=y

def draw_points(image,points,color):
    for p in points:
        cv2.circle(image,p,5,color,-1)

def draw_guiding_box(image,points,potential_point):

    if len(points)==1:
        image = cv2.line(image, points[0], potential_point, (0,0,255), 1)
    if len(points)==2:
        image = cv2.line(image, points[0], points[1], (0,0,255), 1)
        image = cv2.line(image, points[1], potential_point, (0,0,255), 1)
    if len(points)==3:
        image = cv2.line(image, points[0], points[1], (0,0,255), 1)
        image = cv2.line(image, points[1], points[2], (0,0,255), 1)
        image = cv2.line(image, points[2], potential_point, (0,0,255), 1)
    if len(points)==4:
        divisions=3
        for i in range(divisions+1):
            x_start=points[0][0]-(((points[0][0]-points[3][0])*i)//divisions)
            y_start=points[0][1]-(((points[0][1]-points[3][1])*i)//divisions)

            x_end=points[1][0]-(((points[1][0]-points[2][0])*i)//divisions)
            y_end=points[1][1]-(((points[1][1]-points[2][1])*i)//divisions)
            image = cv2.line(image, (x_start,y_start), (x_end,y_end), (200,200,200), 3)
            image = cv2.line(image, (x_start,y_start), (x_end,y_end), (0,0,255), 2)

        for i in range(divisions+1):
            x_start=points[0][0]-(((points[0][0]-points[1][0])*i)//divisions)
            y_start=points[0][1]-(((points[0][1]-points[1][1])*i)//divisions)

            x_end=points[3][0]-(((points[3][0]-points[2][0])*i)//divisions)
            y_end=points[3][1]-(((points[3][1]-points[2][1])*i)//divisions)
            image = cv2.line(image, (x_start,y_start), (x_end,y_end), (200,200,200), 3)
            image = cv2.line(image, (x_start,y_start), (x_end,y_end), (0,0,255), 2)
        # image = cv2.line(image, points[0], points[1], (0,0,255), 1)
        image = cv2.line(image, points[1], points[2], (0,0,255), 1)
        image = cv2.line(image, points[2], points[3], (0,0,255), 1)
        image = cv2.line(image, points[3], points[0], (0,0,255), 1)

def showtransformedimage(image,h_matrix,outputsize):
    font = cv2.FONT_HERSHEY_SIMPLEX

    newimage=cv2.warpPerspective(image,h_matrix,outputsize)
    newimage=cv2.resize(newimage,None,fx=0.5,fy=0.5)
    newimage=cv2.putText(newimage,"press any key to continue",(20,20),font,1,(255,255,255),1)
    cv2.imshow("bird_eye_view",newimage)
    
    cv2.waitKey(0)


def calibrator(video):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap=cv2.VideoCapture(video)

    ret,img=cap.read()
    ret,img=cap.read()

    p=[-1,-1]

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',handle_click,p)
    current_point_number=0
    points_dict={}
    messagetoggle=True
    insufficientpoints=False
    while(1):
        plotted_image=img.copy()
        if current_point_number<=3:
            draw_points(plotted_image,[p],(0,0,255))
            messagetext="'enter' to add point /'r' to reset /'esc' to exit"
        else:
            messagetext="press 's' to save /'r' to reset /'esc' to exit"
            insufficientpoints=False
            
        draw_points(plotted_image,points_dict.values(),(0,255,0))
        for i in points_dict.items():
            plotted_image = cv2.putText(plotted_image, str(i[0]), i[1], font, 1, (255,0,0), 1, cv2.LINE_AA)
        draw_guiding_box(plotted_image,points_dict,p)
        if messagetoggle:
            if insufficientpoints:
                plotted_image = cv2.putText(plotted_image, "insufficient points!", (100,60), font, 0.5, (200,200,255), 2, cv2.LINE_AA)
                plotted_image = cv2.putText(plotted_image, "insufficient points!", (100,60), font, 0.5, (0,0,255), 1, cv2.LINE_AA)

            plotted_image = cv2.putText(plotted_image, "t : toggle message", (100,80), font, 0.5, (200,200,200), 2, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "t : toggle message", (100,80), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, messagetext, (100,100), font, 0.5, (200,200,200), 2, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, messagetext, (100,100), font, 0.5, (255,0,0), 1, cv2.LINE_AA)

            plotted_image = cv2.putText(plotted_image, "0 : top left", (100,120), font, 0.5, (200,200,200), 2, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "1 : top right", (100,140), font, 0.5, (200,200,200), 2, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "2 : bottom right", (100,160), font, 0.5, (200,200,200), 2, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "3 : bottom left", (100,180), font, 0.5, (200,200,200), 2, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "0 : top left", (100,120), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "1 : top right", (100,140), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "2 : bottom right", (100,160), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
            plotted_image = cv2.putText(plotted_image, "3 : bottom left", (100,180), font, 0.5, (255,0,0), 1, cv2.LINE_AA)

        cv2.imshow('image',plotted_image)
        k = cv2.waitKey(1) & 0xFF
        
        

        if k == 13: #enter key
            if current_point_number<=3:
                points_dict[current_point_number]=p.copy()
                current_point_number+=1
            
            
        if k==ord("s"):
            if current_point_number<=3:
                insufficientpoints=True
            else:
                pts=list(points_dict.values())
                measurements=get_width_height()
                if not measurements:
                    break
                homography_matrix,outputsize=find_homography_matrix(img,pts,measurements)
                savetofile(video,pts,measurements,homography_matrix,outputsize)
                # showtransformedimage(img,homography_matrix,outputsize)
                # return True
                break

        if k==ord("t"):
            messagetoggle=not messagetoggle

        if k==ord("r"):
            current_point_number=0
            points_dict={}

        if k == 27: #escape key
            return False

    showtransformedimage(img,homography_matrix,outputsize)
    
    # cv2.destroyAllWindows()
    # return points_dict
    


if __name__=="__main__":
    # video="test_videos/TownCentre.mp4"
    video="test_videos/test3.mp4"
    # video="test_videos/test.mp4"

    calibrator(video)
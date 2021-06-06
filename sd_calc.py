
# read the matrix
# translate the points [[138, 360], [227, 164], [294, 143], [232, 352], [264, 227]]
# calculate the distance between points
import json
import numpy as np
import cv2 as cv2
import math
from itertools import combinations


# from detecting_person_in_video__clean import getPedestrianCoordinates
def read_matrix():

    with open('calibration_values.json') as f:
        data = json.load(f)

    h_matrix=data["translationMatrix"]
    outputsize=data["outputsize"]
    # print(h_matrix,"\n",outputsize)
    return h_matrix,outputsize

# def translate_points(points_input):
#     h_matrix,outputsize=read_matrix()
#     h_matrix = np.array(h_matrix)
#     # transformed_points = cv2.perspectiveTransform(points_input, h_matrix)
#     # print(transformed_points)


#     #showing
#     video="test_videos/test3.mp4"
#     v=cv2.VideoCapture(video)
#     ret=True
#     while ret:
#         ret,img=v.read()
#         coord=getPedestrianCoordinates(img)
#         img=cv2.warpPerspective(img,h_matrix,outputsize)
#         coord=np.array(coord)
#         coord=np.float32(coord).reshape(-1, 1, 2)
#         # print("---",coord,type(coord),"---\n",h_matrix,type(h_matrix))
#         transformed_points=cv2.perspectiveTransform(coord, h_matrix)
#         # print(transformed_points)
#         if not (transformed_points is None):
#             for i in transformed_points:
#             #     # print(i,"----",i[0][0],i[0][1])
#                 cv2.circle(img,list(map(int,(i[0][0],i[0][1]))),5,(0,0,255),-1)
#             # cv2.circle(img,(20,20),3,(0,0,255),-1)
#         img=cv2.resize(img,None,fx=0.4,fy=0.4)
#         cv2.imshow("image",img)
#         # cv2.waitKey(0)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break


def translate_points(points_input):
    h_matrix,outputsize=read_matrix()
    h_matrix = np.array(h_matrix)
    points_np=np.float32(points_input).reshape(-1, 1, 2)

    transformed_points=cv2.perspectiveTransform(points_np,h_matrix)
    # print(transformed_points.tolist())
    if not (transformed_points is None):
        transformed_points=transformed_points.reshape(-1,2)
    # print(transformed_points)
        return transformed_points
    else:
        return []
    # for i in transformed_points:
    #     print(i[0])

def calc_violations(original_points,transformed_points):
    sd_violated_points_transformed=[]
    sd_violated_points_original=[]
    violations_index_pairs=[]

    if len(transformed_points) >= 2:
        # Iterate over every possible 2 by 2 between the transformed_points combinations 
        list_indexes = list(combinations(range(len(transformed_points)), 2))
        # print(list_indexes)
        for i in list_indexes:
            # print(transformed_points[i[0]],transformed_points[i[1]])
            distance=math.sqrt( (transformed_points[i[0]][0] - transformed_points[i[1]][0])**2 + (transformed_points[i[0]][1] - transformed_points[i[1]][1])**2 ) 

            #could improve time complexity here
            if distance < int(200):
            
                # print(points[i[0]],points[i[1]],distance)
                violations_index_pairs.append([i[0],i[1]])
                # if list(transformed_points[i[0]]) not in sd_violated_points_transformed:
                #     sd_violated_points_transformed.append(list(transformed_points[i[0]]))
                #     sd_violated_points_original.append(list(original_points[i[0]]))
                # if list(transformed_points[i[1]]) not in sd_violated_points_transformed:
                #     sd_violated_points_transformed.append(list(transformed_points[i[1]]))
                #     sd_violated_points_original.append(list(original_points[i[1]]))

    # print(sd_violated_points_transformed)
    # return sd_violated_points_original,sd_violated_points_transformed
    return violations_index_pairs
    


def get_sd_violation_pairs(points_input):
    transformed_points=translate_points(points_input)
    violations_index_pairs=calc_violations(points_input,transformed_points)
    return violations_index_pairs

if __name__=="__main__": 
    # h_matrix,outputsize=read_matrix()
    points_input=[[138, 360], [227, 164], [294, 143], [232, 352], [264, 227]]
    points_input = np.array(points_input)
    list_points_to_detect = np.float32(points_input).reshape(-1, 1, 2)
    # translate_points(list_points_to_detect)
    # calc_violations(points_input)
    print(get_sd_violation_pairs(points_input))


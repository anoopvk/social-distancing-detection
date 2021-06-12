import json
import cv2
import numpy as np
import time

def getFilename():
    with open('calibration_values.json') as f:
        data = json.load(f)

    return data["filename"]


def getTranslationMatrix():
    with open('calibration_values.json') as f:
        data = json.load(f)

    return data["translationMatrix"]


def getOutputsize():
    with open('calibration_values.json') as f:
        data = json.load(f)

    return data["outputsize"]


def getOutputScreenSize():
    with open('settings.json') as f:
        data = json.load(f)

    return data["output_screen_width"],data["output_screen_height"]

def getSdDistance():
    with open('settings.json') as f:
        data = json.load(f)

    return data["sd_distance"]

def getSdThresholdIOT():
    with open('settings.json') as f:
        data = json.load(f)

    return data["threshold_iot"]

def getSdThresholdEmail():
    with open('settings.json') as f:
        data = json.load(f)

    return data["threshold_email"]

def getCriticalDensity():
    with open('settings.json') as f:
        data = json.load(f)

    return data["critical_desity"]

def getLastMailTime():
    with open('settings.json') as f:
        data = json.load(f)

    return data["last_mail_time"]

def getMailInterval():
    with open('settings.json') as f:
        data = json.load(f)

    return data["email_interval"]

def setMailTime(curtime):
    with open('settings.json') as f:
        data = json.load(f)

    data["last_mail_time"]=curtime
    json_object = json.dumps(data,indent=1)

    with open("settings.json", "w") as outfile:
        outfile.write(json_object)

def getSaveDataIsOn():
    with open('settings.json') as f:
        data = json.load(f)

    return data["save_data"]

def saveData(sd_count,pedestrian_count):
    with open('data.json') as f:
        data = json.load(f)

    data["sdviolations"].append(sd_count)
    data["numberofpedestrians"].append(pedestrian_count)

    json_object = json.dumps(data,indent=1)

    with open("data.json", "w") as outfile:
        outfile.write(json_object)

def resetSavedData():
    data={
    "sdviolations":[],
    "numberofpedestrians":[]
    }
    json_object = json.dumps(data,indent=1)
    with open("data.json", "w") as outfile:
        outfile.write(json_object)

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def square_image(img):
    s = max(img.shape[0:2])

    #Creating a dark square with NUMPY  
    f = np.zeros((s,s,3),np.uint8)

    #Getting the centering position
    ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2

    #Pasting the 'image' in a centering position
    f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
    return f
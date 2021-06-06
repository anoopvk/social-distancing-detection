import json

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


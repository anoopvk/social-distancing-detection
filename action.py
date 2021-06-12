from email import message
import requests
import json
import time
import os
import smtplib, ssl
from email.mime.text import MIMEText
from datetime import date, datetime

# firebase creating connection
import firebase_admin
from firebase_admin import db
cred_obj = firebase_admin.credentials.Certificate('C:/Users/Anoop/Desktop/btech_project_related/code/learning_stuff/sddetector-firebase-adminsdk-f9k64-b2662e6274.json')

default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://sddetector-default-rtdb.asia-southeast1.firebasedatabase.app/"
	})
ref = db.reference("/")

sender_email=os.environ.get("temp_email_address")
password=os.environ.get("temp_email_password")
# receiver_email = os.environ.get("my_email_address")
receiver_email="anoopthrowaway@gmail.com"

def turnOnSign():
    # 0 for on
    ref.set({"device1":0})

def turnOffSign():
    # 1 for off
    ref.set({"device1":1})

def sendEmail(sd_violations,numberofpedestrians):
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    mymessage="hey, sd violations has crossed the set threshold. \n sd violations={} \n number of pedestrians = {} \n Please do regulate the area.".format(sd_violations,numberofpedestrians)
    msg = MIMEText(mymessage)
    # print(mymessage)
    msg['Subject'] = "SD violation crossed threshold"
    msg['From'] = "Anoop " + sender_email
    msg['To'] = receiver_email
    # print(msg)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("mail sent!")
    
if __name__=="__main__":
    msg= "hey, the sd violations have crossed the threshold, please do the needful."
    # sendEmail(102,520)
    # turnOnSign()
    turnOffSign()


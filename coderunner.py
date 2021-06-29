# exec(open('main.py').read())
# import tkinter module
from tkinter import *       
# import tkMessageBox
# Following will import tkinter.ttk module and
# automatically override all the widgets
# which are present in tkinter module.
from tkinter.ttk import *
# from calibrate_with_json import maincalib
import subprocess
import os

# Create Object
coderunnerroot = Tk()
def runMain():
    # exec(open('main.py').read())
    # retcode = subprocess.call("python" + " main.py")
    # os.system("python" + " main.py")
    subprocess.Popen("python main.py")
    # print(retcode)

def runCalibrate():
    # exec(open('calibrate_with_json.py').read())
    # maincalib()
    # retcode = subprocess.call("python" + " calibrate_with_json.py")
    # os.system("python" + " calibrate_with_json.py")
    subprocess.Popen("python calibrate_with_json.py")


    
def runCriticaldensity():
    # exec(open('find_criticaldensity.py').read())
    # retcode = subprocess.call("python" + " find_criticaldensity.py")
    # os.system("python" + " find_criticaldensity.py")
    subprocess.Popen("python find_criticaldensity.py")



    


# Initialize tkinter window with dimensions 100x100            
coderunnerroot.geometry('250x150')    
 
btnMain = Button(coderunnerroot, text = 'Main', command = runMain)
btnCalibrate = Button(coderunnerroot, text = 'Calibrate', command = runCalibrate)
btnCD = Button(coderunnerroot, text = 'Find critical density', command = runCriticaldensity)

# Set the position of button on the top of window
btnMain.pack(side = 'top',pady=8)
btnCalibrate.pack(side = 'top',pady=8)
btnCD.pack(side = 'top',pady=8)

coderunnerroot.mainloop()
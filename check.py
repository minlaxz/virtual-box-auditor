#!/home/laxz/miniconda3/envs/vbox-dignity/bin/python

"""
Virtual Box Controller.
Code flow by Min Latt (laxz).
[My Repo](https://github.com/minlaxz)
most of Tkinter code credit to:
http://robotic-controls.com/learn/python-guis/basics-tkinter-gui

"""

from tkinter import Tk, Frame, Canvas, Text, Label, Button 
from datetime import datetime
import time, os
busy_flag = False

root = Tk() 
root.geometry("640x300") 
root.title("VM Control Panel") 
root.configure(background='white')
root.resizable(False,False)

### `widgets` :###############################################################
#### >Left Frame
leftFrame = Frame(root, width=200, height = 600)                        ######
leftFrame.grid(row=0, column=0, padx=10, pady=2)                        ######
#### >Right Frame
rightFrame = Frame(root, width=200, height = 600)                       ######
rightFrame.grid(row=0, column=1, padx=10, pady=2)                       ######
#### >>Canvas for drawing circles
circleCanvas = Canvas(rightFrame, width=100, height=100, bg='white')    ######
circleCanvas.grid(row=1, column=0, padx=15, pady=2)                     ######
#### >>Logging VM on/off status
VMLog = Text(rightFrame, width = 60, height = 10, takefocus=0)          ######
VMLog.grid(row=3, column=0, padx=10, pady=2)                            ######
###Labels  
firstLabel = Label(leftFrame, text="Operations")                        ######
firstLabel.grid(row=0, column=0, padx=10, pady=2)                       ######
secondLabel = Label(rightFrame, text="Status History")                  ######
secondLabel.grid(row=2, column=0, padx=10, pady=2)                      ######
thirdLabel = Label(rightFrame, text="Visual Status")                    ######
thirdLabel.grid(row=0, column=0, padx=10, pady=2)                       ######
##############################################################################

def vmOnStateHandler(): 
    global busy_flag
    if(not busy_flag):
        busy_flag = True
        VMLog.insert(0.2, "VM is initiating - Please Wait. {0}\n".format(datetime.now().strftime("%T")))
        buttonsDisabler()
        leftFrame.after(15000, alreadyRunning)
        VMLog.insert(0.2, "VM is lunched at {0}\n".format(datetime.now().strftime("%T")))
    busy_flag = False

def vmOffStateHandler(): 
    global busy_flag
    if(not busy_flag):
        busy_flag = True
        VMLog.insert(0.2, "VM is halting - Please Wait. {0}\n".format(datetime.now().strftime("%T")))
        buttonsDisabler()
        leftFrame.after(5000, VMOFF)
    busy_flag = False

def VMOFF():
    uuid = getVMStatus()
    if(uuid):
        VMLog.insert(0.2, '[VMOFF] Hibernating {0}\n'.format(uuid))
        #os.popen('/usr/lib/virtualbox/VBoxManage controlvm {0} savestate'.format(uuid))
        #VMLog.insert(0.2, "VM is halted at {0}\n".format(datetime.now().strftime("%T")))
        readyToRun()
    else:
        VMLog.insert(0.2, '[VMOFF] Unknown Error!\n')


def VMON():
    VMLog.insert(0.2, "Lunching VM.\n")
    #os.popen('/usr/lib/virtualbox/VBoxHeadless --startvm {b8197fcd-8c67-4d19-b420-dd17f98d7f52}')
    alreadyRunning(getVMStatus())

def buttonsDisabler():
    onButton.configure( state='disabled')
    offButton.configure( state='disabled')


def getVMStatus():
    oses = os.popen("VBoxManage list runningvms").read().strip()
    uuid = oses[len(oses)-38:len(oses)]
    #print("uuid is: ", uuid)
    return uuid

### `first lunch.` 
def alreadyRunning(uuid):
    if(uuid == getVMStatus()):
        circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='green')
        VMLog.insert(0.2, "uuid {0} is running.\n".format(uuid))
        onButton.configure( state='disabled')
        offButton.configure( state='active')
    else:
        readyToRun()

def readyToRun():
    uuid = getVMStatus()
    if(uuid):
        alreadyRunning(uuid)
    else:
        circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='white')
        VMLog.insert(0.2, "uuid {0} is halted.\n".format(uuid))
        onButton.configure( state='active')
        offButton.configure( state='disabled')

def initHandler():
    uuid = getVMStatus()
    if(uuid):
        alreadyRunning(uuid)
    else:
        readyToRun()

def disable_event():
    pass

onButton = Button(leftFrame, text="VM On", command=vmOnStateHandler)
onButton.grid(row=2, column=0, padx=5, pady=5)

offButton = Button(leftFrame, text="VM Off", command=vmOffStateHandler)
offButton.grid(row=3, column=0, padx=5, pady=5)

initHandler()
quitButton = Button(leftFrame, text="Quit", command=root.destroy)
quitButton.grid(row=6, column=0, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", disable_event)
root.mainloop() #loop to update GUI

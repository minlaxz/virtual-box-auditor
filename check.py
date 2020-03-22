#!/home/laxz/miniconda3/envs/vbox-dignity/bin/python

"""
Virtual Box Controller.
Code flow by Min Latt (laxz).
[My Repo](https://github.com/minlaxz)
most of Tkinter code credit to:
http://robotic-controls.com/learn/python-guis/basics-tkinter-gui

"""

from tkinter import Tk, Frame, Canvas, Text, Label, Button, StringVar, OptionMenu, ttk, messagebox
from tkinter.font import Font
from datetime import datetime
import time, os
busy_flag = False

root = Tk() 
root.geometry("700x400") 
root.title("VM Control Panel") 
root.configure(background='#d9d9d9')
root.resizable(False,False)

laxzFont = Font(family="Poppins", size=10, weight='bold')

### `widgets` :###############################################################
#### >Left Frame
leftFrame = Frame(root, width=150, height = 600)                        ######
leftFrame.grid(row=0, column=0, padx=10, pady=2)                        ######
#### >Right Frame
rightFrame = Frame(root, width=150, height = 600)                       ######
rightFrame.grid(row=0, column=1, padx=10, pady=2)                       ######
#### >>Canvas for drawing circles
circleCanvas = Canvas(rightFrame, width=100, height=100, bg='#d9d9d9')  ######
circleCanvas.grid(row=1, column=0, padx=15, pady=2)                     ######
#### >>Logging VM on/off status
VMLog = Text(rightFrame, width = 60, height = 10, takefocus=0)          ######
VMLog.grid(row=3, column=0, padx=10, pady=2)                            ######
VMLog.configure(font=laxzFont)
###Labels  
firstLabel = Label(leftFrame, text="Operations", font=laxzFont)         ######
firstLabel.grid(row=0, column=0, padx=10, pady=2)                       ######
secondLabel = Label(rightFrame, text="Status History")                  ######
secondLabel.grid(row=2, column=0, padx=10, pady=2)                      ######
thirdLabel = Label(rightFrame, text="Developed by minlaxz", font=laxzFont)                  ######
thirdLabel.grid(row=0, column=0, padx=10, pady=2)                     ######
##############################################################################

def vmOnStateHandler(): 
    global busy_flag
    if(not busy_flag):
        busy_flag = True
        buttonsDisabler()
        leftFrame.after(3000, VMON)
        VMLog.insert(0.2, "VM is lunched at {0}\n".format(datetime.now().strftime("%T")))
    busy_flag = False

def vmOffStateHandler(): 
    global busy_flag
    if(not busy_flag):
        busy_flag = True
        buttonsDisabler()
        leftFrame.after(3000, VMOFF)
        VMLog.insert(0.2, "VM is halting - Please Wait. {0}\n".format(datetime.now().strftime("%T")))
    busy_flag = False

def VMOFF():
    uuid = getVMStatus()
    if(uuid):
        os.popen('/usr/lib/virtualbox/VBoxManage controlvm {0} savestate'.format(uuid))
        VMLog.insert(0.2, "VM is halted at {0}\n".format(datetime.now().strftime("%T")))
        readyToRun()


def VMON():
    VMLog.insert(0.2, "Lunching VM.\n")
    os.popen('/usr/lib/virtualbox/VBoxHeadless --startvm {b8197fcd-8c67-4d19-b420-dd17f98d7f52}')
    alreadyRunning()

def buttonsDisabler():
    onButton.configure( state='disabled')
    offButton.configure( state='disabled')


def getVMStatus():
    oses = os.popen("VBoxManage list runningvms").read().strip()
    uuid = oses[len(oses)-38:len(oses)]
    #print("uuid is: ", uuid)
    return uuid

### `first lunch.` 
def alreadyRunning():
    if(getVMStatus()):
        circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='green')
        VMLog.insert(0.2, "uuid {0} is running.\n".format(getVMStatus()))
        onButton.configure( state='disabled')
        offButton.configure( state='active')
    else:
        readyToRun()

def readyToRun():
    if(getVMStatus()):
        alreadyRunning()
    else:
        circleCanvas.create_oval(20, 20, 80, 80, width=0, fill='red')
        VMLog.insert(0.2, "VM is halted.\n")
        onButton.configure( state='active')
        offButton.configure( state='disabled')

def initHandler():
    if(getVMStatus()):
        alreadyRunning()
    else:
        readyToRun()

def disable_event():
    VMLog.insert(0.2, "Quit Button overthere. :> \n")

def getAllVMs():
    oses = os.popen("VBoxManage list vms").read().strip()
    u1 = oses[len(oses)-38:len(oses)]
    pass

def adios():
    ans = messagebox.askokcancel("VM-C","The application will be closed")
    if ans:
        root.destroy()
    else:
        pass


onButton = Button(leftFrame, text="VM On", command=vmOnStateHandler)
onButton.grid(row=2, column=0, padx=5, pady=5)
onButton.config( height=2, width=5 )
onButton.configure(background='#80FFBA')


offButton = Button(leftFrame, text="VM Off", command=vmOffStateHandler)
offButton.grid(row=3, column=0, padx=5, pady=5)
offButton.config( height=2, width=5 )
offButton.configure(background='#EB2A4B')

quitButton = Button(leftFrame, text="Quit", command=adios)   
quitButton.grid(row=5, column=0, padx=5, pady=5)
quitButton.config( height=2, width=5 )
quitButton.configure(background='#FF7500')


OPTIONS = ['foo', 'bar']
myvar = StringVar(leftFrame)
myvar.set(OPTIONS[0])
option = OptionMenu(leftFrame, myvar, *OPTIONS)
##option = ttk.Combobox(leftFrame, values=OPTIONS)
##option.set(OPTIONS[0])
option.grid(row=6,column=0, padx=5, pady=5)
option.configure(height=1, width=3, background='#ABCBEF')
initHandler()
root.protocol("WM_DELETE_WINDOW", disable_event)
root.mainloop() #loop to update GUI

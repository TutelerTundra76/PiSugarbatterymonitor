#!/usr/bin/python
import time
import os
import signal
from subprocess import check_output


# Config
warning=0 #determines if the low battery warning is needed
CLIPS = 1 #enables the low battery warning

status = 0 #the curent battery %
debug = 0  #deterimines if it should print dbug statments 
iconState = ""
PNGVIEWPATH = "/home/pi/gbzbatterymonitor/Pngview/"
ICONPATH = "/home/pi/gbzbatterymonitor/icons"

REFRESH_RATE = 1 #intervieral between each check




def changeicon(percent):
    global iconState
    if iconState != percent:#if the icon needs to be changed
        iconState = percent#set icon state to what it should be
        i = 0
        killid = 0
        os.system(PNGVIEWPATH + "/pngview -b 0 -l 3000" + percent + " -x 650 -y 10 " + ICONPATH + "/battery" + percent + ".png &")#set icon
        out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True) #this lists processes searches for one containing "pngview" then outputs the second columnwitch is the pid of the process
        nums = out.split('\n')#gets rid of new line
        for num in nums:#kill the process
            i += 1
            if i == 1:
                killid = num
                os.system("sudo kill " + killid)


def endProcess(signalnum=None, handler=None):
    os.system("sudo killall pngview")
    exit(0)

# Initial Setup

signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)

# Begin Battery Monitoring

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999 -x 650 -y 10 " + ICONPATH + "/blank.png &")

while True:
    try:
        if os.system('echo "battery_charging" | sudo -nc -U /tmp/pisugar-server.sock')=="battery_charging: false":
            ret = os.system('echo "battery" | sudo -nc -U /tmp/pisugar-server.sock')
            ret =ret.remove("battery: ")
            if debug == 1:
                print(ret)
            if int(ret) <= 0:
                if status != 0:
                    status = 0
            elif int(ret) < 25:
                if status != 25:
                    changeicon("25")
                    if warning != 1:
                        if CLIPS == 1:
                            os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
                    warning = 1
                status = 25
            elif int(ret) < 50:
                if status != 50:
                    changeicon("50")
                status = 50
            elif int(ret) < 75:
                if status != 75:
                    changeicon("75")
                status = 75
            else:
                if status != 100:
                    changeicon("100")
                status = 100
        else:
            if status!=101:
                changeicon("charge")
            status = 101
        time.sleep(REFRESH_RATE)
    except ValueError:
        time.sleep(REFRESH_RATE)

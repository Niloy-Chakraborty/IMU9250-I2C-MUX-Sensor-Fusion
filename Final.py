#import required modules

import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import datetime
import time
import math
import smbus
import csv
from datetime import datetime

bus = smbus.SMBus(1)
global r1,r2,r3,p1,p2,p3,y1,y2,y3

def data_imu(i):
    global r1,r2,r3,p1,p2,p3,y1,y2,y3
    
    # Get the Current Time Stamp
    current = datetime.now()
    now=current.strftime("%H:%M:%S")
    
    #settings file for the IMU
    SETTINGS_FILE = "RTIMULib"
    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
      print("Settings file does not exist, will be created")
    s = RTIMU.Settings(SETTINGS_FILE)
    
    imu = RTIMU.RTIMU(s)
    if (not imu.IMUInit()):
        print("IMU Init Failed")
    else:
     print("IMU Init Succeeded")


    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    poll_interval = imu.IMUGetPollInterval()
    print("Recommended Poll Interval: %dmS\n" % poll_interval)
    while True:
       
            if imu.IMURead():
                x=0
                # x, y, z = imu.getFusionData()
                # print("%f %f %f" % (x,y,z))
                
                data = imu.getIMUData()
                fusionPose = data["fusionPose"]
                
                #convert radians to degree
                print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
                time.sleep(poll_interval*1.0/1000.0)
                r=(math.degrees(fusionPose[0]))
                p=(math.degrees(fusionPose[1]))
                y=(math.degrees(fusionPose[2]))
                
                if(i==0):
                  r1=r
                  p1=p
                  y1=y
                 
                elif (i==1):
                  r2=r
                  p2=p
                  y2=y
                 
                else: 
                  r3=r
                  p3=p
                  y3=y
                  
                  #Write data to file
                  header=['r1','p1','y1','r2','p2','y2','r3','p3','y3']
                  with open('data.csv','a') as f:
                        writer = csv.DictWriter(f,fieldnames=['time','r1','p1','y1','r2','p2','y2','r3','p3','y3'])
                        
                        writer.writerow({'time':now,'r1':r1,'p1':p1,'y1':y1,'r2':r2,'p2':p2,'y2':y2,'r3':r3,'p3':p3,'y3':y3})
                  f.close()
                  
                x=x+1
                if (x==1):
                    return
       
       


while True:
    i=0
    bus.write_byte_data(0x70, 0x04, 1) #Read IMU1
    print("IMU1")
    data_imu(i)
       
    bus.write_byte_data(0x70, 0x04, 2) #Read IMU2
    print("IMU2")
    i=i+1
    data_imu(i)
   
    bus.write_byte_data(0x70, 0x04, 3) #Read IMU3
    print("IMU3")
    i=i+1
    data_imu(i)
    
    

    
    
	
	
    

	
	
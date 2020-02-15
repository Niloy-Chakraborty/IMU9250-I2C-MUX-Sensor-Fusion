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
global r1,r2,r3,p1,p2,p3,y1,y2,y3,ax1,ay1,az1,gx1,gy1,gz1,mx1,my1,mz1,ax2,ay2,az2,gx2,gy2,gz2,mx2,my2,mz2,ax3,ay3,az3,gx3,gy3,gz3,mx3,my3,mz3

def data_imu(i):
    global r1,r2,r3,p1,p2,p3,y1,y2,y3,ax1,ay1,az1,gx1,gy1,gz1,mx1,my1,mz1,ax2,ay2,az2,gx2,gy2,gz2,mx2,my2,mz2,ax3,ay3,az3,gx3,gy3,gz3,mx3,my3,mz3
    
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
                a=data["accel"]
                g=data["gyro"]
                m=data["compass"]
                fusionPose = data["fusionPose"]
                
                #convert radians to degree
                print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
                print("a(x): %f a(y): %f a(z): %f g(x): %f g(y): %f g(z): %f m(x): %f m(y): %f m(z): %f" % (a[0],a[1],a[2],g[0],g[1],g[2],m[0],m[1],m[2]))
                time.sleep(poll_interval*1.0/1000.0)
                r=(math.degrees(fusionPose[0]))
                p=(math.degrees(fusionPose[1]))
                y=(math.degrees(fusionPose[2]))
                ax=a[0]
                ay=a[1]
                az=a[2]
                gx=g[0]
                gy=g[1]
                gz=g[2]
                mx=m[0]
                my=m[1]
                mz=m[2]
                
                if(i==0):
                  r1=r
                  p1=p
                  y1=y
                  ax1=ax
                  ay1=ay
                  az1=az
                  gx1=gx
                  gy1=gy
                  gz1=gz
                  mx1=mx
                  my1=my
                  mz1=mz
                  
                  
                 
                elif (i==1):
                  r2=r
                  p2=p
                  y2=y
                  ax2=ax
                  ay2=ay
                  az2=az
                  gx2=gx
                  gy2=gy
                  gz2=gz
                  mx2=mx
                  my2=my
                  mz2=mz
                 
                else: 
                  r3=r
                  p3=p
                  y3=y
                  ax3=ax
                  ay3=ay
                  az3=az
                  gx3=gx
                  gy3=gy
                  gz3=gz
                  mx3=mx
                  my3=my
                  mz3=mz
                  
                  #Write data to file
                  header=['time','r1','p1','y1','r2','p2','y2','r3','p3','y3']
                  with open('data.csv','a') as f:
                        writer = csv.DictWriter(f,fieldnames=['time','r1','p1','y1','r2','p2','y2','r3','p3','y3'])
                        
                        writer.writerow({'time':now,'r1':r1,'p1':p1,'y1':y1,'r2':r2,'p2':p2,'y2':y2,'r3':r3,'p3':p3,'y3':y3})
                  f.close()
                  header=['time','ax1','ay1','az1','gx1','gy1','gz1','mx1','my1','mz1','ax2','ay2','az2','gx2','gy2','gz2','mx2','my2','mz2','ax3','ay3','az3','gx3','gy3','gz3','mx3','my3','mz3']
                  with open('9axis.csv','a') as f1:
                        writer = csv.DictWriter(f1,fieldnames=['time','ax1','ay1','az1','gx1','gy1','gz1','mx1','my1','mz1','ax2','ay2','az2','gx2','gy2','gz2','mx2','my2','mz2','ax3','ay3','az3','gx3','gy3','gz3','mx3','my3','mz3'])
                        
                        writer.writerow({'time':now,'ax1':ax1,'ay1':ay1,'az1':az1,'gx1':gx1,'gy1':gy1,'gz1':gz1,'mx1':mx1,'my1':my1,'mz1':mz1,'ax2':ax2,'ay2':ay2,'az2':az2,'gx2':gx2,'gy2':gy2,'gz2':gz2,'mx2':mx2,'my2':my2,'mz2':mz2,'ax3':ax3,'ay3':ay3,'az3':az3,'gx3':gx3,'gy3':gy3,'gz3':gz3,'mx3':mx3,'my3':my3,'mz3':mz3})
                  f1.close()
                  
                x=x+1
                if (x==1):
                    return
       
# Kill the program automatically after 4 seconds     
stop_time = time.time() + 4

while time.time() < stop_time :
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
    
    
print("Stopping Auto-Feeder")
    
    
	
	
    

	
	
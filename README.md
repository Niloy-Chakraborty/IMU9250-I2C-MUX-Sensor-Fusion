# IMU9250-I2C-MUX-Sensor-Fusion
Python script for recording data from 3 IMU 9250 Sensors on RPI via MUX and Storing in CSV.

The IMU 9250 are connected to I2C Mux and  which is connected to the Raspberry pi 4.The data is recorded in CSV file .

## Attachents.
1. Python script-Using Kalman Flltering.

 2.Example data

### Dependencies
You must install the RTIMU Library and calibrate each sensor

In order to check if sensor and MUX are connected use the command  in terminal

i2cdetect -y 1

This should display 70 for the mux and  68 for IMU in the grid.
If not check your connections.

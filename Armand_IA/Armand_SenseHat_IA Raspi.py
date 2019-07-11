from picamera import PiCamera
from time import *
from sense_hat import SenseHat
from datetime import datetime
from csv import writer
import csv

sense = SenseHat()

cam = PiCamera()

def get_sense_data():
    sense_data = []
    sense_data.append(sense.get_temperature())
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())
    sense_data.append(sense.get_gyroscope_raw())
    sense_data.append(sense.get_orientation())
    sense_data.append(sense.get_compass_raw())
    sense_data.append(sense.get_accelerometer_raw())
    sense_data.append(datetime.now())

    orientation = sense.get_orientation()
    orientation['yaw']
    orientation['pitch']
    orientation['roll']
    mag = sense.get_compass_raw()
    mag['x']
    mag['y']
    mag['z']
    acc = sense.get_accelerometer_raw()
    acc['x']
    acc['y']
    acc['z']
    gyro = sense.get_gyroscope_raw()
    gyro['x']
    gyro['y']
    gyro['z']

    return sense_data

with open('data20.csv', 'w', newline='') as f:
    data_writer=writer(f)
    data_writer.writerow(['Temp', 'Pres', 'Hum',
                          'Gyroscope', 'Acceleration'])

    while True:
        cam.start_preview()
        sleep(2)
        cam.capture("/home/pi/Desktop/Armand_IA/example.jpg")
        cam.stop_preview()
        data = get_sense_data()
        data_writer.writerow(data)
        sleep(1)

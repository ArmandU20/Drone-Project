import RPi.GPIO as GPIO
import time
import dht11
import datetime
from picamera import PiCamera
from threading import *
import MySQLdb
import sys
# ------------------------------------Create Camera Instance----------------------------------------------
try:
    camera = PiCamera()
except:
    print "Failed to create PiCamera instance..."
    sys.exit(1)
finally:
    camera.resolution = (1024, 768)
# -----------------------------------GPIO Instances--------------------------------------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
# ------------------------------- MySQL Database credentials ----------------------------------------------
server = 'sql2.freemysqlhosting.net'
username = 'sql2286265'
pswd = 'tE6*aN5%'
database = 'sql2286265'
# ---------------------------------Attempt to connect to database -----------------------------------------
try:
    db = MySQLdb.connect(server, username, pswd, database)
except:
    "print Failed to connect to database. Exiting"
    sys.exit(1)
finally:
    cursor = db.cursor()
# ---------------------------------------------------------------------------------------------------------
TRIG = 23  # board pin no. 16
ECHO = 24  # board pin no. 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# read data from DHT11 using pin 14
instance = dht11.DHT11(pin=14)
# ----------------------------------------------------------------------------------------------------------


class DroneSensors:
    __arg = 0

    def __init__(self, arg):
        self.__arg = arg

    def read_proximity(self):

        GPIO.output(TRIG, False)  # Reset the sensor    #GPIO se poate pune can Instance var
        # print "Waiting For Sensor To Settle"
        time.sleep(1)
        # ---------------Trigger HC-SR04 Ultrasound sensor--------------------------------------------------
        GPIO.output(TRIG, True)
        time.sleep(0.00001)     # add delay of 10usec
        GPIO.output(TRIG, False)
        # --------------------------------------------------------------------------------------------------
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150  # Distance  = Speed x Time

        distance = round(distance, 2)  # Round the distance to 2 decimal places for clarity

        print "Distance:", distance, "cm"
        return distance
        # GPIO.cleanup()
# ---------------------------------------------------------------------------------------------------------
 
    def read_dht11(self):
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))      # print timestamp
            print("Temperature: %d C" % result.temperature)                 # print temperature readings
            print("Humidity: %d %%" % result.humidity)                      # print humidity readings
            time.sleep(1)
            return result.humidity, result.temperature                      # return valid DHT11 sensor data
        else:
            return 0
# ----------------------------------------------------------------------------------------------------------

    def capture(self):
        capture_timer = 10

        for timer in range(capture_timer, -1, -1):
            mins, secs = divmod(timer)                  # Get mins and secs left to capture again from camera
            time.sleep(1)
            if mins == 0 and secs == 0:                 # check if 10 secs are complete
                cap_time = datetime.datetime.now()
                cap_time = cap_time.strftime("%H_%M_%S")
                camera.capture(cap_time+'.jpg', resize=(320, 240),  use_video_port=True)    # capture from camera

# ----------------------Thread to capture from camera every 10 secs ----------------------------------------------

def capture_from_cam(inst_cam):
    while True:
        inst_cam.capture()
# ---------------------------------------------------------------------------------------------------------------


def main():
    inst_sensors = DroneSensors(arg=10)                             # Create Class instance
    t1 = Thread(target=capture_from_cam, args=(inst_sensors,))      # Create thread
    t1.daemon = True                                                # Make thread daemon
    t1.start()                                                      # start thread

    while True:
        distance = inst_sensors.read_proximity()                    # Get distance
        humidity, temperature = inst_sensors.read_proximity()       # Get Temp and Humidity

        my_time = datetime.datetime.now()               # Get Timestamp
        my_time = str(my_time.strftime("%H:%M:%S"))     # Format TIME

        query = "INSERT INTO drone_data (Timestamp, Proximity, Humidity, Temperature) VALUES (%s, %s, %s, %s)"
        val = [(my_time, str(distance) + ' cm', str(humidity) + ' %',  str(temperature) + ' Celsius')]

        cursor.executemany(query, val)                  # Query MySQL to send sensor data
        db.commit()                                     # Commit Query
        time.sleep(1)                                   # wait for 1 sec
# ---------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()


import RPi.GPIO as GPIO
from time import sleep, time

# constants
DEBUG = False # debug mode?
SETTLE_TIME = 2 # seconds to let the sensor settle
CALIBRATIONS = 5 # number of calibration measurements to take

CALIBRATION_DELAY = 1 # seconds to delay in between calibration measurements


TRIGGER_TIME = 0.00001 # seconds needed to trigger the sensor

                     # (to get a measurement)
SPEED_OF_SOUND = 343 # speed of sound in m/s

# set the RPi to the Broadcom pin layout
GPIO.setmode(GPIO.BCM)

# GPIO pins
TRIG = 18 # the sensor's TRIG pin
ECHO = 27 # the sensor's ECHO pin

GPIO.setup(TRIG, GPIO.OUT) # TRIG is an output
GPIO.setup(ECHO, GPIO.IN) # ECHO is an input
# calibrates the sensor
# technically, it returns a correction factor to use in our
# calculations
def calibrate():
  
    distance_avg = 0
    for i in range(CALIBRATIONS):
        distance = getDistance()
        if (DEBUG):
            print("--Got {}cm".format(distance))
        # keep a running sum
        distance_avg += distance
        # delay a short time before using the sensor again
        sleep(CALIBRATION_DELAY)

    # calculate the average of the distances
    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print("--Average is {}cm".format(distance_avg))
    
    # calculate the correction factor
    correction_factor = known_distance / distance_avg
    if (DEBUG):
        print("--Correction factor is \{}".format(correction_factor))
    print("Done.")
    print()

    return correction_factor

# uses the sensor to calculate the distance to an object
def getDistance():
    # trigger the sensor by setting it high for a short time and
    # then setting it low
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)
    
    # wait for the ECHO pin to read high
    # once the ECHO pin is high, the start time is set
    # once the ECHO pin is low again, the end time is set
    while (GPIO.input(ECHO) == 0):
        start = time()
    while (GPIO.input(ECHO) == 1):
        end = time()
        
    # calculate the duration that the ECHO pin was high
    # this is how long the pulse took to get from the sensor to
    # the object -- and back again
    duration = end - start
    # calculate the total distance that the pulse traveled by
    # factoring in the speed of sound (m/s)
    distance = (duration * SPEED_OF_SOUND) / 2
    
    return distance

########
# MAIN #
########
# first, allow the sensor to settle for a bit
try:
   while True:
       dist = getDistance()
       print("Measured Distance = %.1f cm" % dist")
       time.sleep(1)
except KeyboardInterrupt:
    print("STOP")
    GPIO.cleamup()

from random import randint
import keyboard
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

while True:
    Answer = input("Do you wanna start? Y or N ")

    while Answer == "Y":

        # run code for ultrasonic sensor

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        #set GPIO Pins
        GPIO_TRIGGER = 18
        GPIO_ECHO = 24
        LED_PIN = 27
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        GPIO.setup(LED_PIN, GPIO.OUT)
        
        def distance():
            # set Trigger to HIGH
            GPIO.output(GPIO_TRIGGER, True)
        
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)
        
            StartTime = time.time()
            StopTime = time.time()
        
            # save StartTime
            while GPIO.input(GPIO_ECHO) == 0:
                StartTime = time.time()
        
            # save time of arrival
            while GPIO.input(GPIO_ECHO) == 1:
                StopTime = time.time()
        
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
        
            return distance

        keyboard.wait("space")
        time.sleep(randint(2, 6))
        # start time/ turn on led
        time1 = time.time()
        GPIO.output(LED_PIN, GPIO.HIGH)
        

        
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(.1)
            if dist <= 100:
                # stop time
                time2 = time.time()
                # turn off led
                GPIO.output(LED_PIN, GPIO.LOW)
                # exit loop
                break
                
        # function that uses start and stop times to get the speed at which hand is moving        
        def GetVelocity(start, finish):
            # default distnace is 3 feet
            distance = 3        
            final_time = finish - start            
            # equation to get velocity from point A to point B
            speed = distance / final_time
            velocity = round(speed, 2) 
            
            return velocity
        
        
        # set variable to velocity to be used for GUI and animal search
        final_vel = GetVelocity(time1, time2)
       
        print(f"You were able to travel at a speed of {final_vel} ft/s")
        break


            

            

            
        

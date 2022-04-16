from random import randint
import RPi.GPIO as GPIO
import time
from tkinter import *
import random
from time import sleep

GPIO.setwarnings(False)

# mock dictionary
animal_List = {4 : "Elk.gif", 3 : "Gazelle.gif", 5 : "Lion.gif"}

x = None

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
        
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
LED_PIN = 27
        
# searches for closest number in the lsit based on the final_vel
def closest(test_dict, search_key):
    res = test_dict.get(search_key) or test_dict[min(test_dict.keys(),
                                                     key = lambda key: abs(key-search_key))]
    return res

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

# function that uses start and stop times to get the speed at which hand is moving        
def GetVelocity(start, finish):
    # default distnace is 3 feet
    distance = 20        
    final_time = finish - start
    print(f"{final_time}")
    # equation to get velocity from point A to point B
    fts_speed = distance / final_time
            
    # converts from feet per second to miles per hour
    mph_speed = fts_speed * 0.681818
            
    return mph_speed


def sound():
    global animal_List
    global x
    # run code for ultrasonic sensor
    
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)

    time.sleep(randint(2, 6))
    # start time/ turn on led
    time1 = time.time()
    GPIO.output(LED_PIN, GPIO.HIGH)
        
    while True:
        dist = distance()
        time.sleep(.1)
        if dist <= 100:
            # stop time
            time2 = time.time()
            # turn off led
            GPIO.output(LED_PIN, GPIO.LOW)
            # exit loop
            break

    # set variable to velocity to be used for GUI and animal search
    final_vel = GetVelocity(time1, time2)
    print(f"{final_vel}")
    
    animal_pic = closest(animal_List, final_vel)

    # next just call the animal image from the dictionary using the new key (speed)
    x = animal_pic

# function to open a new window
# on a button click
def openNewWindow():
    newWindow = Toplevel()
    newWindow.title("New Window")
    newWindow.attributes('-fullscreen', True)
    newWindow.geometry("400x150")
    sound()
    
    #Label(newWindow, text = f"{x}").pack()
    #tkWindow.withdraw()

    img=PhotoImage(file=f'{x}')
    sub = img.subsample(5, 5)
    ln = Label(newWindow, image=sub)
    ln.image = sub
    ln.grid(row=6)

    Button(newWindow, text='restart', command=newWindow.destroy).grid(row =5, columnspan=2)

tkWindow = Tk()  
tkWindow.geometry('400x150')  
tkWindow.attributes('-fullscreen', True)
tkWindow.title('PythonExamples.org - Tkinter Example')
  
button = Button(tkWindow, text = 'Submit', bg='red', activebackground='green', command = openNewWindow)  
button.pack()  
button2 = Button(tkWindow, text = 'QUIT', command= tkWindow.destroy)
button2.pack()
  
tkWindow.mainloop()
                

            

            
        

########################################################################
# Isaac Guidry, Dang Do, Cooper Rachow
# 04/28/2022
# Program that calculates the speed of a punch and maps it to an animal
########################################################################

# Imports 
from random import randint
import RPi.GPIO as GPIO
import time
from tkinter import *
import random
from time import sleep

# disables warnings
GPIO.setwarnings(False)

# animal dictionary with speed: [video, animal name]
animal_dict = {4 : ["Elk.gif", "Elk"], 3 : ["Gazelle.gif", "Gazelle"], 5 : ["Lion.gif", "Lion"]}

# varibales here are created as place holders for values; and set to none
x = None
y = None

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
        
#set GPIO Pins
# ultrasonic sensor
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# leds
red1_LED = 27
green1_LED = 13
red2_LED = 26
green2_LED = 12
        
# searches for closest number in the list based on the final_vel
def closest(test_dict, search_key):
    res = test_dict.get(search_key) or test_dict[min(test_dict.keys(), key = lambda key: abs(key-search_key))]
    return res

# function that calculates the distance the sensor is from a an object
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
        
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
        
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

# function that will return a video and animal name according to the distance and time calculated 
def speed():
    global animal_dict
    global x
    global y
    # run code for ultrasonic sensor
    
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(red_LED1, GPIO.OUT)
    GPIO.setup(green_LED1, GPIO.OUT)
    GPIO.setup(red_LED2, GPIO.OUT)
    GPIO.setup(green_LED2, GPIO.OUT)

    time.sleep(randint(2, 6))
    # start time/ turn on green led
    time1 = time.time()

    # green leds turn on 
    GPIO.output(green_LED1, GPIO.HIGH)
    GPIO.output(green_LED2, GPIO.HIGH)    
        
    while True:
        # call distance function
        dist = distance()
        time.sleep(.1)
        if dist <= 100:
            # stop time
            time2 = time.time()
            # turn off green led
            GPIO.output(green_LED1, GPIO.LOW)
            GPIO.output(green_LED2, GPIO.LOW)    
            # turn on red led
            GPIO.output(red_LED1, GPIO.HIGH)
            GPIO.output(red_LED2, GPIO.HIGH)
            # exit loop
            break

    # set variable to velocity to be used for GUI and animal search
    final_vel = GetVelocity(time1, time2)
    print(f"{final_vel}")
    
    # value of dictionary is mapped to the the key(speed) that is returned by the closest() function
    animal_pic = closest(animal_dict, final_vel)

    # next just call the animal image from the dictionary using the new key (speed)
    x = animal_pic[0] # video
    y = animal_pic[1] # name of animal

# function to create a new GUI on top of the existing GUI
def second_Gui():
    # global functions changes variables created in the begining of the program
    global x
    global y
    newWindow = Toplevel()
    newWindow.title("Results")
    newWindow.attributes('-fullscreen', True)
    newWindow.geometry("400x150")
        
    # call speed function 
    speed()
    
    # this picture serves as the background image
    picture = PhotoImage(file = "faded_forest2.png")
    my_label = Label(newWindow, image=picture)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    # This will display the name of the animal calculated
    text = Label(newWindow, text="Wow! " + y + " like speed!", font=('Helvetica', 25), fg="dark green")
    text.place(x=275, y=420)
    ln = Label(newWindow)
    ln.place(x=100, y=50)
    
    # plays the video of the animal chosen/calculated in this GUI
    player = tkvideo(x, ln, loop = 1, size= (600,350))
    player.play()

    # Restart button that destroys the 2nd GUI (This one) and returns user to first GUI
    Button(newWindow, text='RESTART', bg='red', height = 3, width = 5, command=newWindow.destroy).place(x=45, y=409)
    newWindow.mainloop()


##################################
# MAIN part of the PROGRAM
##################################
# first GUI
tkWindow = Tk()
tkWindow.geometry('400x150')  
tkWindow.attributes('-fullscreen', True)
tkWindow.title('Speed Test')

# this picture serves as the background image
picture = PhotoImage(file = "faded_forest2.png")
my_label = Label(tkWindow, image=picture)
my_label.place(x=0, y=0, relwidth=1, relheight=1)
 
fnt = font.Font(family='Times New Roman', size=30) 

# displays two buttons a start buttona and a quit button
# on pressing the start button, the second_Gui function is called and th second GUI will be displayed
button = Button(tkWindow, text = 'Start!', bg='red', activebackground='green', command = second_Gui, height = 2, width = 7)
button['font'] = fnt
button.pack(padx = 100, pady = 100)

fnt2 = font.Font(size=20) 
# on pressing the quit button, the program is eneded 
button2 = Button(tkWindow, text = 'QUIT',activebackground='gray', command= tkWindow.destroy)
button2['font'] = fnt2
button2.pack()
  
tkWindow.mainloop()
                

            

            
        

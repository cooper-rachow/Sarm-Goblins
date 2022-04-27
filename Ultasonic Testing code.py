from random import randint
import RPi.GPIO as GPIO
import time
from tkinter import *
import random
from time import sleep

GPIO.setwarnings(False)

# mock dictionary
animal_dict = {4 : ["Elk.gif", "Elk"], 3 : ["Gazelle.gif", "Gazelle"], 5 : ["Lion.gif", "Lion"]}

x = None
y = None

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
        
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
red1_LED = 27
green1_LED = 13
red2_LED = 26
green2_LED = 12
        
# searches for closest number in the lsit based on the final_vel
def closest(test_dict, search_key):
    res = test_dict.get(search_key) or test_dict[min(test_dict.keys(), key = lambda key: abs(key-search_key))]
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
    GPIO.output(green_LED1, GPIO.HIGH)
    GPIO.output(green_LED2, GPIO.HIGH)    
        
    while True:
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
    
    animal_pic = closest(animal_dict, final_vel)

    # next just call the animal image from the dictionary using the new key (speed)
    x = animal_pic[0] # video
    y = animal_pic[1] # name of animal

# function to open a new window
# on a button click
def openNewWindow():
    global x
    global y
    newWindow = Toplevel()
    newWindow.title("Results")
    newWindow.attributes('-fullscreen', True)
    newWindow.geometry("400x150")
    sound()
    
    picture = PhotoImage(file = "faded_forest2.png")
    my_label = Label(newWindow, image=picture)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    text = Label(newWindow, text="Wow! " + y + " like speed!", font=('Helvetica', 25), fg="dark green")
    text.place(x=275, y=420)
    ln = Label(newWindow)
    ln.place(x=100, y=50)
    
    player = tkvideo(x, ln, loop = 1, size= (600,350))
    player.play()

    Button(newWindow, text='RESTART', bg='red', height = 3, width = 5, command=newWindow.destroy).place(x=45, y=409)
    newWindow.mainloop()
    
tkWindow = Tk()
tkWindow.geometry('400x150')  
tkWindow.attributes('-fullscreen', True)
tkWindow.title('Speed Test')

picture = PhotoImage(file = "faded_forest2.png")
my_label = Label(tkWindow, image=picture)
my_label.place(x=0, y=0, relwidth=1, relheight=1)
 
fnt = font.Font(family='Times New Roman', size=30) 
button = Button(tkWindow, text = 'Start!', bg='red', activebackground='green', command = openNewWindow, height = 2, width = 7)
button['font'] = fnt
button.pack(padx = 100, pady = 100)
fnt2 = font.Font(size=20) 
button2 = Button(tkWindow, text = 'QUIT',activebackground='gray', command= tkWindow.destroy)
button2['font'] = fnt2
button2.pack()
  
tkWindow.mainloop()
                

            

            
        

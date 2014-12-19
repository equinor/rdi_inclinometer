import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# Set up channel 23 INPUT - PULL UP
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pressed_time_for_horizon_sec = 1 #secs

time_stamp = -1
time_stamp_last_obs = -1

counter = 1

def button_pressed(channel):
    global time_stamp, time_stamp_last_obs, counter

    status = GPIO.input(channel)
    if(status):
        return
    
    print("\n**%d** - Channel: %d - Input: %d" % (counter, channel, status))
    time_stamp = time.time()
    counter = counter +1

    while (GPIO.input(channel) == 0) :
        time.sleep(0.01)

    time_stamp_last_obs = time.time()
    pressed_time = time_stamp_last_obs - time_stamp
    print("Pressed Time: %d msec" % (pressed_time*1000))
    if(pressed_time < pressed_time_for_horizon_sec):
        print("Processing a MEASUREMENT Obs....")
    else:
        print("Processing a HORIZON Obs....")
    

GPIO.add_event_detect(23, GPIO.FALLING, callback=button_pressed, bouncetime = 60)

print "Waiting for Button Action on port 23!"
raw_input("Press enter to Exit!\n")

GPIO.cleanup()

                       

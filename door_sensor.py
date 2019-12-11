import RPi.GPIO as GPIO
import time

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM) 
# This is the GPIO pin number we have one of the door sensor
# wires attached to, the other should be attached to a ground #
DOOR_SENSOR_PIN = 17
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
while True:
	ope = (GPIO.input(DOOR_SENSOR_PIN))
	if(ope):
		print("door is open")
	time.sleep(0.5)

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) 
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
state = "AT HOME"
bu = 1
while(True):
	for t in range(0,600000):
		button = (GPIO.input(BUTTON_PIN))
		if(button == 0):
			bu = 0
	if (bu == 0):
		if(state == "AT HOME"):
			state = "NOT HOME"
		else:
			state = "AT HOME"
	print(state)
	bu = 1
	#time.sleep(0.1)
GPIO.cleanup()  

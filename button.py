import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) 
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
state = "AT HOME"
bu = 1
while(True):
	button = (GPIO.input(BUTTON_PIN))
	print(button)
	time.sleep(0.1)
GPIO.cleanup()  

# Getting the libraries we need
from gpiozero import DistanceSensor
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("pi-server.local", 1883, 60)
print("connected")
# Initialize ultrasonic sensor
GPIO.setmode(GPIO.BCM) 
DOOR_SENSOR_PIN = 17
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
topic = "client2"
pir = MotionSensor(4)
t = 0
while True:
	# Wait 2 seconds
	time.sleep(1)
	# Print the information to the screen
	#client.publish(topic, "Distance: {} cm". format(distance))
	#if pir.motion_detected:
	#	print('Motion detected')
		#client.publish(topic, "Motion detected")
	ope = (GPIO.input(DOOR_SENSOR_PIN))
#	distance = round(sensor.distance * 100, 2)
	
	if(ope):
		print("door is open")
		#print("Distance: {} cm". format(distance))
		if pir.motion_detected:
			#print(t)
			t += 1
			if(t == 1):
			#print('Motion detected')
			#if (distance < 100):
				client.publish(topic,"INTRUDER ALERT!")
				print("INRUDER ALERT")
		else:
			
			t = 0
	else:
		t = 0
        
GPIO.cleanup()  



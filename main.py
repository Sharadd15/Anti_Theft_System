4# Getting the libraries we need
from gpiozero import DistanceSensor
from gpiozero import MotionSensor
import time
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("pi-server.local", 1883, 60)
print("connected")
# Initialize ultrasonic sensor
sensor = DistanceSensor(trigger=18, echo=24)
topic = "client2"
pir = MotionSensor(4)
while True:
	# Wait 2 seconds
	time.sleep(2)
	
	# Get the distance in metres
	#distance = sensor.distance

	# But we want it in centimetres
	#distance = sensor.distance * 100

	# We would get a large decimal number so we will round it to 2 places
	distance = round(sensor.distance * 100, 2)

	# Print the information to the screen
	print("Distance: {} cm". format(distance))
	client.publish(topic, "Distance: {} cm". format(distance))
	if pir.motion_detected:
		print('Motion detected')
		client.publish(topic, "Motion detected")
        
GPIO.cleanup()  



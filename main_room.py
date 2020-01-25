from gpiozero import DistanceSensor
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("pi-server.local", 1883, 60)
print("connected")
topic = "client1"
pir = MotionSensor(4)
t = 0
while True:
	time.sleep(1)
	if pir.motion_detected:
		t += 1
		if(t == 1):
			client.publish(topic,"INTRUDER ALERT FROM Roof-sensor!")
			print("INTRUDER ALERT FROM Roof-sensor!")
	else:
		t = 0

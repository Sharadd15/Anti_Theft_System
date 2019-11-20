import time
from gpiozero import MotionSensor
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("pi-server.local", 1883, 60)
print("connected")
pir = MotionSensor(4)
time.sleep(2)
topic = "client1"
while True:
    if pir.motion_detected:
        print('Motion detected')
        client.publish(topic, "Motion detected")
        time.sleep(2)

GPIO.cleanup()  

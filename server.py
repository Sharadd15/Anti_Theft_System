import paho.mqtt.client as mqtt
import time
from picamera import PiCamera
client = mqtt.Client()
camera = PiCamera() 
def on_message(client, userdata, message):
    print "Message received: "  + message.payload
    if message.payload == "INTRUDER ALERT!":
        camera.start_preview()
        time.sleep(5)
        camera.capture('pict/image.jpeg')
        camera.stop_preview()
client.on_message= on_message   
client.connect("pi-server.local", 1883, 60)
print("connected")
client.loop_start()        #start the loop 
 
client.subscribe("client2")
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()

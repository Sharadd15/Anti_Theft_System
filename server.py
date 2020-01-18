import paho.mqtt.client as mqtt
import time
import datetime
from picamera import PiCamera
import firebase_admin
from firebase_admin import credentials, firestore, storage

client = mqtt.Client()
camera = PiCamera() 

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
bucket = storage.bucket('smart-anti-theft.appspot.com')

def on_message(client, userdata, message):
    print "Message received: "  + message.payload
    if message.payload == "INTRUDER ALERT FROM FRONT DOOR!":
        camera.start_preview()
        time.sleep(5)
        now = datetime.datetime.now()
        pic_path = "pict/" + str(now) + ".jpg"
        camera.capture(pic_path)
        camera.stop_preview()
        db.collection(u'alerts').add({
            u'timestamp': now,
            u'location': u'Front door'
        })

        blob = bucket.blob(str(now) + ".jpg")
        blob.upload_from_filename(pic_path)
    
    if message.payload == "INTRUDER ALERT FROM WINDOW!":
        camera.start_preview()
        time.sleep(5)
        now = datetime.datetime.now()
        pic_path = "pict/" + str(now) + ".jpg"
        camera.capture(pic_path)
        camera.stop_preview()
        db.collection(u'alerts').add({
            u'timestamp': now,
            u'location': u'Window'
        })

        blob = bucket.blob(str(now) + ".jpg")
        blob.upload_from_filename(pic_path)
    
client.on_message= on_message   
client.connect("pi-server.local", 1883, 60)
print("connected")
client.loop_start()
client.subscribe("client2")
client.subscribe("client3")
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()

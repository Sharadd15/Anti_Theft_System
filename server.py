import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import datetime
import pytz
from picamera import PiCamera
import firebase_admin
from firebase_admin import credentials, firestore, storage, messaging

GPIO.setmode(GPIO.BCM) 
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
old_state = False
current_state = True
client = mqtt.Client()
camera = PiCamera() 
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
bucket = storage.bucket('smart-anti-theft.appspot.com')
tok = db.collection(u'users').document(u'testuser').get().to_dict()['token']

def on_message(client, userdata, message):

    if ((message.payload == "INTRUDER ALERT FROM Roof-sensor!") & (current_state == True)):
        print ("Message received: "  + message.payload)
        camera.start_preview()
        time.sleep(5)
        now = datetime.datetime.utcnow()
        pic_path = "pict/" + now.strftime("%Y-%m-%d %H:%M:%S") + ".jpg"
        camera.capture(pic_path)
        camera.stop_preview()
        db.collection(u'alerts').add({
            u'timestamp': now,
            u'location': u'Roof-sensor'
        })
        noti = messaging.Message(
            token = tok,
            notification = messaging.Notification(title = "INTRUDER ALERT", body = "Roof sensor")
        )
        messaging.send(noti)
        blob = bucket.blob(now.strftime("%Y-%m-%d %H:%M:%S") + ".jpg")
        blob.upload_from_filename(pic_path)

    if message.payload == "INTRUDER ALERT FROM FRONT DOOR!":
        print ("Message received: "  + message.payload)
        camera.start_preview()
        time.sleep(5)
        now = datetime.datetime.utcnow()
        pic_path = "pict/" + now.strftime("%Y-%m-%d %H:%M:%S") + ".jpg"
        camera.capture(pic_path)
        camera.stop_preview()
        db.collection(u'alerts').add({
            u'timestamp': now,
            u'location': u'Front-Door'
        })
        noti = messaging.Message(
            token = tok,
            notification = messaging.Notification(title = "INTRUDER ALERT", body = "Roof sensor")
        )
        messaging.send(noti)
        blob = bucket.blob(now.strftime("%Y-%m-%d %H:%M:%S") + ".jpg")
        blob.upload_from_filename(pic_path)
    
    if message.payload == "INTRUDER ALERT FROM WINDOW!":
        print ("Message received: "  + message.payload)
        camera.start_preview()
        time.sleep(5)
        now = datetime.datetime.utcnow()
        pic_path = "pict/" + now.strftime("%Y-%m-%d %H:%M:%S") + ".jpg"
        camera.capture(pic_path)
        camera.stop_preview()
        db.collection(u'alerts').add({
            u'timestamp': now,
            u'location': u'Window'
        })
        noti = messaging.Message(
            token = tok,
            notification = messaging.Notification(title = "INTRUDER ALERT", body = "Roof sensor")
        )
        messaging.send(noti)
        blob = bucket.blob(now.strftime("%Y-%m-%d %H:%M:%S") + ".jpg")
        blob.upload_from_filename(pic_path)
    
client.on_message= on_message   
client.connect("pi-server.local", 1883, 60)
print("connected")
client.loop_start()
client.subscribe("client1")
client.subscribe("client2")
client.subscribe("client3")
print(tok)
try:
    while True:
        old_state = current_state
        print(current_state)
        current_state = GPIO.input(BUTTON_PIN)
        if((old_state == False) & (current_state == True)):
            client.unsubscribe("client1")
            client.unsubscribe("client2")
            client.unsubscribe("client3")
            time.sleep(10)
            client.subscribe("client1")
            client.subscribe("client2")
            client.subscribe("client3")
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()

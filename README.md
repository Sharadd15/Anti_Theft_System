# Smart Anti_Theft_System
# Introduction:
This is a system to detect intruder in house/office. This system is implemented for one room house but can be very easily extended for multi room house. Whenever there is any unknown person entering the house the system will capture the picture wherever is the intrusion (from main door/window/roof(in case there is miss from the other two)) and sends the picture to the owner of the house on the android application on phone and also informs about the point of intrusion
For more information look in the [report](https://github.com/Sharadd15/Anti_Theft_System/blob/master/IoT%20Project%20Report%20SAT%20system.pdf)

# The hardware connections
***The connections are according to the code. If changes are made in the connections corresponding changes must be made in the code.***
There are 4 rpis which are used as server and the other nodes. The image below is refernce for all connection:
![alt text](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Header-with-Photo.png "rpi pin diagram")
### 1. The Server node:
This is main node connected to the internet and should have hotspot enabled and the rest of the noded must be connected via hotspot to server node. The camera(Night vision, normal can also be used) is connected as shown in figure below:
![alt text](https://dab1nmslvvntp.cloudfront.net/wp-content/uploads/2015/07/1436675540rpicamconnector.jpg "Camera connection")
Toggle  button is connected to the server node, it is turned **ON** when person leaves the house and turned off when person is in the house. The button signal node should be connected to GPIO17 or pin number 11.

### 2. Window and Door:
The following connection should be used for both rpi which is monitoring intruder detection on Door and Window. 
1. Contact Sensor: The ground and vcc can be connected to any vcc and ground terminal on rpi. The SIG is connected to GPIO 17. Any magnet can be used for this sensor
2. Motion Sensor: The SIG of PIR motion sensor is connected to GPIO4. The Ground and VCC can be connected to any Ground and 5volts power supply in the rpi

### 3. Roof:
This is installed on the roof to detect the motion in the room. Following Connections are made for the sensors:
1. PIR Motion Sensor: The SIG of PIR motion sensor is connected to GPIO4. The Ground and VCC can be connected to any Ground and 5volts power supply in the rpi

# Software Installation:
The raspbian OS should be installed on all 4 rpis, follow this link for [installation](https://thepi.io/how-to-install-raspbian-on-the-raspberry-pi/). Python 2 is used in all rpis.
### 1. Server Node: 
* Name the Server Node as "pi-server". 
* Install MQTT broker by following this [link](https://www.vultr.com/docs/how-to-install-mosquitto-mqtt-broker-server-on-ubuntu-16-04).
* Install following python libraries using pip:
paho-mqtt
datetime
pytz
firebase_admin
* Now Run server.py as:
    python server.py

### 2. Roof Node:
* Name the Roof node as "client1".
* Install following python libraries:
    gpiozero
    paho-mqtt
* Now Run main_room.py as:
    python main_room.py

### 3. Door Node:
* Name the Door node as "client2".
* Install following libraries:
    gpiozero
    paho-mqtt
* Now Run main_door.py as:
    python main_door.py

### 3. Window Node:
* Name the Door node as "client3".
* Install following libraries:
    gpiozero
    paho-mqtt
* Now Run main_window.py as:
    python main_window.py



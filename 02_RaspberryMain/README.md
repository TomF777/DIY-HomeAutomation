### Main RPi of the home automation system.

This RPi communicates with RPi from living room and bedroom via MQTT.
It also handles data exchange with series of small RP2040's via simple 
self-developed software protocol over RS485 media.

Python scripts are running as services after system start-up.

Following services are configured (see `services_configuration` folder in this repo):
 - `mqtt_publisher.service` : serial communication (USB0 -> RS485) - ttyUSB0
		                it starts **./home_automation_project/src/mqtt_publisher.py**

 - `mqtt_subscriber.service` : mqtt communication with RPi in living room and OrangePiZero in bed room.
 It starts **./home_automation_project/src/mqtt_subscriber.py** to collect the data.

 - `alarm_handler.service` : alarm handler, motion detection, door open detection. It starts **./home_automation_project/src/alarm_handler.py**

 - `zigbee_handler.service` : serial data over UART0 from ZigBee coordinator. It starts **./home_automation_project/src/zigbee_handler.py**

- `flask_visu.service` : Flask web server for visualisation. It starts **./home_automation_project/src/flask_visu/app.py**

- `mosquitto.service` : runs automatically mqtt broker

- `grafana-server.service` : runs automatically Grafana ver. 11

- `camera_handler.service` : runs camera web streaming & motion detection. It starts **./home_automation_project/src/picamera_motion/picamera_motion_stream.py**

All services must be located in folder `/lib/systemd/system/` on the target RPi.
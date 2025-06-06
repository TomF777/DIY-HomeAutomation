### RPi located in living room.

This RPi publishes sensor data (JSON as MQTT message) to main RPi.

Python script runs as service after system start-up.

Following services are configured (see `services_configuration` folder in this repo):
 - `mqtt_client.service` : it starts **./home_automation_project/src/mqtt_publisher.py**


All services must be located in folder `/lib/systemd/system/` on the target RPi.
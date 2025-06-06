#!/usr/bin/env python3.10

""" 
    Script collects data over mqtt from all sensors and RPi's,
    processes it and writes to MySQL database.
    This script must be run prior to the Flask app due to the shared memory dict. 
    shared memory dict passes data from this script to Flask app.
    Requires Python 3.10 or higher
"""

import json
import time
import logging
from datetime import datetime
from threading import Thread
import paho.mqtt.client as mqtt_client
import MySQLdb
from shared_memory_dict import SharedMemoryDict
import service_monitor
import aux_modules

logging.basicConfig(level=logging.DEBUG)

# mqtt settings
BROKER_HOST = "192.168.1.165"
BROKER_PORT = 1883
BROKER_USERNAME = '***'
BROKER_PASSWORD = '***'
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

# MySQL settings
MYSQL_HOST = "localhost"
MYSQL_USER = "***"
MYSQL_PASSWORD = "***"
MYSQL_DB_NAME = "db_home_automation"


class MqttDataSubscriber():
    """
    Subscribe to defined mqtt topics,
    process incoming mqtt messages and saved them into MySQL.
    Timers are defined for logging intervals into MySQL.  
    Timers-lifebits for monitoring of connection status with devices.
    """
    def __init__(self):
        self.services_status = {}
        self.alarm_enabled = 0
        self.camera_enabled = 0
        self.alarm_detected = 0
        self.el_integral_L1 = 0
        self.el_integral_L2 = 0
        self.el_integral_L3 = 0
        self.outdoor_pressure = 0

        # shared memory object to pass data to Flask app
        self.sh_mem_dict_config = SharedMemoryDict(name='config', size=600)

        # timers to define time interval of writing data to MySQL
        self.timer_living_room = aux_modules.Timer()
        self.timer_kitchen = aux_modules.Timer()
        self.timer_kitchen_zigbee = aux_modules.Timer()
        self.timer_bath_room = aux_modules.Timer()
        self.timer_bath_room_zigbee = aux_modules.Timer()
        self.timer_bed_room = aux_modules.Timer()
        self.timer_out_pm = aux_modules.Timer()
        self.timer_electric = aux_modules.Timer()
        self.timer_outdoor = aux_modules.Timer()
        self.timer_alarm_status = aux_modules.Timer()

        self.timer_motion_kitchen = aux_modules.Timer()
        self.timer_motion_living = aux_modules.Timer()
        self.timer_fridge_door_opened = aux_modules.Timer()

        # timers for life bit from RPis
        self.timer_lifebit_bedroom = aux_modules.Timer()
        self.timer_lifebit_livingroom = aux_modules.Timer()

        # timers for life bit from RP2040 Zero's
        self.timer_lifebit_kitchen = aux_modules.Timer()
        self.timer_lifebit_bathroom = aux_modules.Timer()
        self.timer_lifebit_el_switchboard = aux_modules.Timer()

        self.timer_lifebit_light_switch_kitchen = aux_modules.Timer()
        self.timer_lifebit_light_switch_living_room = aux_modules.Timer()
        self.timer_lifebit_light_switch_bed_room = aux_modules.Timer()

        self.mqtt_client = None

        # run service status check in background
        t_service_status = Thread(target=self.get_service_status, args=())
        t_service_status.daemon = False
        t_service_status.start()

        # run sharing data to Flask in background
        t_share_status_to_flask = Thread(target=self.share_status_to_flask, args=())
        t_share_status_to_flask.daemon = False
        t_share_status_to_flask.start()

        #t_service_status.join()
        #t_share_status_to_flask.join()

    def on_mqtt_connect(self, mqtt_client, userdata, flags, rc, props):
        """
        Called when MQTT connection successfully established
        """
        if rc == 0:
            print("Connected to MQTT Broker")

            # Subscribing in on_mqtt_connect() ensures that if connection is lost and
            # reconnected again the subscriptions will be renewed.
            mqtt_client.subscribe([ ("HomeAutomation/LivingRoom/#",1),
                            ("HomeAutomation/BedRoom/#",1),
                            ("HomeAutomation/OutdoorPM/#",1),
                            ("HomeAutomation/Kitchen/#",1),
                            ("HomeAutomation/Bathroom/#",1),
                            ("HomeAutomation/Outdoor/#",1),
                            ("HomeAutomation/Electric/#",1),
                            ("HomeAutomation/AlarmStatus",1)])
        else:
            print(f"Failed to connect to MQTT Broker, error code: {rc}")
            if rc==1:
                print("1: Connection refused - incorrect protocol version")
            elif rc==2:
                print("2: Connection refused - invalid client identifier")
            elif rc==3:
                print("3: Connection refused - server unavailable")
            elif rc==4:
                print("4: Connection refused - bad username or password")
            elif rc==5:
                print("5: Connection refused - not authorised")
            time.sleep(1)

    def on_mqtt_message(self, client, userdata, message):
        """
        Called when MQTT message received
        """
        logging.debug("mqtt topic: %s : mqtt payload: %s", message.topic, message.payload.decode('utf-8'))

        json_msg = json.loads(message.payload.decode("utf-8"))

        match message.topic:
            case "HomeAutomation/LivingRoom":
                self.outdoor_pressure = json_msg["pressure"]

                # restart the timer when mqtt message received
                self.timer_lifebit_livingroom.stop()
                self.timer_lifebit_livingroom.start()

                # 2min time data polling
                if self.timer_living_room.elapsed_time > 120:
                    self.timer_living_room.stop()
                    self.timer_living_room.start()
                    sql_write_trig = True
                else:
                    sql_write_trig = False

                # write sensor motion with max. resolution of 60 sec. to SQL DB
                if str(json_msg["motion_sensor"]) == '1' \
                    and self.timer_motion_living.elapsed_time == 0.0:
                    self.timer_motion_living.start()
                    self.write_to_mysql('room_living',
                                Temperature=json_msg["temperature"],
                                Humidity=json_msg["humidity"],
                                Motion=json_msg["motion_sensor"],
                                PM1=json_msg["pm1"],
                                PM2_5=json_msg["pm2.5"],
                                PM10=json_msg["pm10"],
                                Timestamp = datetime.now() )

                elif (str(json_msg["motion_sensor"]) == '1' and \
                    self.timer_motion_living.elapsed_time > 60) or \
                    sql_write_trig is True:
                    self.write_to_mysql('room_living',
                                    Temperature=json_msg["temperature"],
                                    Humidity=json_msg["humidity"],
                                    Motion=json_msg["motion_sensor"],
                                    PM1=json_msg["pm1"],
                                    PM2_5=json_msg["pm2.5"],
                                    PM10=json_msg["pm10"],
                                    Timestamp = datetime.now() )

                    if self.timer_motion_living.elapsed_time == 0.0:
                        self.timer_motion_living.start()
                    else:
                        self.timer_motion_living.stop()
                        self.timer_motion_living.start()

            case "HomeAutomation/BedRoom":

                # restart the timer when mqtt message received
                self.timer_lifebit_bedroom.stop()
                self.timer_lifebit_bedroom.start()

                # 2min.  time data polling
                if self.timer_bed_room.elapsed_time > 120:
                    self.timer_bed_room.stop()
                    self.timer_bed_room.start()
                    self.write_to_mysql('room_bedroom',
                                Temperature=json_msg["temperature"],
                                Humidity=json_msg["humidity"],
                                Motion=json_msg["motion_sensor"],
                                PM1=json_msg["PM1_in"],
                                PM2_5=json_msg["PM2.5_in"],
                                PM10=json_msg["PM10_in"],
                                Timestamp = datetime.now() )

            case "HomeAutomation/OutdoorPM":
                # 2min. time data polling
                if self.timer_out_pm.elapsed_time > 120:
                    self.timer_out_pm.stop()
                    self.timer_out_pm.start()
                    self.write_to_mysql('generic_outside_particulate_matter',
                                PM1=json_msg["PM1_out"],
                                PM2_5=json_msg["PM2.5_out"],
                                PM10=json_msg["PM10_out"],
                                Timestamp = datetime.now() )

            case "HomeAutomation/Outdoor":
                # 2min. time data polling
                if self.timer_outdoor.elapsed_time > 120:
                    self.timer_outdoor.stop()
                    self.timer_outdoor.start()

                    if self.outdoor_pressure is not None and self.outdoor_pressure != 0:
                        self.write_to_mysql('generic_outside_conditions',
                                    Temperature=json_msg["temperature"],
                                    Humidity=json_msg["humidity"],
                                    Pressure=self.outdoor_pressure,
                                    Timestamp = datetime.now() )

            case "HomeAutomation/Bathroom":

                # restart the timer when mqtt message received
                self.timer_lifebit_bathroom.stop()
                self.timer_lifebit_bathroom.start()

                # 2min. time data polling
                if self.timer_bath_room.elapsed_time > 120:
                    self.timer_bath_room.stop()
                    self.timer_bath_room.start()
                    self.write_to_mysql('room_bathroom',
                                Temperature=json_msg["temperature"],
                                Humidity=json_msg["humidity"],
                                Timestamp = datetime.now() )

            case "HomeAutomation/Bathroom/ZigBee":
                # 2min. time data polling
                if self.timer_bath_room_zigbee.elapsed_time >60:
                    self.timer_bath_room_zigbee.stop()
                    self.timer_bath_room_zigbee.start()
                    self.write_to_mysql('room_bathroom_zigbee',
                                Fan_Vib_X=json_msg["fan_vibration_axis_x"],
                                Fan_Vib_Y=json_msg["fan_vibration_axis_y"],
                                Fan_Vib_Z=json_msg["fan_vibration_axis_z"],
                                Timestamp = datetime.now() )

            case "HomeAutomation/Kitchen":

                # restart the timer when mqtt message received
                self.timer_lifebit_kitchen.stop()
                self.timer_lifebit_kitchen.start()

                motion_sensor =  json_msg["status_word"] & 0x01
                smoke_sensor = (json_msg["status_word"] & 0x02) >> 1

                # 2min. time data polling
                if self.timer_kitchen.elapsed_time > 120:
                    self.timer_kitchen.stop()
                    self.timer_kitchen.start()
                    sql_write_trig = True
                else:
                    sql_write_trig = False

                # write sensor motion with max. resoluton of 60 sec. to SQL DB
                if str(motion_sensor) == '1' and self.timer_motion_kitchen.elapsed_time == 0.0:
                    self.timer_motion_kitchen.start()
                    self.write_to_mysql('room_kitchen',
                                Temperature = json_msg["temperature"],
                                Humidity = json_msg["humidity"],
                                Motion = motion_sensor,
                                SmokeAlarm = smoke_sensor,
                                Timestamp = datetime.now() )


                elif (str(motion_sensor) == '1' \
                    and self.timer_motion_kitchen.elapsed_time > 60.0) \
                    or str(smoke_sensor) == '1' or sql_write_trig is True:
                    self.write_to_mysql('room_kitchen',
                                    Temperature = json_msg["temperature"],
                                    Humidity = json_msg["humidity"],
                                    Motion = motion_sensor,
                                    SmokeAlarm = smoke_sensor,
                                    Timestamp = datetime.now() )
                    if self.timer_motion_kitchen.elapsed_time == 0.0:
                        self.timer_motion_kitchen.start()
                    else:
                        self.timer_motion_kitchen.stop()
                        self.timer_motion_kitchen.start()

            case "HomeAutomation/Kitchen/ZigBee":
                if self.timer_kitchen_zigbee.elapsed_time > 120:
                    self.timer_kitchen_zigbee.stop()
                    self.timer_kitchen_zigbee.start()
                    sql_write_trig = True
                else:
                    sql_write_trig = False

                # detect if fridge door open or timer elapsed
                if json_msg["fridge_door_status"] == '1' and \
                    self.timer_fridge_door_opened.elapsed_time == 0.0:
                    self.timer_fridge_door_opened.start()
                    self.write_to_mysql('room_kitchen_zigbee',
                                Freezer_Temperature = json_msg["freezer_temperature"],
                                Fridge_Temperature = json_msg["fridge_temperature"],
                                Fridge_Humidity = json_msg["fridge_humidity"],
                                Fridge_Door_Status = json_msg["fridge_door_status"],
                                Timestamp = datetime.now() )

                # write fridge door opened status with max. resolution of 30 sec. to SQL DB
                elif (json_msg["fridge_door_status"] == '1' and \
                    self.timer_fridge_door_opened.elapsed_time > 30) or \
                    sql_write_trig is True:
                    self.write_to_mysql('room_kitchen_zigbee',
                                Freezer_Temperature = json_msg["freezer_temperature"],
                                Fridge_Temperature = json_msg["fridge_temperature"],
                                Fridge_Humidity = json_msg["fridge_humidity"],
                                Fridge_Door_Status = json_msg["fridge_door_status"],
                                Timestamp = datetime.now() )
                    if self.timer_fridge_door_opened.elapsed_time == 0.0:
                        self.timer_fridge_door_opened.start()
                    else:
                        self.timer_fridge_door_opened.stop()
                        self.timer_fridge_door_opened.start()

            case "HomeAutomation/Electric":

                # restart the timer when mqtt message received
                self.timer_lifebit_el_switchboard.stop()
                self.timer_lifebit_el_switchboard.start()

                self.el_integral_L1 = self.el_integral_L1 + json_msg["el_currentL1"]
                self.el_integral_L2 = self.el_integral_L2 + json_msg["el_currentL2"]
                self.el_integral_L3 = self.el_integral_L3 + json_msg["el_currentL3"]

                # 5 min (300 sec.) time for data aggregation i.e.:
                # (fixed integral of electrical current over time)
                if self.timer_electric.elapsed_time >= 300:
                    self.timer_electric.stop()
                    self.write_to_mysql('generic_current_integral',
                                L1 = self.el_integral_L1,
                                L2 = self.el_integral_L2,
                                L3 = self.el_integral_L3,
                                Timestamp = datetime.now() )
                    self.el_integral_L1, \
                    self.el_integral_L2, \
                    self.el_integral_L3 = 0, 0, 0
                    self.timer_electric.start()

            case "HomeAutomation/AlarmStatus":
                self.alarm_enabled = json_msg["alarm_enabled"]
                self.camera_enabled = json_msg["camera_enabled"]
                self.alarm_detected = json_msg["alarm_detected"]

            case "HomeAutomation/BedRoom/LightSwitch":
                # restart the timer when mqtt message received
                self.timer_lifebit_light_switch_bed_room.stop()
                self.timer_lifebit_light_switch_bed_room.start()

            case "HomeAutomation/LivingRoom/LightSwitch":
                # restart the timer when mqtt message received
                self.timer_lifebit_light_switch_living_room.stop()
                self.timer_lifebit_light_switch_living_room.start()

            case "HomeAutomation/Kitchen/LightSwitch":
                # restart the timer when mqtt message received
                self.timer_lifebit_light_switch_kitchen.stop()
                self.timer_lifebit_light_switch_kitchen.start()

    def connect_mqtt(self):
        """
        Connect to MQTT broker
        """
        while True:
            try:
                logging.info("Connecting to MQTT broker...")
                self.mqtt_client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2,
                                                      "mqtt_subscriber01",
                                                      protocol=mqtt_client.MQTTv5)
                self.mqtt_client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
                self.mqtt_client.on_connect = self.on_mqtt_connect
                self.mqtt_client.on_message = self.on_mqtt_message
                self.mqtt_client.connect(BROKER_HOST, BROKER_PORT)
                self.mqtt_client.loop_start()
            except Exception as err:
                logging.info("--- Connection to MQTT broker failed: %s ---", err)
            else:
                logging.info("+++ Connection to MQTT broker successfully established +++")
                break

    def get_service_status(self):
        """
        Get status of running services
        """
        while True:
            for service in service_monitor.services:
                self.services_status.update({service: service_monitor.check_service(service) })

            time.sleep(3)

    def share_status_to_flask(self):
        """
        Share connection states and service states 
        via shared_memory_dict to Flask app
        """

        try:
            self.timer_living_room.start()
            self.timer_kitchen.start()
            self.timer_kitchen_zigbee.start()
            self.timer_bath_room.start()
            self.timer_bath_room_zigbee.start()
            self.timer_bed_room.start()
            self.timer_out_pm.start()
            self.timer_electric.start()
            self.timer_outdoor.start()

            self.timer_lifebit_bedroom.start()
            self.timer_lifebit_livingroom.start()
            self.timer_lifebit_kitchen.start()
            self.timer_lifebit_bathroom.start()
            self.timer_lifebit_el_switchboard.start()

            self.timer_lifebit_light_switch_kitchen.start()
            self.timer_lifebit_light_switch_living_room.start()
            self.timer_lifebit_light_switch_bed_room.start()

            while True:

                # detect if connection to RPi in bedroom and living room was lost
                # check if connection lost longer then 20 sec.
                living_room_conn_ok = self.timer_lifebit_livingroom.elapsed_time < 20
                bed_room_conn_ok = self.timer_lifebit_bedroom.elapsed_time < 20

                # detect if RS 485 connection lost to RP2040s
                kitchen_conn_ok = self.timer_lifebit_kitchen.elapsed_time < 15
                electrical_switchboard_conn_ok = self.timer_lifebit_el_switchboard.elapsed_time < 15
                bathroom_conn_ok = self.timer_lifebit_bathroom.elapsed_time < 15
                kitchen_ligth_switch_conn_ok = self.timer_lifebit_light_switch_kitchen.elapsed_time < 15
                living_ligth_switch_conn_ok = self.timer_lifebit_light_switch_living_room.elapsed_time < 15
                bedroom_ligth_switch_conn_ok = self.timer_lifebit_light_switch_bed_room.elapsed_time < 15

                self.sh_mem_dict_config["con_status_livingroom"] = living_room_conn_ok
                self.sh_mem_dict_config["con_status_bedroom"] = bed_room_conn_ok
                self.sh_mem_dict_config["con_status_kitchen"] = kitchen_conn_ok
                self.sh_mem_dict_config["con_status_el_switchboard"] = electrical_switchboard_conn_ok
                self.sh_mem_dict_config["con_status_bathroom"] = bathroom_conn_ok
                self.sh_mem_dict_config["con_status_kitchen_light_switch"] = kitchen_ligth_switch_conn_ok
                self.sh_mem_dict_config["con_status_living_light_switch"] = living_ligth_switch_conn_ok
                self.sh_mem_dict_config["con_status_bedroom_light_switch"] = bedroom_ligth_switch_conn_ok
                self.sh_mem_dict_config["alarm_enabled"] = self.alarm_enabled
                self.sh_mem_dict_config["camera_enabled"] = self.camera_enabled
                self.sh_mem_dict_config["alarm_detected"] = self.alarm_detected

                # check if services_status already populated with status of all services
                if len(self.services_status) == len(service_monitor.services):
                    self.sh_mem_dict_config["mqtt_publisher.service"]    = self.services_status["mqtt_publisher.service"]
                    self.sh_mem_dict_config["mqtt_subscriber.service"]   = self.services_status["mqtt_subscriber.service"]
                    self.sh_mem_dict_config["mosquitto"]                 = self.services_status["mosquitto"]
                    self.sh_mem_dict_config["flask_app.service"]         = self.services_status["flask_app.service"]
                    self.sh_mem_dict_config["grafana-server.service"]    = self.services_status["grafana-server.service"]
                    self.sh_mem_dict_config["mysql.service"]             = self.services_status["mysql.service"]
                    self.sh_mem_dict_config["alarm_handler.service"]     = self.services_status["alarm_handler.service"]


                print (f" status: \n livingroom : {living_room_conn_ok} \
                    \n bedroom: {bed_room_conn_ok} \
                    \n kitchen: {kitchen_conn_ok} \
                    \n bathroom: {bathroom_conn_ok} \
                    \n kitchen light switch {kitchen_ligth_switch_conn_ok} \
                    \n living light switch {living_ligth_switch_conn_ok} \
                    \n bedroom light switch {bedroom_ligth_switch_conn_ok}")

                time.sleep(1)

            # client.disconnect()
            # client.loop_stop()

        except KeyboardInterrupt:
            self.sh_mem_dict_config.shm.close()
            self.sh_mem_dict_config.shm.unlink()

    def write_to_mysql(self, room_name, **room_data):
        """
        Write room data to respective room_name table in MySQL
        """

        try:
            mysql_connection=MySQLdb.connect(host=MYSQL_HOST,
                                            user=MYSQL_USER,
                                            passwd=MYSQL_PASSWORD,
                                            db=MYSQL_DB_NAME)

            match room_name:
                case "generic_current_integral":
                    el_current_ph1 = list(room_data.values())[0]
                    el_current_ph2 = list(room_data.values())[1]
                    el_current_ph3 = list(room_data.values())[2]
                    timestamp = list(room_data.values())[3]

                    sql = "INSERT INTO generic_current_integral \
                        (L1, L2, L3, Timestamp) VALUES (%s, %s, %s, %s)"
                    val = (el_current_ph1, el_current_ph2, el_current_ph3, timestamp)

                case "room_living":
                    temperature = list(room_data.values())[0]
                    humidity = list(room_data.values())[1]
                    motion = list(room_data.values())[2]
                    pm1 = list(room_data.values())[3]
                    pm2_5 = list(room_data.values())[4]
                    pm10 = list(room_data.values())[5]
                    timestamp = list(room_data.values())[6]

                    sql = "INSERT INTO room_living \
                        (Temperature, Humidity, Motion, Timestamp, PM1, PM2_5, PM10) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s )"
                    val = (temperature, humidity, motion,  timestamp, pm1, pm2_5, pm10)

                case "room_bedroom":
                    temperature = list(room_data.values())[0]
                    humidity = list(room_data.values())[1]
                    motion = list(room_data.values())[2]
                    pm1_in = list(room_data.values())[3]
                    pm25_in = list(room_data.values())[4]
                    pm10_in = list(room_data.values())[5]
                    timestamp = list(room_data.values())[6]

                    sql = "INSERT INTO room_bedroom \
                        (Temperature, Humidity, Motion, Timestamp, PM1_in, PM2_5_in, PM10_in) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    val = (temperature, humidity, motion, timestamp, pm1_in, pm25_in, pm10_in)

                case "generic_outside_particulate_matter":
                    pm1_out = list(room_data.values())[0]
                    pm25_out = list(room_data.values())[1]
                    pm10_out = list(room_data.values())[2]
                    timestamp = list(room_data.values())[3]

                    sql = "INSERT INTO generic_outside_particulate_matter \
                        (PM1_out, PM2_5_out, PM10_out, Timestamp) VALUES \
                        (%s, %s, %s, %s )"
                    val = (pm1_out, pm25_out, pm10_out,  timestamp)

                case "generic_outside_conditions":
                    temperature = list(room_data.values())[0]
                    humidity = list(room_data.values())[1]
                    pressure = list(room_data.values())[2]
                    timestamp = list(room_data.values())[3]

                    sql = "INSERT INTO generic_outside_conditions \
                        (Temperature, Humidity, Pressure, Timestamp) VALUES \
                        (%s, %s, %s, %s )"
                    val = (temperature, humidity, pressure, timestamp)

                case "room_bathroom":
                    temperature = list(room_data.values())[0]
                    humidity = list(room_data.values())[1]
                    timestamp = list(room_data.values())[2]

                    sql = "INSERT INTO room_bathroom \
                        (Temperature, Humidity, Motion, Timestamp) VALUES \
                        (%s, %s, %s, %s )"
                    val = (temperature, humidity, 0,  timestamp)

                case "room_bathroom_zigbee":
                    fan_vib_x = list(room_data.values())[0]
                    fan_vib_y = list(room_data.values())[1]
                    fan_vib_z = list(room_data.values())[2]
                    timestamp = list(room_data.values())[3]
                    sql = "INSERT INTO room_bathroom_zigbee \
                            (Fan_Vib_X, Fan_Vib_Y, Fan_Vib_Z, Timestamp) \
                            VALUES (%s, %s, %s, %s )"
                    val = (fan_vib_x, fan_vib_y, fan_vib_z,  timestamp)

                case "room_kitchen":
                    temperature = list(room_data.values())[0]
                    humidity = list(room_data.values())[1]
                    motion_alarm = list(room_data.values())[2]
                    smoke_alarm = list(room_data.values())[3]
                    timestamp = list(room_data.values())[4]

                    sql = "INSERT INTO room_kitchen \
                        (Temperature, Humidity, Motion, SmokeAlarm, Timestamp) \
                        VALUES (%s, %s, %s, %s, %s)"
                    val = (temperature, humidity, motion_alarm, smoke_alarm, timestamp)

                case "room_kitchen_zigbee":
                    freezer_temperature = list(room_data.values())[0]
                    fridge_temperature = list(room_data.values())[1]
                    fridge_humidity = list(room_data.values())[2]
                    fridge_door_status = list(room_data.values())[3]
                    timestamp = list(room_data.values())[4]

                    sql = "INSERT INTO room_kitchen_zigbee \
                        (Freezer_Temperature, \
                        Fridge_Temperature, \
                        Fridge_Humidity, \
                        Fridge_Door_Status, \
                        Timestamp) \
                        VALUES (%s, %s, %s, %s, %s)"
                    val = (freezer_temperature,
                        fridge_temperature,
                        fridge_humidity,
                        fridge_door_status,
                        timestamp)

            #create a cursor object to execute queries
            cursor = mysql_connection.cursor()
            cursor.execute(sql, val)
            mysql_connection.commit()
            mysql_connection.close()
        except MySQLdb.Error as sql_error:
            logging.error(" MySQL error %s", sql_error)

if __name__ == "__main__":

    data_subscriber = MqttDataSubscriber()
    data_subscriber.connect_mqtt()

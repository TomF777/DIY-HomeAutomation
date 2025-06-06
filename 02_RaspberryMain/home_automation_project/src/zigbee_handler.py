#!/usr/bin/env python
"""
Script collects data over UART from zigbee coordinator (ESP32C6),
proccesses it, packs into json and publishes as MQTT messages.
"""
import time
import datetime
import re
import pprint
import logging
import json
from threading import Thread
import RPi.GPIO as GPIO
import serial
import paho.mqtt.client as mqtt


logging.basicConfig(level=logging.INFO)

# config output pin for enable ESP32C6
ZIGBEE_ENABLE_GPIO_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(ZIGBEE_ENABLE_GPIO_PIN, GPIO.OUT)

# mqtt settings
BROKER_HOST = "192.168.1.165"
BROKER_PORT = 1883
BROKER_USERNAME = '***'
BROKER_PASSWORD = '***'

# main structure to store incoming data from bath and kitchen by zigbee
monitor_data = {'fridge_live_bit': 0,
                'fridge_chip_temperature': 0.0,
                'freezer_temperature': 0.0,
                'fridge_door_status': False,
                'fridge_temperature': 0.0,
                'fridge_humidity': 0.0,

                'fan_live_bit': 0,
                'fan_chip_temperature': 0.0,
                'fan_vibration_axis_x': 0.0,
                'fan_vibration_axis_y': 0.0,
                'fan_vibration_axis_z': 0.0}


class ZigBeeCoordinatorHandler():
    """
    Fetch data from ZigBee coordinator over UART
    and publish them regulary as MQTT messages
    """

    def __init__(self):
        # indicators if any single data ready in `monitor_data``
        self.bathroom_fan_data_ready = False
        self.kitchen_fridge_data_ready = False

        # keys from `monitor_data` which already occured in frame from UART
        self.fridge_added_keys = set()
        self.bath_fan_added_keys = set()
        self.mqtt_client = None

        t_fetch_serial_data = Thread(target=self.fetch_serial_data,
                                        args=())
        t_fetch_serial_data.start()

    def fetch_serial_data(self):
        """ 
        Read serial data from zigbee coordinator ESP32C6 
        and update its value to dictionary 'monitor_data'
        """

        failed_data_count = 0
        while True:
            # enable chip ESP32C6
            GPIO.output(ZIGBEE_ENABLE_GPIO_PIN, True)

            try:
                logging.info("===== Setting up UART =====")
                serial_port = serial.Serial('/dev/serial0',
                            baudrate=19200,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            timeout=3.0,
                            rtscts=False,
                            dsrdtr=False
                            )
            except (ValueError, serial.SerialException) as e:
                logging.error(" Serial port configuration error: %s", e)
            else:
                time.sleep(0.1)
                #count = 0
                while True:

                    #count += 1

                    try:
                        get_serial_data = str(serial_port.read(26), 'utf-8')
                    except Exception as e:
                        logging.error(" Wrong serial data: %s", e)
                        failed_data_count += 1
                    else:
                        time.sleep (0.03)
                        logging.info("-" * 50)
                        logging.info("Raw serial data: %s", get_serial_data)
                        logging.info("Data length: %s", len(get_serial_data))

                        if len(get_serial_data) == 0:
                            failed_data_count += 1

                        if get_serial_data is not None:
                            #data = get_serial_data.split(":")
                            # split serial data into list including delimiter ":"
                            data = re.split(r'(\:)', get_serial_data)
                            logging.debug(data)

                            # find all occurences of 'K' (key) and 'V' (value) within serial data
                            keys_pos = [i for i, x in enumerate(data) if x == "K"]
                            values_pos = [i for i, x in enumerate(data) if x == "V"]

                            logging.debug("Keys: %s :Values %s", keys_pos, values_pos)

                            # find min lenght of keys and values list
                            min_index = min([len(keys_pos), len(values_pos)])
                            logging.debug("Min index of keys and values lists: %s", min_index)

                            for idx in range(0,min_index):
                                # 1. there must be enough successors element in data
                                # 2. key value must be positive
                                # 3. V must be successor of K in serial data
                                if len(data) >= values_pos[idx] + 4 and \
                                len(data) >= keys_pos[idx] + 4 and \
                                int(data[keys_pos[idx]+2]) >= 0 and \
                                values_pos[idx] > keys_pos[idx]:

                                    key_val = int(data[keys_pos[idx]+2])
                                    logging.debug(" Key: %s", key_val)

                                    # update monitor_data dictionary with received data from UART
                                    monitor_data[list(monitor_data.keys())[int(data[keys_pos[idx]+2])]] = data[values_pos[idx]+2]

                                    if key_val in range(0, 6):
                                        # data from fridge received
                                        self.kitchen_fridge_data_ready = True
                                        self.fridge_added_keys.add(key_val)
                                    elif key_val in range(6, 11):
                                        # data from fan in bathroom received
                                        self.bathroom_fan_data_ready = True
                                        self.bath_fan_added_keys.add(key_val)

                                    logging.debug("Kitchen data ready:%s fan data ready:%s",
                                                  self.kitchen_fridge_data_ready,
                                                  self.bathroom_fan_data_ready)

                                    logging.debug(idx)
                                    pprint.pp(monitor_data)

                        # for future use
                        # if count % 5 == 0:
                        #     print(" Sending data ... ")
                        #     send_data = 888
                        #     ser.write("888".encode())
                        #     ser.write("22".encode())
                        #     #ser.write(serial.to_bytes([120,220]))
                        #     ser.flush()

                        #clear serial buffer
                        serial_port.flush()
                        serial_port.flushInput()
                        time.sleep(0.2)

                    if failed_data_count >= 10:
                        serial_port.close()
                        failed_data_count = 0
                        self.reset_zigbee(reason='no data from uart')
                        break

    def reset_zigbee(self, reason):
        """
        Reset zigbbe coordinator by
        setting its enable pin to FALSE
        Args:
            reason: str    - cause why the chip is to be reset
        """
        # disable coordinator chip ESP32C6 = RESET
        GPIO.output(ZIGBEE_ENABLE_GPIO_PIN, False)
        logging.info(" *************** RESETTING ZigBee coordinator *******************")
        with open("/home/pi/scripts/diag.log", "a", encoding="utf-8") as f:
            time_now = datetime.datetime.now()
            f.write("\n " + reason + " -> Reset of ESP32C6 Coordinator: " + str(time_now))
        time.sleep(2)
        GPIO.output(ZIGBEE_ENABLE_GPIO_PIN, True)

    def publish_mqtt(self):
        """
        Publish dictionary 'monitor_data' as mqtt message and 
        check if there are active data transmissions over UART
        If no live bit increase then disable for a while the coordinator ESP32C6 (chip reset) 
        """

        time_start = time.time()
        fridge_live_bit_old = monitor_data["fridge_live_bit"]
        fan_live_bit_old = monitor_data["fan_live_bit"]

        while True:
            fridge_live_bit_now = monitor_data["fridge_live_bit"]
            fan_live_bit_now = monitor_data["fan_live_bit"]
            time_now = time.time()

            # check every 120 sec. if live bits increse
            if time_now - time_start >= 120:
                conn_timeout = ''
                logging.debug(" *************** checking live bits *******************")
                logging.debug("time now:%s time start: %s", time_now, time_start)

                if fridge_live_bit_old == fridge_live_bit_now:
                    conn_timeout = 'fridge'
                elif fan_live_bit_old == fan_live_bit_now:
                    conn_timeout = 'bath_fan'

                if len(conn_timeout) > 0 :
                    self.reset_zigbee(reason="connection timeout of " + conn_timeout)

                time_start = time.time()
                fridge_live_bit_old = monitor_data["fridge_live_bit"]
                fan_live_bit_old = monitor_data["fan_live_bit"]


            mqtt_topic = "HomeAutomation/Kitchen/ZigBee"
            kitchen_data = {
                "fridge_livebit":           monitor_data["fridge_live_bit"], 
                "fridge_chip_temperature":  round(int(monitor_data["fridge_chip_temperature"]) / 100.0, 1),
                "freezer_temperature":      round(int(monitor_data["freezer_temperature"]) / 100, 1),
                "fridge_door_status":       monitor_data["fridge_door_status"],
                "fridge_temperature":       round(int(monitor_data["fridge_temperature"]) / 100, 1),
                "fridge_humidity":          round(int(monitor_data["fridge_humidity"]) / 100.0, 0)
                }

            if self.kitchen_fridge_data_ready and [0,1,2,3,4,5] == list(self.fridge_added_keys):
                logging.info(" publish MQTT from kitchen ")
                self.mqtt_client.publish(topic=mqtt_topic,
                               payload=json.dumps(kitchen_data),
                               qos=1,
                               retain=False)
                self.kitchen_fridge_data_ready = False

            mqtt_topic = "HomeAutomation/Bathroom/ZigBee"
            bathroom_data = {"fan_livebit":             monitor_data["fan_live_bit"],
                            "fan_chip_temperature":     round(int(monitor_data["fan_chip_temperature"]) / 100.0, 1),
                            "fan_vibration_axis_x":     int(monitor_data["fan_vibration_axis_x"]),
                            "fan_vibration_axis_y":     int(monitor_data["fan_vibration_axis_y"]),
                            "fan_vibration_axis_z":     int(monitor_data["fan_vibration_axis_z"])}

            if self.bathroom_fan_data_ready and [6,7,8,9,10] == list(self.bath_fan_added_keys):
                logging.info(" publish MQTT from bathroom ")
                self.mqtt_client.publish(topic=mqtt_topic,
                                         payload=json.dumps(bathroom_data),
                                         qos=1,
                                         retain=False)
                self.bathroom_fan_data_ready = False

            time.sleep(1)

    def on_mqtt_connect(self, mqttc, userdata, flags, rc, props):
        """
        Called when MQTT connection successfully established
        """
        if rc==0:
            logging.info("Connected to MQTT Broker")
        else:
            logging.error("Failed to connect to MQTT Broker, error code: %s", rc)
            if rc==1:
                logging.error("1: Connection refused - incorrect protocol version")
            elif rc==2:
                logging.error("2: Connection refused - invalid client identifier")
            elif rc==3:
                logging.error("3: Connection refused - server unavailable")
            elif rc==4:
                logging.error("4: Connection refused - bad username or password")
            elif rc==5:
                logging.error("5: Connection refused - not authorised")

            time.sleep(1)

    def on_mqtt_message(self, client, userdata, message):
        """
        Called when MQTT message received
        """
        print(str(message.topic), ":", str(message.payload.decode('utf-8')))

    def connect_mqtt(self):
        """
        Connect to MQTT broker
        """
        while True:
            try:
                logging.info("Connecting to MQTT broker...")
                self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                                "mqtt_publisher_zigbee",
                                                protocol=mqtt.MQTTv5)
                self.mqtt_client.username_pw_set(BROKER_USERNAME,
                                        BROKER_PASSWORD)
                self.mqtt_client.on_connect = self.on_mqtt_connect
                self.mqtt_client.on_message = self.on_mqtt_message
                self.mqtt_client.connect(BROKER_HOST, BROKER_PORT)
                self.mqtt_client.loop_start()
                time.sleep(1)
            except Exception as err:
                logging.error("--- Connection to MQTT broker failed: %s ---", err)
            else:
                logging.info("+++ Connection to MQTT broker successfully established +++")
                break


if __name__ == "__main__":

    zigbee_handler = ZigBeeCoordinatorHandler()
    zigbee_handler.connect_mqtt()
    zigbee_handler.publish_mqtt()

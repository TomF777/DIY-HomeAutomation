#!/usr/bin/env python3.8.10

""" Script reads from following sensors: 
    - air contamination data (PM1, PM2.5, PM10) from PMS3003P via serial connections.
    - temperature and humidity from DHT22 sensor
    - binary status of motion sensor (HW not implemented, but SW ready to use)
    
    Finally, fetched data are sent in JSON format as MQTT Message 
"""
import logging
import json
import time
from threading import Thread
from pyA20.gpio import gpio
from pyA20.gpio import port
import paho.mqtt.client as mqtt
import serial
from DHT22_Python_library_OPi import dht22
import aux_modules

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# input for DHT22 sensor
DHT22_PIN_NO = port.PA2

gpio.init()

# PC3 as input
gpio.setcfg(port.PC3, gpio.INPUT)

# clear pullups
gpio.pullup(port.PC3, 0)


# mqtt settings
BROKER_HOST = "192.168.1.165"
BROKER_PORT = 1883
BROKER_USERNAME = 'mqttbroker'
BROKER_PASSWORD = 'IoT@2023'


# set outputs for PMS3003P control
gpio.setcfg(port.PA3, gpio.OUTPUT)         #PA3 as output
gpio.setcfg(port.PC0, gpio.OUTPUT)         #PC0 as output
gpio.setcfg(port.PC1, gpio.OUTPUT)         #PC1 as output
gpio.setcfg(port.PC2, gpio.OUTPUT)         #PC1 as output

# set outputs to HIGH
gpio.output(port.PA3, gpio.HIGH)
gpio.output(port.PC0, gpio.HIGH)
gpio.output(port.PC1, gpio.HIGH)
gpio.output(port.PC2, gpio.HIGH)


class MqttDataPublisher():
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.pm1_indoor = None
        self.pm2_5_indoor = None
        self.pm10_indoor = None
        self.pm1_outdoor = None
        self.pm2_5_outdoor = None
        self.pm10_outdoor = None

        self.mqtt_client = None

        # read temperature & humidity in background thread
        t_temperature_humidity = Thread(target=self.read_temperature_humidity,
                                        args=())
        t_temperature_humidity.daemon = False
        t_temperature_humidity.start()

        t_air_dust = Thread(target=self.read_air_dust_sensor,
                                        args=())
        t_air_dust.daemon = False
        t_air_dust.start()


    def read_temperature_humidity(self):
        """ 
        Read temperature and humidity from DHT22 sensor 
        """

        instance_dht22 = dht22.DHT22(pin=DHT22_PIN_NO)

        while True:
            dht22_result = instance_dht22.read()
            time.sleep(3)

            if dht22_result.is_valid():
                self.temperature = dht22_result.temperature
                self.humidity = dht22_result.humidity
                logging.debug("temperature: %s | humidity: %s",
                              self.temperature, self.humidity)
            else:
                logging.error("Can't read out DHT22")

    def read_air_dust_sensor(self):
        """
        Connect to UART1 & UART 2 and read out data
        from air contamination sensors
        """
        while True:
            try:
                logging.info("Configuring UART1")
                serial1 = serial.Serial('/dev/ttyS1',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=3.0,
                rtscts=False,
                dsrdtr=False
                )

                logging.info("Configuring UART2")
                serial2 = serial.Serial('/dev/ttyS2',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=3.0,
                rtscts=False,
                dsrdtr=False
                )

                time.sleep(0.1)

            except (serial.SerialException, ConnectionRefusedError) as e:
                logging.error("Error with UART connection: %s", e)
            else:
                while True:
                    try:
                        # ****************************
                        # *** read data over RS232 ***
                        # ****************************
                        # read 40 bytes from ttyS1 and ttyS2
                        data_uart1=serial1.read(40).hex()       # get data from UART 1
                        data_uart2=serial2.read(40).hex()       # get data from UART 2

                        time.sleep (0.3)
                        logging.info("read UART1: %s", data_uart1)
                        logging.info("read UART2: %s", data_uart2)

                        self.pm1_outdoor, \
                        self.pm2_5_outdoor, \
                        self.pm10_outdoor = self.read_uart(uart_no=1,
                                                          uart_data=data_uart1)

                        self.pm1_indoor, \
                        self.pm2_5_indoor, \
                        self.pm10_indoor = self.read_uart(uart_no=2,
                                                          uart_data=data_uart2)

                        # clear UART buffer
                        serial1.flushInput()
                        serial2.flushInput()
                        time.sleep(3)

                    except Exception as e:
                        logging.error('Error while reading serial uart: %s', e)
                        break

    def read_uart(self, uart_no, uart_data):
        """
        Extract pm1, pm2.5 & PM10 values from serial frame
        of respective UART
        
        Args:
            uart_no: int        - UART number (1, 2 etc)
            uarta_data: str     - string of hexadecimal numbers from serial frame
        Returns:
            PM1, PM2.5 PM10 : float -  air particulate matter value
        """
        # find start character from PMS3003
        start_char = uart_data.find("424d")
        logging.warning("UART%s start sign found at position %s", uart_no, start_char)
        if -1 < start_char < 30:

            start_char_1 = int(uart_data[start_char:start_char + 2], 16)
            start_char_2 = int(uart_data[start_char + 2:start_char + 4], 16)

            frame_len_hi = int(uart_data[start_char + 4:start_char + 6], 16)
            frame_len_lo = int(uart_data[start_char + 6:start_char + 8], 16)
            frame_len = frame_len_hi * 256 + frame_len_lo

            # PM1 [ug/m3] standard particle
            data1_hi = int(uart_data[start_char + 8:start_char + 10], 16)
            data1_lo = int(uart_data[start_char + 10:start_char + 12], 16)
            data1 = data1_hi * 256 + data1_lo

            # PM2.5 [ug/m3] standard particle
            data2_hi = int(uart_data[start_char + 12:start_char + 14], 16)
            data2_lo = int(uart_data[start_char + 14:start_char + 16], 16)
            data2 = data2_hi * 256 + data2_lo

            # PM10 [ug/m3] standard particle
            data3_hi = int(uart_data[start_char + 16:start_char + 18], 16)
            data3_lo = int(uart_data[start_char + 18:start_char + 20], 16)
            data3 = data3_hi * 256 + data3_lo

            # PM1 [ug/m3] atmospheric environment
            data4_hi = int(uart_data[start_char + 20:start_char + 22], 16)
            data4_lo = int(uart_data[start_char + 22:start_char + 24], 16)
            data4 = data4_hi * 256 + data4_lo

            # PM2.5 [ug/m3] atmospheric environment
            data5_hi = int(uart_data[start_char + 24:start_char + 26], 16)
            data5_lo = int(uart_data[start_char + 26:start_char + 28], 16)
            data5 = data5_hi * 256 + data5_lo

            # PM10 [ug/m3] atmospheric environment
            data6_hi = int(uart_data[start_char + 28:start_char + 30], 16)
            data6_lo = int(uart_data[start_char + 30:start_char + 32], 16)
            data6 = data6_hi * 256 + data6_lo

            logging.debug("-" * 30)
            logging.debug("UART%s data: 1=outdoor; 2=indoor", uart_no)
            logging.debug("UART start char1: %s start char2: %s frame length: %s",
                          start_char_1, start_char_2, frame_len)
            logging.debug("Data1 (PM1 standard particle)         : %s", data1)
            logging.debug("Data2 (PM2.5 standard particle)       : %s", data2)
            logging.debug("Data3 (PM10 standard particle)        : %s", data3)
            logging.debug("Data4 (PM1 atmospheric environment)   : %s", data4)
            logging.debug("Data5 (PM2.5 atmospheric environment) : %s", data5)
            logging.debug("Data6 (PM10 atmospheric environment)  : %s", data6)
            logging.debug("-" * 30)
            pm1 = data1
            pm2_5 = data2
            pm10 = data3
            return 	pm1, pm2_5, pm10
        return None, None, None

    def connect_mqtt(self):
        """
        Connect to MQTT broker
        """
        while True:
            try:
                logging.info("Connecting to MQTT broker...")
                self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                                "mqtt_publisher_bedroom",
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

    def publish_mqtt(self):
        """
        Publish sensors data in JSON format as mqtt message
        """

        # timer for cyclically sending data over mqtt
        resend_timer = aux_modules.Timer()
        resend_timer.start()
        life_bit = 0

        while True:
            life_bit += 1

            if life_bit > 254:
                life_bit = 0

            motion_sensor = gpio.input(port.PC3)
            # slow down while loop
            time.sleep(0.2)

            if resend_timer.elapsed_time > 5 or motion_sensor is True:
                resend_timer.stop()
                resend_timer.start()

                if self.humidity is not None and self.temperature is not None \
                and self.pm1_indoor is not None and self.pm1_outdoor is not None:

                    mqtt_topic="HomeAutomation/BedRoom"
                    json_msg = {'temperature':  self.temperature,
                            'humidity':     self.humidity,
                            'motion_sensor': motion_sensor,
                            'PM1_in': self.pm1_indoor,
                            'PM2.5_in':self.pm2_5_indoor,
                            'PM10_in': self.pm10_indoor,
                            'life_bit': life_bit}
                    self.mqtt_client.publish(topic=mqtt_topic,
                                                payload=json.dumps(json_msg),
                                                qos=1, retain=False)


                    mqtt_topic="HomeAutomation/OutdoorPM"
                    json_msg = {'PM1_out':  self.pm1_outdoor,
                            'PM2.5_out': self.pm2_5_outdoor,
                            'PM10_out': self.pm10_outdoor}
                    self.mqtt_client.publish(topic=mqtt_topic,
                                                payload=json.dumps(json_msg),
                                                qos=1, retain=False)
                else:
                    logging.warning("Sensor data not ready")

    def on_mqtt_message(self, client, userdata, message):
        """
        Called when MQTT message received
        """
        print(str(message.topic), ":", str(message.payload.decode('utf-8')))
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

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
        time.sleep(0.5)


if __name__ == "__main__":

    data_publisher = MqttDataPublisher()
    data_publisher.connect_mqtt()
    data_publisher.publish_mqtt()

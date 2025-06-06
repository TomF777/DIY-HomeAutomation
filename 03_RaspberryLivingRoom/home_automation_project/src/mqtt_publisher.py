#!/usr/bin/env python
"""
Script collects data from temperature/humidity sensor, pressure sensor and air contamination sensor.
Sensor data are processed and converted into json and published as MQTT messages.
"""
import json
import time
import logging
import serial
from threading import Thread
import RPi.GPIO as GPIO
import smbus
import paho.mqtt.client as mqtt
import Adafruit_DHT
import aux_modules

logging.basicConfig(level=logging.DEBUG)

MOTION_SENSOR_GPIO_PIN = 27
PMS3003_SET_GPIO_PIN = 23
PMS3003_RESET_GPIO_PIN = 24

GPIO.setmode(GPIO.BCM)
# set motion sensor pin as input
GPIO.setup(MOTION_SENSOR_GPIO_PIN, GPIO.IN)

# set SET/RESET pins of PMS3003 as output
GPIO.setup(PMS3003_SET_GPIO_PIN, GPIO.OUT)
GPIO.setup(PMS3003_RESET_GPIO_PIN, GPIO.OUT)

# mqtt settings
BROKER_HOST = "192.168.1.165"
BROKER_PORT = 1883
BROKER_USERNAME = '***'
BROKER_PASSWORD = '***'


# settings for sensor type: DHT22
DHT_TYPE = Adafruit_DHT.DHT22
# sensor connected to GPIO4
DHT_PIN_NO = 4


# settings for I2C bus (MPL115A2 sensor)
i2c_bus = smbus.SMBus(1)


class MqttDataPublisher():
    """
    Class for sensor data processing and publishing as mqtt messages
    """
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.pressure = None
        self.pm1 = None
        self.pm2_5 = None
        self.pm10 = None
        self.mqtt_client = None

        # read temperature & humidity in background thread
        t_temperature_humidity = Thread(target=self.read_temperature_humidity,
                                        args=(DHT_TYPE, DHT_PIN_NO))
        t_temperature_humidity.daemon = False
        t_temperature_humidity.start()

        # read air dust (PM1, PM2.5, PM10) in background thread
        t_pm = Thread(target=self.read_air_dust_sensor, args=())
        t_pm.daemon = False
        t_pm.start()

    def read_temperature_humidity(self, sensor_type, pin_no):
        """ 
        Read temperature and humidity from DHT22 sensor 
        Args:
            sensor_type: str - sensor type (Adafruit_DHT.DHT22 or Adafruit_DHT.DHT11)
            pin_no: int - GPIO pin of connected sensor
        """

        while True:
            self.humidity, self.temperature = Adafruit_DHT.read_retry(sensor_type, pin_no)
            time.sleep(4)

    def read_pressure(self, i2c_address):
        """
        Read data from pressure  MPL115A2 sensor.
        MPL115A2 address: 0x60(96dec)
        Reading Coefficents for compensation
        Read data back from 0x04(04), 8 bytes
        a0 MSB, a0 LSB, b1 MSB, b1 LSB, b2 MSB, b2 LSB, c12 MSB, c12 LSB
        """

        data = i2c_bus.read_i2c_block_data(i2c_address, 0x04, 8)

        # Convert the data to floating points
        a0 = (data[0] * 256 + data[1]) / 8.0
        b1 = data[2] * 256 + data[3]
        if b1 > 32767:
            b1 -= 65536
        b1 = b1 / 8192.0
        b2 = data[4] * 256 + data[5]
        if b2 > 32767:
            b2 -= 65535
        b2 = b2 / 16384.0
        c12 = ((data[6] * 256 + data[7]) / 4) / 4194304.0

        # write command to the sensor:
        # MPL115A2 address: 0x60(96)
        # Send Pressure measurement command: 0x12(18)
        # Start conversion: 0x00(00)
        i2c_bus.write_byte_data(i2c_address, 0x12, 0x00)

        time.sleep(0.1)

        # read data from i2c:
        # MPL115A2 address, 0x60(96)
        # Read data back from 0x00(00), 4 bytes
        # pres MSB, pres LSB, temp MSB, temp LSB
        data = i2c_bus.read_i2c_block_data(i2c_address, 0x00, 4)

        # Convert the data to 10-bits
        pres = ((data[0] * 256) + (data[1] & 0xC0)) / 64
        temp = ((data[2] * 256) + (data[3] & 0xC0)) / 64

        # Calculate pressure compensation
        press_comp = a0 + (b1 + c12 * temp) * pres + b2 * temp

        # Convert the data to [hPa]
        self.pressure = ((65.0 / 1023.0) * press_comp + 50) * 10.0
        converted_temp = (temp - 498) / (-5.35) + 25

    def read_air_dust_sensor(self):
        """
        Read data from air contamination sensor PMS3003 
        over serial connection
        """

        GPIO.output(PMS3003_SET_GPIO_PIN, 0)
        GPIO.output(PMS3003_RESET_GPIO_PIN, 0)
        time.sleep(1)

        # set GPIO23 - SET(PMS3003), GPIO24 - RESET(PMS3003) to High
        GPIO.output(PMS3003_SET_GPIO_PIN, 1)
        GPIO.output(PMS3003_RESET_GPIO_PIN, 1)

        try:
            logging.info("Setting UART parameters")
            uart_conn = serial.Serial('/dev/ttyAMA0',
                                    baudrate=9600,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=3.0,
                                    rtscts=False,
                                    dsrdtr=False
                                    )

            time.sleep(0.5)

        except serial.SerialException:
            logging.error("UART connection failure")

        else:
            time.sleep(0.5)

            while True:
                hex_data = uart_conn.read(30).hex()
                time.sleep(0.5)

                start_char = hex_data.find("424d")

                if start_char > -1 and start_char < 30:

                    frame_len_hi = int(hex_data[start_char + 4:start_char + 6], 16)
                    frame_len_lo = int(hex_data[start_char + 6:start_char + 8], 16)
                    frame_len = frame_len_hi * 256 + frame_len_lo

                    pm1_std_hi = int(hex_data[start_char + 8:start_char + 10], 16)
                    pm1_std_lo = int(hex_data[start_char + 10:start_char + 12], 16)
                    pm1_std = pm1_std_hi * 256 + pm1_std_lo
                    logging.info("PM1: %s", pm1_std)

                    pm2_5_std_hi = int(hex_data[start_char + 12:start_char + 14], 16)
                    pm2_5_std_lo = int(hex_data[start_char + 14:start_char + 16], 16)
                    pm2_5_std = pm2_5_std_hi *256 + pm2_5_std_lo
                    logging.info("PM2.5: %s", pm2_5_std)

                    pm10_std_hi = int(hex_data[start_char + 16:start_char + 18], 16)
                    pm10_std_lo = int(hex_data[start_char + 18:start_char + 20], 16)
                    pm10_std = pm10_std_hi * 256 + pm10_std_lo
                    logging.info("PM10: %s", pm10_std)

                    self.pm1, self.pm2_5, self.pm10 = pm1_std, pm2_5_std, pm10_std

                    time.sleep(5)

    def process_publish(self):
        """
        Process sensor data and publish as mqtt messages
        """
        life_bit = 0

        # timer for cyclically sending data
        resend_timer = aux_modules.Timer()
        resend_timer.start()
        while True:

            # send life_bit to main RPi
            life_bit += 1
            if life_bit > 254:
                life_bit = 0

            # read status of motion sensor
            motion_sensor = GPIO.input(MOTION_SENSOR_GPIO_PIN)

            self.read_pressure(i2c_address=0x60)

            # send data every 3 seconds or immediately if motion detected
            if resend_timer.elapsed_time > 3 or motion_sensor is True:
                resend_timer.stop()
                resend_timer.start()

                temperature = self.temperature
                humidity = self.humidity
                pressure = self.pressure
                pm1 = self.pm1
                pm2_5 = self.pm2_5
                pm10 = self.pm10

                if (humidity is not None
                    and temperature is not None
                    and pressure is not None
                    and pm1 is not None and pm2_5 is not None and pm10 is not None):
                    logging.debug(" \n \
                                    Temp={0:0.1f} \n \
                                    Humidity={1:0.1f}% \n \
                                    Press={2:0.1f} \n \
                                    MotionSensor:{3:2d} \n \
                                    PM1:{4:2d} PM2.5:{5:2d} PM10:{6:2d} ".
                                    format(temperature,
                                            humidity,
                                            pressure,
                                            motion_sensor,
                                            pm1,
                                            pm2_5,
                                            pm10))

                    time.sleep(0.3)

                    mqtt_topic = "HomeAutomation/LivingRoom"
                    logging.info("Publishing message to topic: %s", mqtt_topic)

                    json_msg = {'temperature': round(temperature, 3),
                                'humidity':    round(humidity, 0),
                                'pressure':    round(pressure, 2),
                                'motion_sensor': motion_sensor,
                                'pm1': pm1,
                                'pm2.5': pm2_5,
                                'pm10': pm10,
                                'life_bit': life_bit}
                    self.mqtt_client.publish(topic=mqtt_topic,
                                                payload=json.dumps(json_msg),
                                                qos=1,
                                                retain=False)

                else:
                    logging.error("Failed to fetch sensors data ")
                    time.sleep(0.5)

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
                                                "mqtt_publisher_living_room",
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

    data_publisher = MqttDataPublisher()
    data_publisher.connect_mqtt()
    data_publisher.process_publish()

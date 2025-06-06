#!/usr/bin/env python3.10

"""
    This program receives data over RS485 from RP2040's, distributes the data over mqtt
    and sends commands to control room light (switch on and off)
    Requires Python 3.10 or higher
"""

import logging
import json
import time
import threading
import serial
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from shared_memory_dict import SharedMemoryDict

logging.basicConfig(level=logging.INFO)

sh_mem_dict_control = SharedMemoryDict(name='control', size=100)


# Pin definition
CTRL_RS485 = 17

# broadcom pin numbering scheme
GPIO.setmode(GPIO.BCM)

# set GPIO as output, for control RS485Pi
GPIO.setup(17, GPIO.OUT)

# mqtt broker settings
BROKER_HOST = "192.168.1.165"
BROKER_PORT = 1883
BROKER_USERNAME = '***'
BROKER_PASSWORD = '***'

def on_connect(client, userdata, flags, rc, props):
    """
    Called when MQTT connection successfully established
    """

    if rc==0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect to MQTT Broker")
        if rc==1:
            print("1: Connection refused - incorrect protocol version")
        if rc==2:
            print("2: Connection refused - invalid client identifier")
        if rc==3:
            print("3: Connection refused - server unavailable")
        if rc==4:
            print("4: Connection refused - bad username or password")
        if rc==5:
            print("5: Connection refused - not authorised")
        time.sleep(1)


def connect_mqtt():
    """
    Connect to MQTT broker
    """
    while True:
        try:
            logging.info("Connecting to MQTT broker")
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                 "Client_Main RPi",
                                 protocol=mqtt.MQTTv5)
            client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)
            client.on_connect=on_connect
            client.connect(BROKER_HOST, BROKER_PORT)
            client.loop_start()

        except Exception as e:
            logging.error("Error with MQTT connection %s", e)
        else:
            return client


def connect_uart():
    """
    Connect to UART serial port
    """
    while True:
        try:
            logging.info("Setting UART parameters")
            serial_port = serial.Serial('/dev/ttyUSB0',
            #serial_port = serial.Serial('/dev/ttyS0',baudrate=19200,
                    baudrate=19200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=3.0,
                    rtscts=False,
                    dsrdtr=False
                    )
        except Exception as e:
            logging.error("Error with UART connection %s", e)
        else:
            return serial_port


def extract_from_uart(slave_name, uart_data, registers_no):
    """
    Extract register's values from uart data
    
    Args:
      slave_name: str  -  UART slave 85AF1..85AF6
      uart_data: str  - data received by UART e.g. 85AF1:R1=0.38 R2=3.14 R3=0.84 R4=31.73
      registers_no: int - number of register to be read out from uart frame
      
    Return:
      registers_values: list with extracted values of R1..Rn registers
      
    """
    registers_values = []
    registers_positions = []
    key_find = uart_data.find(slave_name + ":")

    for register in range(1, registers_no + 1):
        register_to_find = "R" + str(register) + "="
        registers_positions.append(uart_data.find(register_to_find))

    result = True
    for _ in registers_positions:
        if _ == -1:
            result = False
            break

    try:
        if key_find != -1 and result is True:
            if registers_no > 1:
                for reg_no in range(1, registers_no):
                    registers_values.append(
                        float(
                              uart_data[registers_positions[reg_no-1]+3:registers_positions[reg_no]-1]
                              )
                            )

            elif registers_no <= 0:
                return None

            # add last element
            registers_values.append(
                float(
                      uart_data[registers_positions[registers_no-1]+3:registers_positions[registers_no-1]+7]
                      )
                     )

    except Exception as e:
        logging.error("Exception error %s", e)

    logging.debug(" reg values %s", registers_values)
    return registers_values


def fetch_sensors_data(mqtt_client):
    """
    Read data from sensors and publish their values as mqtt messages
    """

    floor_data = {"el_currentL1":0, "el_currentL2":0, "el_currentL3":0, "chip_temp":0}
    outdoor_data = {'temperature':0, 'humidity':0}
    kitchen_data = {'temperature':0, 'humidity':0, 'status_word':0, 'chip_temp':0}
    bathroom_data = {'temperature':0, 'humidity':0, 'chip_temp':0}

    bedroom_light_switch = {'chip_temp':0}
    living_light_switch = {'chip_temp':0}
    kitchen_light_switch = {'chip_temp':0}

    light_switch_codes = {"switch_light_bedroom": "85AF4",
                            "switch_light_living": "85AF5",
                            "switch_light_kitchen": "85AF6"}

	# mapping of expected data length for each UART slave response
	# 85AF1 = Floor RP2040 | 85AF2 = Kitchen Socket | 85AF3 = Bathroom
	# 85AF4 = bedroom light switch | 85AF5 = living room light switch | 85AF6 = kitchen light switch
    data_dict = {"85AF1" : 40,
                 "85AF2" : 52,
                 "85AF3" : 30,
                 "85AF4" : 14,
                 "85AF5" : 14,
                 "85AF6" : 14}

    while True:

        serial_port = connect_uart()

        time.sleep(0.2)
        # test for writing data over RS485
        # while True:
        # 	serial_port.write(str.encode('85AF4 255'))
        # 	time.sleep (2)
        # 	serial_port.write(str.encode('85AF4 0'))
        # 	time.sleep (2)

        while True:
            logging.debug("shared memory dict: %s", sh_mem_dict_control)


            # get command value from sh_mem_dict_control (True/False) and
            # send proper command 255/0 to RP2040 over serial port
            # control command must be e.g.:
            # '85AF5 255' (for switch on the light)
            # or '85AF5 0' (for switch off the light)
            for room in sh_mem_dict_control:
                command = 255 if sh_mem_dict_control[room] is True else 0
                serial_port.write(str.encode(light_switch_codes[room] + " " + str(command)))

            # delay while loop to save CPU consumption
            time.sleep(0.2)

            for key, value in data_dict.items():
                # read different size of usart data defined in `data_dict`

                # ======== read data over RS485 ========
                # set RS485 driver to WRITE # not needed if UART over USB0
                # GPIO.output(17,GPIO.LOW)  # not needed if UART over USB0

                # send slave request
                #serial_port.write(str.encode('85AF4'))
                logging.info(" request to slave: %s", key)
                serial_port.write(str.encode(key))

                # set RS485 driver to READ
                # GPIO.output(17,GPIO.HIGH) # not needed if UART over USB0

                time.sleep(0.2)

                # check if slave answered with any data
                if serial_port.in_waiting > 7:
                    uart_data = None
                    uart_data=serial_port.read(value)
                    uart_data=uart_data.decode(('ascii'), errors='ignore')

                    logging.info("read UART: %s", uart_data)

                    match key:
                        case '85AF1':
                            registers_values = extract_from_uart('85AF1', uart_data, 4)
                            logging.debug(" 85AF1 registers value: %s", registers_values)

                            if len(registers_values) == 4:
                                floor_data["el_currentL1"] = registers_values[0]
                                floor_data["el_currentL2"] = registers_values[1]
                                floor_data['el_currentL3'] = registers_values[2]
                                floor_data['chip_temp'] = registers_values[3]

                                mqtt_topic = "HomeAutomation/Electric"
                                mqtt_client.publish(topic=mqtt_topic,
                                            payload=json.dumps(floor_data),
                                            qos=1,
                                            retain=False)


                        case '85AF2':
                            registers_values = extract_from_uart('85AF2', uart_data, 6)
                            logging.debug(" 85AF2 registers value: %s", registers_values)

                            if len(registers_values) == 6:
                                outdoor_data["humidity"] = registers_values[3]
                                outdoor_data["temperature"] = registers_values[1]
                                kitchen_data["temperature"] = registers_values[0]
                                kitchen_data["humidity"] = registers_values[2]
                                kitchen_data["status_word"] = int(registers_values[5])
                                kitchen_data["chip_temp"] = registers_values[4]

                                mqtt_topic = "HomeAutomation/Outdoor"
                                mqtt_client.publish(topic=mqtt_topic,
                                                payload=json.dumps(outdoor_data),
                                                qos=1,
                                                retain=False)

                                mqtt_topic = "HomeAutomation/Kitchen"
                                mqtt_client.publish(topic=mqtt_topic,
                                                payload=json.dumps(kitchen_data),
                                                qos=1,
                                                retain=False)


                        case '85AF3':
                            registers_values = extract_from_uart('85AF3', uart_data, 3)
                            logging.debug(" 85AF3 registers value: %s", registers_values)

                            if len(registers_values) == 3:
                                bathroom_data["temperature"] = registers_values[0]
                                bathroom_data["humidity"] = registers_values[1]
                                bathroom_data["chip_temp"] = registers_values[2]

                                mqtt_topic = "HomeAutomation/Bathroom"
                                mqtt_client.publish(topic=mqtt_topic,
                                            payload=json.dumps(bathroom_data),
                                            qos=1,
                                            retain=False)


                        case '85AF4':
                            registers_values = extract_from_uart('85AF4', uart_data, 1)
                            logging.debug(" 85AF4 registers value: %s", registers_values)

                            if len(registers_values) == 1:
                                bedroom_light_switch["chip_temp"] = registers_values[0]

                                mqtt_topic = "HomeAutomation/BedRoom/LightSwitch"
                                mqtt_client.publish(topic=mqtt_topic,
                                            payload=json.dumps(bedroom_light_switch),
                                            qos=1, retain=False)


                        case '85AF5':
                            registers_values = extract_from_uart('85AF5', uart_data, 1)
                            logging.debug(" 85AF5 registers value: %s", registers_values)

                            if len(registers_values) == 1:
                                living_light_switch["chip_temp"] = registers_values[0]

                                mqtt_topic = "HomeAutomation/LivingRoom/LightSwitch"
                                mqtt_client.publish(topic=mqtt_topic,
                                            payload=json.dumps(living_light_switch),
                                            qos=1,
                                            retain=False)


                        case '85AF6':
                            registers_values = extract_from_uart('85AF6', uart_data, 1)
                            logging.debug(" 85AF6 registers value: %s", registers_values)

                            if len(registers_values) == 1:
                                kitchen_light_switch["chip_temp"] = registers_values[0]

                                mqtt_topic = "HomeAutomation/Kitchen/LightSwitch"
                                mqtt_client.publish(topic=mqtt_topic,
                                            payload=json.dumps(kitchen_light_switch),
                                            qos=1,
                                            retain=False)


                    serial_port.flush()
                    serial_port.flushInput()

                else:
                    logging.warning("No uart data from %s", key)

        serial_port.close()

    GPIO.cleanup()


if __name__ == "__main__":
    try:

        mqtt_client = connect_mqtt()

        thread_fetch_data = threading.Thread(target=fetch_sensors_data,
                                             args=[mqtt_client],
                                             daemon=True)
        thread_fetch_data.start()
        thread_fetch_data.join()

    except KeyboardInterrupt:
        sh_mem_dict_control.shm.close()
        sh_mem_dict_control.shm.unlink()
        del sh_mem_dict_control

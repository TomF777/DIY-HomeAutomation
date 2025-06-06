# 25.06.2023 - Program to receive data over RS485 from master and to switch on/off light switch with output 3 (Pin3)
#
# Slave request| Slave response
# 85AF6        | R1=xxx Chip Temperature [deg C]
# 85AF6 255    | Switch Light ON (Pin3)
# 85AF6 0      | Switch Light OFF (Pin3)

from machine import UART, ADC
from machine import Pin
import struct
import time
import neopixel

time.sleep(4)

pin_led_onboard=16
pixel_led = neopixel.NeoPixel(Pin(pin_led_onboard), 1)

LightSwitch = Pin(3, Pin.OUT)

# TX_On=True for sending data out from RPi2040, False for receiving data at RPi2040
Uart_TX_On = Pin(2, Pin.OUT)

uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, parity=None, stop=1)
data_tx = 0
data_rx = 0

# ADC settings
adc0 = ADC(0)   # ADC 0 - not used
adc1 = ADC(1)   # ADC 1 - not used
adc2 = ADC(2)   # ADC 2 - not used
adc3 = ADC(3)   # ADC 3 - not used
adc4 = ADC(4)   # on-chip temperature sensor
convert_factor = 3.3/65535

pixel_led[0] = (10,0,0)
pixel_led.write()
time.sleep(1)

while True:
    pixel_led[0] = (0,10,0)
    pixel_led.write()
    ChipTemp = round(27 - ((adc4.read_u16() * convert_factor)-0.706) / 0.001721 , 2) 

    # switch to UART receive mode
    Uart_TX_On.value(0)
    time.sleep(0.05)
    # any serial data received
    if uart.any():
        data_rx = uart.read()
        print("data received: " , str(data_rx))
        data_rx = str(data_rx)
        pixel_led[0] = (0,0,10)
        pixel_led.write()

        slave_req_switchON  = data_rx.find("85AF6 255")
        slave_req_switchOFF = data_rx.find("85AF6 0")
        slave_req = data_rx.find("85AF6")
        if slave_req_switchON !=-1:
            print("slave requested")
            time.sleep(0.02)
            LightSwitch.value(1)
        elif slave_req_switchOFF !=-1:
            print("slave requested")
            time.sleep(0.02)
            LightSwitch.value(0)
        elif slave_req !=-1:
            print("slave requested")
            # switch to UART sending mode
            Uart_TX_On.value(1)

            uart.write("85AF6:" + "R1="+str(ChipTemp) + " ")
            time.sleep(0.02)

        else:
            print("another slave requested")





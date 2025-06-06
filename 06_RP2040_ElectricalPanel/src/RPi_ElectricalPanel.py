"""
This code measures voltage (0-3.3V) of three analog inputs.
Signal on analog inputs is converted by electronics 
conditioner which measures AC current from Current Transformers.

Analog input voltage (0-3.3) is scaled to real AC current value
and sent in serial frame after the slave device was interrogated by
master device.
"""

from machine import UART
from machine import Pin
import time
import machine, neopixel

pin_led_onboard=16
pixel_led = neopixel.NeoPixel(machine.Pin(pin_led_onboard), 1)

# TX_On=True for sending data out from RPi2040, False for receiving data at RPi2040
Uart_TX_On = machine.Pin(2, machine.Pin.OUT)

uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, parity=None, stop=1)
data_tx = 0
data_rx = 0

# ADC settings
adc0 = machine.ADC(0)   # el. current L1
adc1 = machine.ADC(1)   # el. current L2
adc2 = machine.ADC(2)   # el. current L3
adc3 = machine.ADC(4)
convert_factor = 3.3/65535

pixel_led[0] = (0,30,0)
pixel_led.write()
time.sleep(1)

while True:
    
    pixel_led[0] = (10,0,0)
    pixel_led.write()
    ChipTemp = round(27 - ((adc3.read_u16() * convert_factor)-0.706) / 0.001721 , 2) 
    ElCurrentL1 = round((7.4301 * (adc0.read_u16() * convert_factor)) + 0.0819 , 2)
    ElCurrentL2 = round((7.4301 * (adc1.read_u16() * convert_factor)) + 0.0819 , 2)
    ElCurrentL3 = round((7.4301 * (adc2.read_u16() * convert_factor)) + 0.0819 , 2)

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
        
        slave_req=data_rx.find("85AF1")
        if slave_req !=-1:
            print("slave requested")
            # switch to UART sending mode
            Uart_TX_On.value(1)
            
            uart.write("85AF1:" + "R1="+str(ElCurrentL1) + " " + "R2="+str(ElCurrentL2) + " " + "R3="+str(ElCurrentL3) + " " + "R4="+str(ChipTemp) + " ")
            await uasyncio.sleep(0.02)
        else:
            print("another slave requested")

    pixel_led[0] = (0,0,0)
    pixel_led.write()

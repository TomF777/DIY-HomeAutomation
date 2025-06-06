"""
This code measures outdoor temperature and humidity 
from SHT31 sensor by using I2C 
and 
indoor temperature and humidity from DHT22 sensor.

It also detects motion in room (digital input from HC-SR501 sensor) and 
smoke alarm (digital input from SD11B8)

The measured data are sent in serial frame after the slave device
was interrogated by master device.
"""

import machine, neopixel
from machine import UART
from machine import Pin
import time
import dht
from machine import I2C
import sht31
import uasyncio

# XOSC Register start address
XOSC_BASE = 0x40024000

XOSC_STATUS = 0x04

# bit to check indicating XOSC is stable
XOSC_STATUS_STABLE_BIT = 0x80000000

# ROSC Registers start address
ROSC_BASE = 0x40060000

# need to test this
machine.mem32[0x40024000 + 0x0c] = 0x00c4
machine.mem32[0x40024000 + 0x0c] = 1 << 20


# i2c config
sda=machine.Pin(8)
scl=machine.Pin(9)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)

temp_humid_indoor  = dht.DHT22(Pin(3))
motion_sensor      = machine.Pin(5, machine.Pin.IN)
smoke_sensor       = machine.Pin(6, machine.Pin.IN)

temp_in=0
humid_in=0
temp_out=0
humid_out=0

pin_led_onboard=16
pixel_led = neopixel.NeoPixel(machine.Pin(pin_led_onboard), 1)

# TX_On=True for sending data out from RPi2040, 
# TX_On=False for receiving data at RPi2040
Uart_TX_On = machine.Pin(2, machine.Pin.OUT)

uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, txbuf=60 ,parity=None, stop=1)
data_tx = 0
data_rx = 0

# ADC settings
adc3 = machine.ADC(4)
convert_factor = 3.3/65535

pixel_led[0] = (10,0,0)
pixel_led.write()
time.sleep(1)

async def read_temp_humid_sensors():
    global temp_in, humid_in, temp_out, humid_out
    
    while True:
        temp_humid_indoor.measure()
        temp_humid_outdoor = sht31.SHT31(i2c, addr=68)
        
        temp_in = temp_humid_indoor.temperature()
        humid_in = temp_humid_indoor.humidity()
        
        temp_out = round(temp_humid_outdoor.get_temp_humi()[0],1)
        humid_out = int(temp_humid_outdoor.get_temp_humi()[1])
        
        await uasyncio.sleep(1)
    
async def main_task():
    global temp_in, humid_in, temp_out, humid_out
    
    while True:
        pixel_led[0] = (0,10,0)
        pixel_led.write()
        chip_temp = round(27 - ((adc3.read_u16() * convert_factor) - 0.706) / 0.001721 , 2)

        status_word = motion_sensor.value() | smoke_sensor.value()<<1

        # switch to UART receive mode
        Uart_TX_On.value(0)
        await uasyncio.sleep(0.05)
        
        # any serial data received
        if uart.any():
            data_rx = uart.read()
            print("data received: " , str(data_rx))
            data_rx = str(data_rx)
            pixel_led[0] = (0,0,10)
            pixel_led.write()
            
            slave_req=data_rx.find("85AF2")
            if slave_req !=-1:
                print("slave requested")
                # switch to UART sending mode
                Uart_TX_On.value(1)
                
                uart.write("85AF2:" +
                           "R1="+str(temp_in) + " " + \
                           "R2="+str(temp_out) + " " + \
                           "R3="+str(humid_in) + " " + \
                           "R4="+str(humid_out) +  " " + \
                           "R5="+str(chip_temp) + " " + \
                           "R6="+str(status_word) + " " ) 
                
                await uasyncio.sleep(0.02)
                print("85AF2:" +
                           "R1="+str(temp_in) + " " + \
                           "R2="+str(temp_out) + " " + \
                           "R3="+str(humid_in) + " " + \
                           "R4="+str(humid_out) +  " " + \
                           "R5="+str(chip_temp) + " " + \
                           "R6="+str(status_word) + " " )


            else:
                print("another slave requested")
        
        pixel_led[0] = (0,0,0)
        pixel_led.write()


###################################################    
####### asynchronous program execution ############
###################################################
        
event_loop = uasyncio.get_event_loop()

# define coroutines to the event loop
event_loop.create_task(read_temp_humid_sensors())
event_loop.create_task(main_task())

# start the event loop
event_loop.run_forever()




"""
This code measures temperature and humidity from DHT22 sensor.

The measured data are sent in serial frame after the slave device
was interrogated by master device.
"""

import machine, neopixel
from machine import UART
from machine import Pin
import time
import dht
import uasyncio

# DHT22 config
temp_humid_sensor  = dht.DHT22(Pin(3))
temperature, humidity = 0, 0


pin_led_onboard=16
pixel_led = neopixel.NeoPixel(machine.Pin(pin_led_onboard), 1)

# TX_On=True for sending data out from RPi2040, False for receiving data at RPi2040
Uart_TX_On = machine.Pin(2, machine.Pin.OUT)

uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, parity=None, stop=1)
data_tx = 0
data_rx = 0

# ADC settings
adc4 = machine.ADC(4)
convert_factor = 3.3/65535

pixel_led[0] = (10,0,0)
pixel_led.write()
time.sleep(1)

async def read_temp_humid_sensors():
    while True:
        global temperature, humidity
        temp_humid_sensor.measure()
        
        temperature = temp_humid_sensor.temperature()
        humidity = temp_humid_sensor.humidity()
        
        await uasyncio.sleep(4)
    
async def main_task():
    while True:
        pixel_led[0] = (0,10,0)
        pixel_led.write()
        chip_temp = round(27 - ((adc4.read_u16() * convert_factor)-0.706) / 0.001721 , 2)

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

            slave_req=data_rx.find("85AF3")
            if slave_req !=-1:
                print("slave requested")
                # switch to UART sending mode
                Uart_TX_On.value(1)

                uart.write("85AF3:" + "R1="+str(temperature) + " " + "R2="+str(humidity) + " " + "R3="+str(chip_temp) )
                await uasyncio.sleep(0.02)
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





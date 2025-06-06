DHT22 Python library
This simple class can be used for reading temperature and humidity values from DHT22 sensor on Orange PI.

# Usage

Example:
```python
from pyA20.gpio import gpio
from pyA20.gpio import port
 
#import RPi.GPIO as GPIO
import dht22
import time
import datetime
 
# initialize GPIO
#gpio.setwarnings(False)
#gpio.setmode(GPIO.BCM)
PIN2 = port.PA6
gpio.init()
#gpio.cleanup()
 
 
# read data using pin 14
instance = dht22.DHT22(pin=PIN2)
 
while True:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %.2f C" % result.temperature)
        print("Humidity: %.2f %%" % result.humidity)
 
    time.sleep(1)
```    
Please see tutorial:
http://www.piprojects.xyz/temperature-sensor-orange-pi-python-code/

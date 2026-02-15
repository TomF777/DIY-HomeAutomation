// Copyright 2024 Espressif Systems (Shanghai) PTE LTD
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//f
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @brief This example demonstrates Zigbee temperature sensor.
 *
 * The example demonstrates how to use Zigbee library to create a end device temperature sensor.
 * The temperature sensor is a Zigbee end device, which is controlled by a Zigbee coordinator.
 *
 * Proper Zigbee mode must be selected in Tools->Zigbee mode
 * and also the correct partition scheme must be selected in Tools->Partition Scheme.
 *
 * Please check the README.md for instructions and more detailed description.
 *
 * Created by Jan Procházka (https://github.com/P-R-O-C-H-Y/)
 */

#ifndef ZIGBEE_MODE_ED
#error "Zigbee end device mode is not selected in Tools->Zigbee mode"
#endif

#include "Zigbee.h"
#include "ZigbeeGenericSensor.h"


#include <OneWire.h>
#include <millisDelay.h>
#include "Wire.h"
#include "SHT31.h"

// configure DS18B20
OneWire ds18b20(18);          // one-wire sensor on pin GPIO18 (D10) (a 4.7K resistor is necessary)
byte one_wire_addr[8];        // fetched address from one-wire sensor  

// configure SHT31
#define SHT31_ADDRESS   0x44
SHT31 sht31;
uint32_t sht31_start;
uint32_t sht31_stop;

/* DI configuration */
#define GPIO_INPUT_DOOR_SENSOR      D1
#define GPIO_INPUT_D3               D3
#define GPIO_INPUT_D8               D8

/* DO configuration */
#define GPIO_BUZZER                 D7
#define GPIO_OUTPUT_D9              D9
#define GPIO_OUTPUT_D10             D10

/* AI configuration */
#define ANALOG_PIN_A0  A0
#define ANALOG_PIN_A2  A2

/* Zigbee temperature sensor configuration */
#define SENSOR_ENDPOINT_NUMBER      7
uint8_t button = BOOT_PIN;

// Optional Time cluster variables
struct tm timeinfo;
struct tm *localTime;
int32_t timezone;

ZigbeeGenericSensor zbGenericSensor = ZigbeeGenericSensor(SENSOR_ENDPOINT_NUMBER);

/************************ Sensor Handler *****************************/
static void sensor_value_update(void *arg) {
  bool door_sensor;
  int16_t one_wire_temperature;
  uint16_t index = 0;
  float data_value;
  int16_t live_bit;
  float chip_temperature;
  float sht31_temp, sht31_humid;
  int16_t sht31_temperature, sht31_humidity;

  for (;;) {

    index = (index == 6) ? 0 : index;
    live_bit = (live_bit == 100) ? 0 : live_bit;

    if (one_wire_addr[0] == 0x28) {
      one_wire_temperature = int16_t(one_wire_read_temp_sensor() * 100);
    }

    sht31_read_temp_humid(&sht31_temp, &sht31_humid);
    sht31_temperature = sht31_temp * 100;
    sht31_humidity = sht31_humid * 100;

    // Read temperature sensor value
    chip_temperature = temperatureRead();

    door_sensor = digitalRead(GPIO_INPUT_DOOR_SENSOR);
    
    switch (index) {
      case 0:
        data_value = (float)live_bit;
        break;
      case 1:
        data_value = chip_temperature;                        // ESP32C6 temperature
        break;
      case 2:
        data_value = (float)(one_wire_temperature)/100.0;     // freezer temperature
        break;
      case 3:
        data_value = (float)door_sensor;
        break;
      case 4:
        data_value = sht31_temp;                              // icebox temperature
        break;
      case 5:
        data_value = sht31_humid;                             // icebox humidity
        break;
    }

    log_i("Updated index value:%d  data value to %.2f°C\r\n", index, data_value);
    // Update sensor value of End Point
    zbGenericSensor.setSensorValue(index, data_value);

    log_i("Updating data values...\n");
    log_i("Index: %d || Value: %.3f", index, data_value);

    log_i("============================================");
    log_i("Live bit: %d", int(live_bit));
    log_i("ESP32C6 chip temperature: %.3f", chip_temperature);
    log_i("1-wire temperature: %.3f", one_wire_temperature/100.0);
    log_i("Door status: %d", door_sensor);
    log_i("SHT31 temperature %.3f", sht31_temp);
    log_i("SHT31 humidity %.3f", sht31_humid);
    log_i("============================================");

    delay(4000);
    index += 1;
    live_bit += 1;

  }
}


static void door_sensor_eval(bool door_sensor) {
  typedef enum {
    SWITCH_IDLE,
    SWITCH_PRESS_ARMED,
    SWITCH_PRESSED,
    SWITCH_RELEASED,
  } switch_state_t;

  static switch_state_t door_status;
  static millisDelay door_switch_delay;
  static millisDelay delay_sound_1, delay_sound_2;
  static bool door_opened_delayed;
  static uint8_t delay_seq;

  switch (door_status) {
    // door_state: HIGH = door opened; LOW = door closed
    case SWITCH_IDLE:             
                      door_status = (door_sensor == HIGH) ?  SWITCH_PRESSED : SWITCH_IDLE; 
                      break;
    case SWITCH_PRESSED:   
                      door_status = (door_sensor == HIGH) ?  SWITCH_PRESSED : SWITCH_RELEASED;
                      if (!door_switch_delay.isRunning() ) {
                                                            door_switch_delay.start(60000);                // 60 sec. delay after door opened
                                                            } 
                      break;
    case SWITCH_RELEASED:
                      door_status = SWITCH_IDLE;
                      door_switch_delay.stop();
                      noTone(GPIO_BUZZER);
                      digitalWrite(LED_BUILTIN, HIGH);
                      delay_seq = 0;
                      door_opened_delayed = false;
                      break;
    default: break;  
  }


    if (door_switch_delay.justFinished()) {
        door_opened_delayed = true;
        }

    if (door_opened_delayed) {                                
          switch(delay_seq) {
                              case 0:
                                delay_sound_1.start(600);
                                tone(GPIO_BUZZER, 1000);
                                delay_seq = 10;
                                digitalWrite(LED_BUILTIN, LOW);
                                break;
                              case 10:
                                if (delay_sound_1.justFinished()) {
                                                                  noTone(GPIO_BUZZER);
                                                                  delay_sound_1.stop();
                                                                  delay_sound_2.start(600);
                                                                  tone(GPIO_BUZZER, 1500);
                                                                  digitalWrite(LED_BUILTIN, HIGH);
                                                                  delay_seq = 20;
                                                                  } 
                                break;  
                              case 20:
                                if (delay_sound_2.justFinished()) {
                                                                  noTone(GPIO_BUZZER);
                                                                  delay_sound_2.stop();
                                                                  delay_seq = 0;
                                                                  } 
                                break;
                          }
          }

}

/****************** one-wire temperature sensor ********************/
void one_wire_temp_sensor_setup(void) {
  byte i;
  byte type_s;


  if ( !ds18b20.search(one_wire_addr)) {
    log_i("No more addresses.");
    log_i();
    ds18b20.reset_search();
    delay(250);
    return;
  }

  log_i("DS18B20 ROM =");
  for( i = 0; i < 8; i++) {
    log_i(" ");
    log_i("%d", one_wire_addr[i]);
  }

  if (OneWire::crc8(one_wire_addr, 7) != one_wire_addr[7]) {
      log_e("CRC is not valid!");
      return;
  }

  if (one_wire_addr[0] == 0x28) {
    log_i(" Sensor DS18B20 found ");
  } else {
    log_e(" No sensor DS18B20 could be found ");
    return;
  }

  }

float one_wire_read_temp_sensor() {

  byte data[12];
  byte present = 0;
  byte i;
  float celsius;

  // set resolution to 10 bit
  ds18b20.reset();
  ds18b20.select(one_wire_addr);
  ds18b20.write(0x4E, 1);        // write scratchpad
  delay(2); 
  ds18b20.write(0, 1);           // TH/USER BYTE 1 - just dummy value - no impact on configuration
  delay(2); 
  ds18b20.write(0, 1);           // TH/USER BYTE 2 - just dummy value - no impact on configuration
  delay(2); 
  ds18b20.write(0x20, 1);        // 10 bit resolution
  delay(2); 


  ds18b20.reset();
  ds18b20.select(one_wire_addr);
  ds18b20.write(0x44, 1);        // start conversion, with parasite power on at the end

  delay(200);               // for 10bit res. 190 ms is enough

  present = ds18b20.reset();
  ds18b20.select(one_wire_addr);    
  ds18b20.write(0xBE);                 // read scratchpad

  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds18b20.read();
    // Serial.print(data[i], HEX);
    // Serial.print(" ");
  }

  int16_t raw = (data[1] << 8) | data[0];
  byte cfg = (data[4] & 0x60);
  
  // at lower res, the low bits are undefined, so let's zero them
  if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
  else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
  else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
  //// default is 12 bit resolution, 750 ms conversion time

  celsius = (float)raw / 16.0;
//   Serial.print("One wire Temperature = ");
//   Serial.println(celsius);

  return celsius;
}

void sht31_read_temp_humid( float* temperature, float* humidity) {
  sht31_start = micros();
  sht31.read(false);         //  default = true/fast       slow = false
  sht31_stop = micros();

  *temperature = sht31.getTemperature();
  *humidity = sht31.getHumidity();
  // Serial.print("SHT31 temperature: "); Serial.print(sht31.getTemperature(), 1);
  // Serial.print("\t");
  // Serial.print("SHT31 humidity: "); Serial.println(sht31.getHumidity(), 1);

  return;   // no return value
}

void evaluate_door_contact(bool door_switch) {

}

/********************* Arduino functions **************************/
void setup() {

  // External antenna usage
  pinMode(WIFI_ENABLE, OUTPUT);
  digitalWrite(WIFI_ENABLE, LOW);         //turn on this function
  delay(100);
  pinMode(WIFI_ANT_CONFIG, OUTPUT); 
  digitalWrite(WIFI_ANT_CONFIG, LOW);    //use external antenna, LOW=built-in antenna
  
  one_wire_temp_sensor_setup();

  pinMode(GPIO_BUZZER, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT); 
  pinMode(GPIO_INPUT_DOOR_SENSOR, INPUT_PULLUP);

  digitalWrite(LED_BUILTIN, HIGH);

  //Serial.begin(115200);

  // Init SHT31 sensor
  Wire.begin();
  Wire.setClock(100000);
  sht31.begin();
  uint16_t stat = sht31.readStatus();
  log_i(" =========== read SHT31 ====================");
  log_i("%d", stat);


  // Init BOOT button switch
  pinMode(button, INPUT_PULLUP);

  // Optional: set Zigbee device name and model
  zbGenericSensor.setManufacturerAndModel("Espressif", "ZigbeeGenericSensor");

  // Add indexer to sensor
  zbGenericSensor.addIndexToSensor(0, 100.0, 1.0);
  
  // Set minimum and maximum sensor value (10-50°C is default range for chip temperature measurement)
  zbGenericSensor.setMinMaxValue(500, -500);

  // Optional: Set tolerance for sensor measurement (lowest possible value is 0.01)
  zbGenericSensor.setTolerance(0.01);

  // Optional: Time cluster configuration (default params, as this device will retrieve time from coordinator)
  zbGenericSensor.addTimeCluster();

  // Add endpoint to Zigbee Core
  Zigbee.addEndpoint(&zbGenericSensor);

  Serial.println("Starting Zigbee...");
  // When all EPs are registered, start Zigbee in End Device mode
  if (!Zigbee.begin()) {
    log_e("Zigbee failed to start!");
    log_i("Rebooting...");
    Zigbee.factoryReset();
    ESP.restart();
  } else {
    log_i("Zigbee started successfully!");
  }
  
  log_i("Connecting to network");

  unsigned long startTime = millis();
  while (!Zigbee.connected()) {
    log_i(".");
    delay(200);

    // Timeout after 30 seconds
    if (millis() - startTime > 30000) {
      log_i("\nConnection timeout! Rebooting...");
      // Zigbee.factoryReset();
      ESP.restart();
    }
  }

  // Optional: If time cluster is added, time can be read from the coordinator
  //timeinfo = zbTempSensor.getTime();
  //timezone = zbTempSensor.getTimezone();

  //Serial.println("UTC time:");
  //Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");

  //time_t local = mktime(&timeinfo) + timezone;
  //localTime = localtime(&local);

  //Serial.println("Local time with timezone:");
  //Serial.println(localTime, "%A, %B %d %Y %H:%M:%S");

  // Start sensor reading task
  xTaskCreate(sensor_value_update, "sensor_update", 2048, NULL, 10, NULL);

  // Set reporting interval for sensor measurement in seconds, must be called after Zigbee.begin()
  // min_interval and max_interval in seconds, delta (value change in 0,1 )
  // if min = 1 and max = 0, reporting is sent only when value changes by delta
  // if min = 0 and max = 10, reporting is sent every 10 seconds or value changes by delta
  // if min = 0, max = 10 and delta = 0, reporting is sent every 10 seconds regardless of value change

  zbGenericSensor.setSensorReporting(1, 0, 0.001);
  zbGenericSensor.setIndexReporting(1, 0, 0.001);

}

void loop() {

  door_sensor_eval( digitalRead(GPIO_INPUT_DOOR_SENSOR) );

  // Checking BOOT button for factory reset
  if (digitalRead(button) == LOW) {  // Push button pressed
    // Key debounce handling
    delay(100);
    int startTime = millis();
    while (digitalRead(button) == LOW) {
      delay(50);
      if ((millis() - startTime) > 3000) {
        // If key pressed for more than 3secs, factory reset Zigbee and reboot
        log_i("Resetting Zigbee to factory and rebooting in 1s.");
        delay(1000);
        Zigbee.factoryReset();
      }
    }
    
    //zbGenericSensor.reportTemperature();
  }

  delay(100);
}
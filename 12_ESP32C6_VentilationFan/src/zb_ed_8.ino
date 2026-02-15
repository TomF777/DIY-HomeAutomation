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


#include <millisDelay.h>
#include <SPI.h>
#include <SparkFun_ADXL345.h>
 

// configure ADXL345
ADXL345 Adxl345 = ADXL345();

int16_t accel_x_int, accel_y_int, accel_z_int;

/* Switch configuration */



/* Zigbee temperature sensor configuration */
#define SENSOR_ENDPOINT_NUMBER 8
uint8_t button = BOOT_PIN;

// Optional Time cluster variables
struct tm timeinfo;
struct tm *localTime;
int32_t timezone;

ZigbeeGenericSensor zbGenericSensor = ZigbeeGenericSensor(SENSOR_ENDPOINT_NUMBER);

/************************ Sensor Handler *****************************/
static void sensor_value_update(void *arg) {
  uint16_t index = 6;
  float data_value;
  int16_t live_bit;
  float chip_temperature;


  for (;;) {
    index = (index == 11) ? 6 : index;
    live_bit = (live_bit == 100) ? 0 : live_bit;

    // Read temperature sensor value
    chip_temperature = temperatureRead();
    
    switch (index) {
      case 6:
        data_value = (float)live_bit;
        break;
      case 7:
        data_value = chip_temperature;                          // ESP32C6 temperature
        break;
      case 8:
        data_value = ((float)accel_x_int)/10.0;                      // vibration acceleration axis x                     
        break;
      case 9:
        data_value = ((float)accel_y_int)/10.0;                      // vibration acceleration axis y
        break;
      case 10:
        data_value = ((float)accel_z_int)/10.0;                      // vibration acceleration axis z                            
        break;
    }

    log_i("Updated index value:%d  data value to %.2f\r\n", index, data_value);
    // Update sensor value of End Point
    zbGenericSensor.setSensorValue(index, data_value);

    log_i("Updating data values...");
    log_i("Index: %d || Value: %.3f", index, data_value);

    log_i("============================================");
    log_i("Live bit: %d", live_bit);
    log_i("ESP32C6 chip temperature: %.3f", chip_temperature); 
    log_i("Vibration X: %.3f", (float)accel_x_int);
    log_i("Vibration Y: %.3f", (float)accel_y_int);
    log_i("Vibration Z: %.3f", (float)accel_z_int);
    log_i("============================================");

    delay(3000);
    index += 1;
    live_bit += 1;

  }
}

/************************ Accelerometer Measurement *****************************/
static void accelerometer_measurement(void *arg) {

  // separate task for ADXL 345 accelerometer sensor handling

  bool sensor_status;
  byte error_code;
  int x, y, z;
  int16_t accel_x, accel_y, accel_z;
  int16_t accel_x_calc, accel_y_calc, accel_z_calc;
  byte counter;

  while(true) {

      sensor_status = Adxl345.status;
      error_code = Adxl345.error_code;
      if (sensor_status == 1 & error_code == 0) {

          // read sensor accelerations
          Adxl345.readAccel (&x, &y, &z);

          // calibration
          accel_x = (int16_t(x) + 165);
          accel_y = (int16_t(y) - 192);
          accel_z = (int16_t(z) - 5);

          log_d("axis x: %d || axis y: %d || axis z: %d", accel_x, accel_y, accel_z);

          counter += 1;
          if (counter < 30) {
                            // calculate integral over time: 30 x 20ms = 600ms
                            // aggregate 10 measurements
                            accel_x_calc += abs(accel_x);
                            accel_y_calc += abs(accel_y);
                            accel_z_calc += abs(accel_z);
          } else {
                          accel_x_int = accel_x_calc;
                          accel_y_int = accel_y_calc;
                          accel_z_int = accel_z_calc;

                          counter = 0;
                          accel_x_calc = 0;
                          accel_y_calc = 0;
                          accel_z_calc = 0;
                  }
            }

      delay(20);
      
      //vTaskDelay(10 / portTICK_RATE_MS);              // Let's the task scheduler gives time to the other tasks

      }
}


/********************* Arduino functions **************************/
void setup() {

  // External antenna usage
  pinMode(WIFI_ENABLE, OUTPUT);
  digitalWrite(WIFI_ENABLE, LOW);         //turn on this function
  delay(100);
  pinMode(WIFI_ANT_CONFIG, OUTPUT); 
  digitalWrite(WIFI_ANT_CONFIG, HIGH);    // HIGH=use external antenna, LOW=built-in antenna

  pinMode(LED_BUILTIN, OUTPUT); 
  //pinMode(input_name, INPUT_PULLUP);

  digitalWrite(LED_BUILTIN, HIGH);

  //Serial.begin(115200);

  // init ADXL345 accelerometer sensor
  Adxl345.powerOn ();
  Adxl345.setRangeSetting (2);      // set range for +-2g

  // Init BOOT button switch
  pinMode(button, INPUT_PULLUP);

  // Optional: set Zigbee device name and model
  zbGenericSensor.setManufacturerAndModel("Espressif", "ZigbeeGenericSensor");

  // Add indexer to sensor
  zbGenericSensor.addIndexToSensor(0, 100.0, 1.0);
  
  // Set minimum and maximum sensor value (10-50°C is default range for chip temperature measurement)
  // min/max = -155.36 /+155.36 for range 500/-500 - what kind of scaling is it ??? 
  zbGenericSensor.setMinMaxValue(500, -500);

  // Optional: Set tolerance for sensor measurement (lowest possible value is 0.01)
  zbGenericSensor.setTolerance(0.01);

  // Optional: Time cluster configuration (default params, as this device will retrieve time from coordinator)
  zbGenericSensor.addTimeCluster();

  // Add endpoint to Zigbee Core
  Zigbee.addEndpoint(&zbGenericSensor);


  log_i("Starting Zigbee...");
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

  // Start task for accelerometer measurement
  xTaskCreate(accelerometer_measurement, "accelerometer_measurement", 4096, NULL, 4, NULL);

  // Set reporting interval for sensor measurement in seconds, must be called after Zigbee.begin()
  // min_interval and max_interval in seconds, delta (value change in 0,1 )
  // if min = 1 and max = 0, reporting is sent only when value changes by delta
  // if min = 0 and max = 10, reporting is sent every 10 seconds or value changes by delta
  // if min = 0, max = 10 and delta = 0, reporting is sent every 10 seconds regardless of value change

  zbGenericSensor.setSensorReporting(1, 0, 0.001);
  zbGenericSensor.setIndexReporting(1, 0, 0.001);

}

void loop() {
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
    
  }

  delay(100);
}
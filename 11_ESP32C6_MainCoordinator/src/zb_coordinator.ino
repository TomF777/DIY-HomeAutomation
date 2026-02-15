// Copyright 2024 Espressif Systems (Shanghai) PTE LTD
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @brief This example demonstrates simple Zigbee thermostat.
 *
 * The example demonstrates how to use Zigbee library to get data from temperature
 * sensor end device and act as an thermostat.
 * The temperature sensor is a Zigbee end device, which is controlled by a Zigbee coordinator (thermostat).
 *
 * Proper Zigbee mode must be selected in Tools->Zigbee mode
 * and also the correct partition scheme must be selected in Tools->Partition Scheme.
 *
 * Please check the README.md for instructions and more detailed description.
 *
 * Created by Jan Procházka (https://github.com/P-R-O-C-H-Y/) zbThermostat1
 */

#ifndef ZIGBEE_MODE_ZCZR
#error "Zigbee coordinator mode is not selected in Tools->Zigbee mode"
#endif

#include "Zigbee.h"
#include "ZigbeeGenericCoordinator.h"

/* Zigbee thermostat configuration */
#define ENDPOINT_NUMBER_01   7
#define ENDPOINT_NUMBER_02   8
#define ENDPOINT_NUMBER_03   5
#define ENDPOINT_NUMBER_04   6
#define USE_RECEIVE_TEMP_WITH_SOURCE 1
uint8_t button = BOOT_PIN;

ZigbeeGenericCoordinator zbGenericSensor1 = ZigbeeGenericCoordinator(ENDPOINT_NUMBER_01);
ZigbeeGenericCoordinator zbGenericSensor2 = ZigbeeGenericCoordinator(ENDPOINT_NUMBER_02);
ZigbeeGenericCoordinator zbGenericSensor3 = ZigbeeGenericCoordinator(ENDPOINT_NUMBER_03);
ZigbeeGenericCoordinator zbGenericSensor4 = ZigbeeGenericCoordinator(ENDPOINT_NUMBER_04);

// Save sensor data
float sensor_val;
float sensor_max_value;
float sensor_min_value;
float sensor_tolerance;

float sensor2_max_value;
float sensor2_min_value;
float sensor2_tolerance;

float sensor3_max_value;
float sensor3_min_value;
float sensor3_tolerance;

float sensor4_max_value;
float sensor4_min_value;
float sensor4_tolerance;

// Save index data
float index_val;
float index_max_value;
float index_min_value;
float index_tolerance;

float index2_max_value;
float index2_min_value;
float index2_tolerance;

float index3_max_value;
float index3_min_value;
float index3_tolerance;

float index4_max_value;
float index4_min_value;
float index4_tolerance;

uint8_t current_src_endpoint;

struct tm timeinfo = {};  // Time structure for Time cluster

/****************** Sensor handling *******************/
#if USE_RECEIVE_TEMP_WITH_SOURCE == 0
void receiveSensorValue(float sensor_value) {
  log_i("Sensor value: %.2f\n", sensor_value);
  sensor_val = sensor_value;
}
#else
void receiveSensorValueSource(float sensor_value, uint8_t src_endpoint, esp_zb_zcl_addr_t src_address) {
  if (src_address.addr_type == ESP_ZB_ZCL_ADDR_TYPE_SHORT) {
    log_i("Sensor value: %.2f from endpoint %d, address 0x%04x\n", sensor_value, src_endpoint, src_address.u.short_addr);
  } else {
    log_i(
      "Sensor value: %.2f°C from endpoint %d, address %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n", sensor_value, src_endpoint,
      src_address.u.ieee_addr[7], src_address.u.ieee_addr[6], src_address.u.ieee_addr[5], src_address.u.ieee_addr[4], src_address.u.ieee_addr[3],
      src_address.u.ieee_addr[2], src_address.u.ieee_addr[1], src_address.u.ieee_addr[0]
    );
  }
  sensor_val = sensor_value;
  current_src_endpoint = src_endpoint;
}

void receiveIndexWithSource(float index_value, uint8_t src_endpoint, esp_zb_zcl_addr_t src_address) {
  if (src_address.addr_type == ESP_ZB_ZCL_ADDR_TYPE_SHORT) {
    log_i("Index value: %.1f from endpoint %d, address 0x%04x\n", index_value, src_endpoint, src_address.u.short_addr);
  } else {
    log_i(
      "Index value: %.1f% from endpoint %d, address %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n", index_value, src_endpoint,
      src_address.u.ieee_addr[7], src_address.u.ieee_addr[6], src_address.u.ieee_addr[5], src_address.u.ieee_addr[4], src_address.u.ieee_addr[3],
      src_address.u.ieee_addr[2], src_address.u.ieee_addr[1], src_address.u.ieee_addr[0]
    );
  }

  // match sensor value and index only when source endpoints for both of them are the same 
  if (src_endpoint==current_src_endpoint) {
        index_val = index_value;
        log_i("*********************************************************");
        switch (uint16_t(index_val)){
          case 0:
            log_i("** Kitchen Fridge chip live bit: %d", uint16_t(sensor_val));
            break;
          case 1:
            log_i("** Kitchen Fridge Chip temperature: %.2f", sensor_val);
            break;
          case 2:
            log_i("** Kitchen Freezer temperature (DS18B10): %.2f", sensor_val);
            break;
          case 3:
            log_i("** Kitchen Fridge door sensor: %d", uint16_t(sensor_val));
            break;
          case 4:
            log_i("** Kitchen SHT31 temperature: %.2f", sensor_val);
            break;
          case 5:
            log_i("** Kitchen SHT31 humidity: %.1f", sensor_val);
            break;
          case 6:
            log_i("** Bathroom chip live bit: %d", uint16_t(sensor_val));
            break;
          case 7:
            log_i("** Bathroom Chip temperature: %.2f", sensor_val);
            break;
          case 8:
            log_i("** Bathroom acceleration axis X: %.6f", sensor_val);
            break;
          case 9:
            log_i("** Bathroom acceleration axis Y: %.6f", sensor_val);
            break;
          case 10:
            log_i("** Bathroom acceleration axis Z: %.6f", sensor_val);
            break;
          case 11:
            log_i("** Endpoint 5 live bit: %.0f", sensor_val);
            break;
          case 12:
            log_i("** Endpoint 5 chip temp: %.3f", sensor_val);
            break;
          case 13:
            log_i("** Endpoint 5 val01: %.3f", sensor_val);
            break;
          case 14:
            log_i("** Endpoint 5 val02: %.3f", sensor_val);
            break;
          case 15:
            log_i("** Endpoint 6 live bit: %.0f", sensor_val);
            break;
          case 16:
            log_i("** Endpoint 6 chip temp: %.3f", sensor_val);
            break;
          case 17:
            log_i("** Endpoint 6 val01: %.3f", sensor_val);
            break;
          case 18:
            log_i("** Endpoint 6 val02: %.3f", sensor_val);
            break;
        }

        log_i("*********************************************************");
        
        // log_i(" EP1: sensor_max_value: %.2f sensor_min_value: %.2f || index_max_value: %.2f index_min_value: %.2f \n",
        //                 sensor_max_value, sensor_min_value, index_max_value, index_min_value);

        // log_i(" EP2: sensor_max_value: %.2f sensor_min_value: %.2f || index_max_value: %.2f index_min_value: %.2f \n",
        //         sensor2_max_value, sensor2_min_value, index2_max_value, index2_min_value);

        // log_i(" EP3: sensor_max_value: %.2f sensor_min_value: %.2f || index_max_value: %.2f index_min_value: %.2f \n",
        //         sensor3_max_value, sensor3_min_value, index3_max_value, index3_min_value);

        if (uint16_t(index_val) >=0 && uint16_t(index_val) <= 18) {
            // send data as Key:Value pair over UART to RPi
            Serial1.print("K:");Serial1.print(uint16_t(index_val));Serial1.print(":");
            Serial1.print("V:");
            Serial1.print(sensor_val);Serial1.print(":");
            
            // output for Arduino console
            log_i("K:%d:V:%f:", uint16_t(index_val), sensor_val);
        }

  }
  
}
#endif

void receiveSensorConfig_EP1(float min_value, float max_value, float tolerance) {
  log_i("Sensor config: min %.2f°C, max %.2f°C, tolerance %.2f°C\n", min_value, max_value, tolerance);
  sensor_min_value = min_value;
  sensor_max_value = max_value;
  sensor_tolerance = tolerance;
}

void receiveSensorConfig_EP2(float min_value, float max_value, float tolerance) {
  log_i("Sensor config: min %.2f°C, max %.2f°C, tolerance %.2f°C\n", min_value, max_value, tolerance);
  sensor2_min_value = min_value;
  sensor2_max_value = max_value;
  sensor2_tolerance = tolerance;
}

void receiveSensorConfig_EP3(float min_value, float max_value, float tolerance) {
  log_i("Sensor config: min %.2f°C, max %.2f°C, tolerance %.2f°C\n", min_value, max_value, tolerance);
  sensor3_min_value = min_value;
  sensor3_max_value = max_value;
  sensor3_tolerance = tolerance;
}

void receiveSensorConfig_EP4(float min_value, float max_value, float tolerance) {
  log_i("Sensor config: min %.2f°C, max %.2f°C, tolerance %.2f°C\n", min_value, max_value, tolerance);
  sensor4_min_value = min_value;
  sensor4_max_value = max_value;
  sensor4_tolerance = tolerance;
}



void receiveIndexConfig_EP1(float min_value, float max_value, float tolerance) {
  log_i("Index config: min %.2f%, max %.2f%, tolerance %.2f%\n", min_value, max_value, tolerance);
  index_min_value = min_value;
  index_max_value = max_value;
  index_tolerance = tolerance;
}

void receiveIndexConfig_EP2(float min_value, float max_value, float tolerance) {
  log_i("Index config: min %.2f%, max %.2f%, tolerance %.2f%\n", min_value, max_value, tolerance);
  index2_min_value = min_value;
  index2_max_value = max_value;
  index2_tolerance = tolerance;
}

void receiveIndexConfig_EP3(float min_value, float max_value, float tolerance) {
  log_i("Index config: min %.2f%, max %.2f%, tolerance %.2f%\n", min_value, max_value, tolerance);
  index3_min_value = min_value;
  index3_max_value = max_value;
  index3_tolerance = tolerance;
}

void receiveIndexConfig_EP4(float min_value, float max_value, float tolerance) {
  log_i("Index config: min %.2f%, max %.2f%, tolerance %.2f%\n", min_value, max_value, tolerance);
  index4_min_value = min_value;
  index4_max_value = max_value;
  index4_tolerance = tolerance;
}


/********************* Arduino functions **************************/
void setup() {

  // External antenna usage
  pinMode(WIFI_ENABLE, OUTPUT);
  digitalWrite(WIFI_ENABLE, LOW);         //turn on this function
  delay(100);
  pinMode(WIFI_ANT_CONFIG, OUTPUT); 
  digitalWrite(WIFI_ANT_CONFIG, HIGH);    // HIGH=use external antenna, LOW=built-in antenna

  uint16_t loop_count=0;

  //Serial.begin(115200);

  // Init button switch
  pinMode(button, INPUT_PULLUP);

  // configure serial communication
  Serial1.begin(19200, SERIAL_8N1, D7, D6);              // communication over RX(D7) / TX(D6) pins

// Set callback function for receiving temperature from sensor - Use only one option
#if USE_RECEIVE_TEMP_WITH_SOURCE == 0
  zbGenericSensor1.onTempReceive(receiveSensorValue);  // If you bound only one sensor or you don't need to know the source of the sensor
#else
  zbGenericSensor1.onSensorValueReceiveWithSource(receiveSensorValueSource);
  zbGenericSensor2.onSensorValueReceiveWithSource(receiveSensorValueSource);
  zbGenericSensor3.onSensorValueReceiveWithSource(receiveSensorValueSource);
  zbGenericSensor4.onSensorValueReceiveWithSource(receiveSensorValueSource);

  zbGenericSensor1.onIndexValueReceiveWithSource(receiveIndexWithSource);
  zbGenericSensor2.onIndexValueReceiveWithSource(receiveIndexWithSource);
  zbGenericSensor3.onIndexValueReceiveWithSource(receiveIndexWithSource);
  zbGenericSensor4.onIndexValueReceiveWithSource(receiveIndexWithSource);
#endif

  // Set callback function for receiving sensor & index configuration
  zbGenericSensor1.onSensorConfigReceive(receiveSensorConfig_EP1);
  zbGenericSensor2.onSensorConfigReceive(receiveSensorConfig_EP2);
  zbGenericSensor3.onSensorConfigReceive(receiveSensorConfig_EP3);
  zbGenericSensor4.onSensorConfigReceive(receiveSensorConfig_EP4);

  zbGenericSensor1.onIndexConfigReceive(receiveIndexConfig_EP1);
  zbGenericSensor2.onIndexConfigReceive(receiveIndexConfig_EP2);
  zbGenericSensor3.onIndexConfigReceive(receiveIndexConfig_EP3);
  zbGenericSensor4.onIndexConfigReceive(receiveIndexConfig_EP4);

  //Optional: set Zigbee device name and model
  zbGenericSensor1.setManufacturerAndModel("Espressif", "ZigbeeGenericSensor1");
  zbGenericSensor2.setManufacturerAndModel("Espressif", "ZigbeeGenericSensor2");
  zbGenericSensor3.setManufacturerAndModel("Espressif", "ZigbeeGenericSensor3");
  zbGenericSensor4.setManufacturerAndModel("Espressif", "ZigbeeGenericSensor4");


  zbGenericSensor1.allowMultipleBinding(true);
  zbGenericSensor2.allowMultipleBinding(true);
  zbGenericSensor3.allowMultipleBinding(true);
  zbGenericSensor4.allowMultipleBinding(true);


  //Optional Time cluster configuration
  //example time January 13, 2025 13:30:30 CET
  //timeinfo.tm_year = 2025 - 1900;  // = 2025
  //timeinfo.tm_mon = 0;             // January
  //timeinfo.tm_mday = 13;           // 13th
  //timeinfo.tm_hour = 12;           // 12 hours - 1 hour (CET)
  //timeinfo.tm_min = 30;            // 30 minutes
  //timeinfo.tm_sec = 30;            // 30 seconds
  //timeinfo.tm_isdst = -1;

  // Set time and gmt offset (timezone in seconds -> CET = +3600 seconds)
  //zbGenericSensor1.addTimeCluster(timeinfo, 3600);

  //Add endpoint to Zigbee Core
  Zigbee.addEndpoint(&zbGenericSensor1);
  Zigbee.addEndpoint(&zbGenericSensor2);
  Zigbee.addEndpoint(&zbGenericSensor3);
  Zigbee.addEndpoint(&zbGenericSensor4);

  //Open network for 240 seconds after boot
  Zigbee.setRebootOpenNetwork(240);

  // When all EPs are registered, start Zigbee with ZIGBEE_COORDINATOR mode
  if (!Zigbee.begin(ZIGBEE_COORDINATOR)) {
    log_i("Zigbee failed to start!");
    log_i("Rebooting...");
    Zigbee.factoryReset();
    ESP.restart();
  }

  delay(5000);

  log_i("Waiting for sensors to bound to the coordinator");
  while ( !zbGenericSensor1.bound() || !zbGenericSensor2.bound() || !zbGenericSensor3.bound() || !zbGenericSensor4.bound() ) {
    log_i(".");
    log_i(" bound1: %d,   bound2: %d,   bound3: %d,   bound4: %d", zbGenericSensor1.bound(), zbGenericSensor2.bound(), zbGenericSensor3.bound(), zbGenericSensor4.bound() );
    delay(500);
    loop_count++;
    if (loop_count>15) {
      loop_count = 0;
      //Zigbee.factoryReset();
      ESP.restart();
    }
  }

  // Get temperature sensor configuration for all bound sensors by endpoint number and address
  // std::list<zb_device_params_t *> boundSensors = zbGenericSensor1.getBoundDevices();
  
  // for (const auto &device : boundSensors) {
  //   log_i("--------------------------------");
  //   if (device->short_addr == 0x0000 || device->short_addr == 0xFFFF) {  //End devices never have 0x0000 short address or 0xFFFF group address
  //     log_i(
  //       "Device on endpoint %d, IEEE Address: %02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X\r\n", device->endpoint, device->ieee_addr[7], device->ieee_addr[6],
  //       device->ieee_addr[5], device->ieee_addr[4], device->ieee_addr[3], device->ieee_addr[2], device->ieee_addr[1], device->ieee_addr[0]
  //     );
  //     zbGenericSensor1.getTemperatureSettings(device->endpoint, device->ieee_addr);
  //     zbGenericSensor1.getHumiditySettings(device->endpoint, device->ieee_addr);
  //   } else {
  //     log_i("Device on endpoint %d, short address: 0x%x\r\n", device->endpoint, device->short_addr);
  //     zbGenericSensor1.getTemperatureSettings(device->endpoint, device->short_addr);
  //     zbGenericSensor1.getHumiditySettings(device->endpoint, device->short_addr);
  //   }
  // }


  // std::list<zb_device_params_t *> boundSensors2 = zbGenericSensor2.getBoundDevices();
  
  // for (const auto &device : boundSensors2) {
  //   log_i("--------------------------------");
  //   if (device->short_addr == 0x0000 || device->short_addr == 0xFFFF) {  //End devices never have 0x0000 short address or 0xFFFF group address
  //     log_i(
  //       "Device on endpoint %d, IEEE Address: %02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X\r\n", device->endpoint, device->ieee_addr[7], device->ieee_addr[6],
  //       device->ieee_addr[5], device->ieee_addr[4], device->ieee_addr[3], device->ieee_addr[2], device->ieee_addr[1], device->ieee_addr[0]
  //     );
  //     zbGenericSensor2.getTemperatureSettings(device->endpoint, device->ieee_addr);
  //     zbGenericSensor2.getHumiditySettings(device->endpoint, device->ieee_addr);
  //   } else {
  //     log_i("Device on endpoint %d, short address: 0x%x\r\n", device->endpoint, device->short_addr);
  //     zbGenericSensor2.getTemperatureSettings(device->endpoint, device->short_addr);
  //     zbGenericSensor2.getHumiditySettings(device->endpoint, device->ieee_addr);
  //   }
  // }

  // std::list<zb_device_params_t *> boundSensors3 = zbGenericSensor3.getBoundDevices();
  
  // for (const auto &device : boundSensors2) {
  //   log_i("--------------------------------");
  //   if (device->short_addr == 0x0000 || device->short_addr == 0xFFFF) {  //End devices never have 0x0000 short address or 0xFFFF group address
  //     log_i(
  //       "Device on endpoint %d, IEEE Address: %02X:%02X:%02X:%02X:%02X:%02X:%02X:%02X\r\n", device->endpoint, device->ieee_addr[7], device->ieee_addr[6],
  //       device->ieee_addr[5], device->ieee_addr[4], device->ieee_addr[3], device->ieee_addr[2], device->ieee_addr[1], device->ieee_addr[0]
  //     );
  //     zbGenericSensor3.getTemperatureSettings(device->endpoint, device->ieee_addr);
  //     zbGenericSensor3.getHumiditySettings(device->endpoint, device->ieee_addr);
  //   } else {
  //     log_i("Device on endpoint %d, short address: 0x%x\r\n", device->endpoint, device->short_addr);
  //     zbGenericSensor3.getTemperatureSettings(device->endpoint, device->short_addr);
  //     zbGenericSensor3.getHumiditySettings(device->endpoint, device->ieee_addr);
  //   }
  // }

}

void loop() {
  // Handle button switch in loop()
  if (digitalRead(button) == LOW) {  // Push button pressed
    // Key debounce handling
    while (digitalRead(button) == LOW) {
      delay(50);
    }
    // Set reporting interval for temperature sensor
    zbGenericSensor1.setTemperatureReporting(1, 0, 0.001);
    zbGenericSensor2.setTemperatureReporting(1, 0, 0.001);
    zbGenericSensor3.setTemperatureReporting(1, 0, 0.001);
  }

  delay(10);

}
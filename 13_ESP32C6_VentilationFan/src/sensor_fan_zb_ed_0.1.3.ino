// Copyright 2024 Espressif Systems (Shanghai) PTE LTD
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @brief This example demonstrates simple Zigbee temperature sensor.
 *
 * The example demonstrates how to use ESP Zigbee stack to create a end device temperature sensor.
 * The temperature sensor is a Zigbee end device, which is controlled by a Zigbee coordinator.
 *
 * Proper Zigbee mode must be selected in Tools->Zigbee mode
 * and also the correct partition scheme must be selected in Tools->Partition Scheme.
 *
 * Please check the README.md for instructions and more detailed description.
 */

#ifndef ZIGBEE_MODE_ED
#error "Zigbee end device mode is not selected in Tools->Zigbee mode"
#endif

#include "esp_zigbee_core.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "ha/esp_zigbee_ha_standard.h"

#include <OneWire.h>
#include <SPI.h>
#include <Wire.h>
#include <SparkFun_ADXL345.h>

#include <esp_task_wdt.h>
#define WDT_TIMEOUT   4000       // define a 4 seconds WDT (Watch Dog Timer)

//if 1 core doesn't work, try with 2
#define CONFIG_FREERTOS_NUMBER_OF_CORES 1 

esp_task_wdt_config_t twdt_config = {
        .timeout_ms = WDT_TIMEOUT,
        .idle_core_mask = (1 << CONFIG_FREERTOS_NUMBER_OF_CORES) - 1,    // Bitmask of all cores
        .trigger_panic = true,
    };



ADXL345 Adxl345 = ADXL345();

/* Switch configuration */
#define GPIO_INPUT_IO_TOGGLE_SWITCH GPIO_NUM_0
#define PAIR_SIZE(TYPE_STR_PAIR)    (sizeof(TYPE_STR_PAIR) / sizeof(TYPE_STR_PAIR[0]))

typedef enum {
  SWITCH_ON_CONTROL,
  SWITCH_OFF_CONTROL,
  SWITCH_ONOFF_TOGGLE_CONTROL,
  SWITCH_LEVEL_UP_CONTROL,
  SWITCH_LEVEL_DOWN_CONTROL,
  SWITCH_LEVEL_CYCLE_CONTROL,
  SWITCH_COLOR_CONTROL,
} switch_func_t;

typedef struct {
  uint8_t pin;
  switch_func_t func;
} switch_func_pair_t;

typedef enum {
  SWITCH_IDLE,
  SWITCH_PRESS_ARMED,
  SWITCH_PRESS_DETECTED,
  SWITCH_PRESSED,
  SWITCH_RELEASE_DETECTED,
} switch_state_t;

static switch_func_pair_t button_func_pair[] = {{GPIO_INPUT_IO_TOGGLE_SWITCH, SWITCH_ONOFF_TOGGLE_CONTROL}};

int16_t live_bit;
int16_t test_value[4];
int16_t accel_x_int, accel_y_int, accel_z_int; 

/* Default End Device config */
#define ESP_ZB_ZED_CONFIG()                                                                 \
  {                                                                                         \
    .esp_zb_role = ESP_ZB_DEVICE_TYPE_ED, .install_code_policy = INSTALLCODE_POLICY_ENABLE, \
    .nwk_cfg = {                                                                            \
      .zed_cfg =                                                                            \
        {                                                                                   \
          .ed_timeout = ED_AGING_TIMEOUT,                                                   \
          .keep_alive = ED_KEEP_ALIVE,                                                      \
        },                                                                                  \
    },                                                                                      \
  }

#define ESP_ZB_DEFAULT_RADIO_CONFIG() \
  { .radio_mode = ZB_RADIO_MODE_NATIVE, }

#define ESP_ZB_DEFAULT_HOST_CONFIG() \
  { .host_connection_mode = ZB_HOST_CONNECTION_MODE_NONE, }

/* Zigbee configuration */
#define INSTALLCODE_POLICY_ENABLE   false /* enable the install code policy for security */
#define ED_AGING_TIMEOUT            ESP_ZB_ED_AGING_TIMEOUT_64MIN
#define ED_KEEP_ALIVE               5000                                 /* 5000 millisecond */
#define HA_ESP_SENSOR_ENDPOINT      9                                    /* esp temperature sensor device endpoint, used for ventilation fan data measurement */
#define ESP_ZB_PRIMARY_CHANNEL_MASK ESP_ZB_TRANSCEIVER_ALL_CHANNELS_MASK /* Zigbee primary channel mask use in the example */

/* Temperature sensor configuration */
#define ESP_TEMP_SENSOR_UPDATE_INTERVAL (1)  /* Local sensor update interval (second) */
#define ESP_TEMP_SENSOR_MIN_VALUE       (10) /* Local sensor min measured value (degree Celsius) */
#define ESP_TEMP_SENSOR_MAX_VALUE       (50) /* Local sensor max measured value (degree Celsius) */

/* Attribute values in ZCL string format
 * The string should be started with the length of its own.
 */
#define MANUFACTURER_NAME \
  "\x0B"                  \
  "ESPRESSIF"
#define MODEL_IDENTIFIER "\x09" CONFIG_IDF_TARGET

/********************* Zigbee functions **************************/
static int16_t float_to_s16(float temp) {
  return (int16_t)(temp * 100);
}

static void esp_zb_buttons_handler(switch_func_pair_t *button_func_pair) {
  if (button_func_pair->func == SWITCH_ONOFF_TOGGLE_CONTROL) {
    /* Send report attributes command */
    esp_zb_zcl_report_attr_cmd_t report_attr_cmd;
    report_attr_cmd.address_mode = ESP_ZB_APS_ADDR_MODE_DST_ADDR_ENDP_NOT_PRESENT;
    report_attr_cmd.attributeID = ESP_ZB_ZCL_ATTR_TEMP_MEASUREMENT_VALUE_ID;
    report_attr_cmd.cluster_role = ESP_ZB_ZCL_CLUSTER_SERVER_ROLE;
    report_attr_cmd.clusterID = ESP_ZB_ZCL_CLUSTER_ID_TEMP_MEASUREMENT;
    report_attr_cmd.zcl_basic_cmd.src_endpoint = HA_ESP_SENSOR_ENDPOINT;

    esp_zb_lock_acquire(portMAX_DELAY);
    esp_zb_zcl_report_attr_cmd_req(&report_attr_cmd);
    esp_zb_lock_release();
    log_i("Send 'report attributes' command");
  }
}

static void esp_app_sensor_handler(float temperature) {
 
  int16_t door_sensor;
  int16_t one_wire_temperature;
  int16_t data_key, data_value;
  int16_t chip_temperature = float_to_s16(temperatureRead()); 


  data_key += 1;
  live_bit += 1;

  data_key = (data_key == 11) ? 6 : data_key; 


  switch (data_key) {
    case 6:
      data_value = live_bit;
      break;
    case 7:
      data_value = chip_temperature;                // ESP32C6 temperature
      break;
    case 8:                  
      data_value = accel_x_int;                       // vibration acceleration axis x
      break;
    case 9:
      data_value = accel_y_int;                       // vibration acceleration axis y
      break;
    case 10:
      data_value = accel_z_int;                       // vibration acceleration axis z
      break;
  }

    Serial.println("Updating data values...");
    Serial.print("data_key:"); Serial.println(data_key);
    Serial.println("============================================");
    Serial.print("Live bit: ");
    Serial.println(live_bit);

    Serial.print("ESP32C6 chip temperature: ");
    Serial.println(chip_temperature/100.0); 

    Serial.print("Vibration X: ");
    Serial.println(accel_x_int);

    Serial.print("Vibration Y: ");
    Serial.println(accel_y_int);

    Serial.print("Vibration Z: ");
    Serial.println(accel_z_int);

    Serial.println("============================================");



  if (data_key >= 6 && data_key<= 10 && accel_x_int != 0.0 && accel_y_int != 0.0 && accel_z_int != 0.0 ) {
      /* Update measured data values */
      esp_zb_lock_acquire(portMAX_DELAY);
      esp_zb_zcl_set_attribute_val(
        HA_ESP_SENSOR_ENDPOINT, ESP_ZB_ZCL_CLUSTER_ID_TEMP_MEASUREMENT, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE, ESP_ZB_ZCL_ATTR_TEMP_MEASUREMENT_VALUE_ID, &data_key,
        false
      );

      esp_zb_zcl_set_attribute_val(
      HA_ESP_SENSOR_ENDPOINT, ESP_ZB_ZCL_CLUSTER_ID_TEMP_MEASUREMENT, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE, ESP_ZB_ZCL_ATTR_TEMP_MEASUREMENT_MIN_VALUE_ID, &data_value,
      false
      );

      esp_zb_lock_release();
  }

}


static void bdb_start_top_level_commissioning_cb(uint8_t mode_mask) {
  ESP_ERROR_CHECK(esp_zb_bdb_start_top_level_commissioning(mode_mask));
}


// After startup complete, esp_zb_app_signal_handler is called, so application will know when to do some useful things.
void esp_zb_app_signal_handler(esp_zb_app_signal_t *signal_struct) {
  uint32_t *p_sg_p = signal_struct->p_app_signal;
  esp_err_t err_status = signal_struct->esp_err_status;
  esp_zb_app_signal_type_t sig_type = (esp_zb_app_signal_type_t)*p_sg_p;
  switch (sig_type) {
    case ESP_ZB_ZDO_SIGNAL_SKIP_STARTUP:
      log_i("Zigbee stack initialized");
      esp_zb_bdb_start_top_level_commissioning(ESP_ZB_BDB_MODE_INITIALIZATION);
      break;
    case ESP_ZB_BDB_SIGNAL_DEVICE_FIRST_START:
    case ESP_ZB_BDB_SIGNAL_DEVICE_REBOOT:
      if (err_status == ESP_OK) {
        log_i("Start network steering");
        log_i("Device started up in %s factory-reset mode", esp_zb_bdb_is_factory_new() ? "" : "non");

        // Start Temperature sensor reading task
        xTaskCreate(sensor_value_update, "temp_sensor_update", 2048, NULL, 10, NULL);

        if (esp_zb_bdb_is_factory_new()) {
          log_i("Start network steering");
          esp_zb_bdb_start_top_level_commissioning(ESP_ZB_BDB_MODE_NETWORK_STEERING);
        } else {
          log_i("Device rebooted");
        }
      } else {
        /* commissioning failed */
        log_w("Failed to initialize Zigbee stack (status: %s)", esp_err_to_name(err_status));
      }
      break;
    case ESP_ZB_BDB_SIGNAL_STEERING:
      if (err_status == ESP_OK) {
        esp_zb_ieee_addr_t extended_pan_id;
        esp_zb_get_extended_pan_id(extended_pan_id);
        log_i(
          "Joined network successfully (Extended PAN ID: %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x, PAN ID: 0x%04hx, Channel:%d, Short Address: 0x%04hx)",
          extended_pan_id[7], extended_pan_id[6], extended_pan_id[5], extended_pan_id[4], extended_pan_id[3], extended_pan_id[2], extended_pan_id[1],
          extended_pan_id[0], esp_zb_get_pan_id(), esp_zb_get_current_channel(), esp_zb_get_short_address()
        );
      } else {
        log_i("Network steering was not successful (status: %s)", esp_err_to_name(err_status));
        esp_zb_scheduler_alarm((esp_zb_callback_t)bdb_start_top_level_commissioning_cb, ESP_ZB_BDB_MODE_NETWORK_STEERING, 1000);
      }
      break;
    default: log_i("ZDO signal: %s (0x%x), status: %s", esp_zb_zdo_signal_to_string(sig_type), sig_type, esp_err_to_name(err_status)); break;
  }
}

static esp_zb_cluster_list_t *custom_temperature_sensor_clusters_create(esp_zb_temperature_sensor_cfg_t *temperature_sensor) {
  esp_zb_cluster_list_t *cluster_list = esp_zb_zcl_cluster_list_create();
  esp_zb_attribute_list_t *basic_cluster = esp_zb_basic_cluster_create(&(temperature_sensor->basic_cfg));
  ESP_ERROR_CHECK(esp_zb_basic_cluster_add_attr(basic_cluster, ESP_ZB_ZCL_ATTR_BASIC_MANUFACTURER_NAME_ID, (void *)MANUFACTURER_NAME));
  ESP_ERROR_CHECK(esp_zb_basic_cluster_add_attr(basic_cluster, ESP_ZB_ZCL_ATTR_BASIC_MODEL_IDENTIFIER_ID, (void *)MODEL_IDENTIFIER));
  ESP_ERROR_CHECK(esp_zb_cluster_list_add_basic_cluster(cluster_list, basic_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE));
  ESP_ERROR_CHECK(
    esp_zb_cluster_list_add_identify_cluster(cluster_list, esp_zb_identify_cluster_create(&(temperature_sensor->identify_cfg)), ESP_ZB_ZCL_CLUSTER_SERVER_ROLE)
  );
  ESP_ERROR_CHECK(
    esp_zb_cluster_list_add_identify_cluster(cluster_list, esp_zb_zcl_attr_list_create(ESP_ZB_ZCL_CLUSTER_ID_IDENTIFY), ESP_ZB_ZCL_CLUSTER_CLIENT_ROLE)
  );
  ESP_ERROR_CHECK(esp_zb_cluster_list_add_temperature_meas_cluster(
    cluster_list, esp_zb_temperature_meas_cluster_create(&(temperature_sensor->temp_meas_cfg)), ESP_ZB_ZCL_CLUSTER_SERVER_ROLE
  ));
  return cluster_list;
}

static esp_zb_ep_list_t *custom_temperature_sensor_ep_create(uint8_t endpoint_id, esp_zb_temperature_sensor_cfg_t *temperature_sensor) {
  esp_zb_ep_list_t *ep_list = esp_zb_ep_list_create();
  esp_zb_endpoint_config_t endpoint_config = {
    .endpoint = endpoint_id,
    .app_profile_id = ESP_ZB_AF_HA_PROFILE_ID, 
    .app_device_id = ESP_ZB_HA_TEMPERATURE_SENSOR_DEVICE_ID, 
    .app_device_version = 0
  };
  esp_zb_ep_list_add_ep(ep_list, custom_temperature_sensor_clusters_create(temperature_sensor), endpoint_config);
  return ep_list;
}

static void esp_zb_task(void *pvParameters) {

  esp_zb_cfg_t zb_nwk_cfg = ESP_ZB_ZED_CONFIG();
  esp_zb_init(&zb_nwk_cfg);
  /* Create customized temperature sensor endpoint */
  esp_zb_temperature_sensor_cfg_t sensor_cfg = ESP_ZB_DEFAULT_TEMPERATURE_SENSOR_CONFIG();

  /* Set (Min|Max)MeasuredValure */
  sensor_cfg.temp_meas_cfg.min_value = float_to_s16(ESP_TEMP_SENSOR_MIN_VALUE);
  sensor_cfg.temp_meas_cfg.max_value = float_to_s16(ESP_TEMP_SENSOR_MAX_VALUE);
  esp_zb_ep_list_t *esp_zb_sensor_ep = custom_temperature_sensor_ep_create(HA_ESP_SENSOR_ENDPOINT, &sensor_cfg);
  
  /* Register the device */
  esp_zb_device_register(esp_zb_sensor_ep);

  /* Config the reporting info  */
  esp_zb_zcl_reporting_info_t reporting_info = {
    .direction = ESP_ZB_ZCL_CMD_DIRECTION_TO_SRV,
    .ep = HA_ESP_SENSOR_ENDPOINT,
    .cluster_id = ESP_ZB_ZCL_CLUSTER_ID_TEMP_MEASUREMENT,
    .cluster_role = ESP_ZB_ZCL_CLUSTER_SERVER_ROLE,
    .attr_id = ESP_ZB_ZCL_ATTR_TEMP_MEASUREMENT_VALUE_ID,
    .u =
      {
        .send_info =
          {
            .min_interval = 1,
            .max_interval = 0,
            .delta =
              {
                .u16 = 100,
              },
            .def_min_interval = 1,
            .def_max_interval = 0,
          },
      },
    .dst =
      {
        .profile_id = ESP_ZB_AF_HA_PROFILE_ID,
      },
    .manuf_code = ESP_ZB_ZCL_ATTR_NON_MANUFACTURER_SPECIFIC,
  };
  esp_zb_zcl_update_reporting_info(&reporting_info);
  esp_zb_set_primary_network_channel_set(ESP_ZB_PRIMARY_CHANNEL_MASK);

  //Erase NVRAM before creating connection to new Coordinator
  esp_zb_nvram_erase_at_start(true); //Comment out this line to erase NVRAM data if you are connecting to new Coordinator

  ESP_ERROR_CHECK(esp_zb_start(false));
  esp_zb_main_loop_iteration();

  while(true) 
  {
    delay(100);
  }
}


static void accelerometer_task(void *pvParameters) {
  // separate task for ADXL 345 accelerometer sensor handling

  esp_task_wdt_add(NULL);             //add current task to WDT watch

  bool sensor_status;
  byte error_code;
  int x, y, z;
  int16_t accel_x, accel_y, accel_z;
  int16_t accel_x_calc, accel_y_calc, accel_z_calc;
  byte counter;

  while(true) {

            sensor_status = Adxl345.status;
            error_code = Adxl345.error_code;
            if (sensor_status == 1 and error_code == 0) {

                    // read sensor accelerations
                    Adxl345.readAccel (&x, &y, &z);

                    // calibration
                    accel_x = (int16_t(x) + 192);
                    accel_y = (int16_t(y) - 162);
                    accel_z = (int16_t(z) - 7);

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
            esp_task_wdt_reset();                           // Added to repeatedly reset the Watch Dog Timer
            vTaskDelay(10 / portTICK_RATE_MS);              // Let's the task scheduler gives time to the other tasks

            }
}


/************************ sensor handler *****************************/
static void sensor_value_update(void *arg) {
  for (;;) {
    float tsens_value = temperatureRead();        // read esp32c6 chip temperature 
    esp_app_sensor_handler(tsens_value);
    delay(1000);
  }
}


/********************* Arduino functions **************************/
void setup() {

  // configure external antenna
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW);     //turn on this function
  delay(100);
  pinMode(14, OUTPUT); 
  digitalWrite(14, HIGH);   //HIGH=use external antenna; LOW=built-in antenna

  Serial.begin(115200);
  // Init Zigbee
  esp_zb_platform_config_t config = {
    .radio_config = ESP_ZB_DEFAULT_RADIO_CONFIG(),
    .host_config = ESP_ZB_DEFAULT_HOST_CONFIG(),
  };
  ESP_ERROR_CHECK(esp_zb_platform_config(&config));


  // init ADXL345 accelerometer sensor
  Adxl345.powerOn ();
  Adxl345.setRangeSetting (2);      // set range for +-2g

  // watchdog configuration. 3 sec.
  esp_task_wdt_deinit();              //wdt is enabled by default, so we need to deinit it first
  esp_task_wdt_init(&twdt_config);    //enable panic so ESP32 restarts
  esp_task_wdt_add(NULL);             //add current thread to WDT watch

  // Start Zigbee task
  xTaskCreate(esp_zb_task, "Zigbee_main", 4096, NULL, 5, NULL);
  xTaskCreate(accelerometer_task, "Accelerometer_task", 4096, NULL, 4, NULL);

}


// variables for watchdog handling
int last = millis();
int16_t cycle_count;

void loop() {

  cycle_count++;

  // resetting WDT every 2sec.
  if (millis() - last >= 2000)
    {
      esp_task_wdt_reset();           // Added to repeatedly reset the Watch Dog Timer
      last = millis();        
    }

  delay(500);

  // reset chip every 2 hrs.
  if (cycle_count > 14400)
  {
    cycle_count = 0;
    Serial.println(" ****************************************** ");
    Serial.println(" ************  Resetting ESP32  *********** ");
    reboot();
  } 

}

void reboot() {
  esp_task_wdt_deinit();              // disable wdt
  while (1) {}                        // endles loop
}



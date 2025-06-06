""" Flask app to display real time data
    this script must be run after mqtt_subscriber.py due to the shared memory dict 
    shared memory dict receives data from mqtt_subscriber
"""

import time
from multiprocessing.resource_tracker import unregister
from flask import Flask, render_template, request, jsonify
from shared_memory_dict import SharedMemoryDict
import MySQLdb
from flask_csp.csp import csp_header
from flask_cors import CORS
import global_data


app = Flask(__name__)
CORS(app)


SWITCH_LIGHT_LIVING_COMMAND = "OFF"
SWITCH_LIGHT_KITCHEN_COMMAND = "OFF"
SWITCH_LIGHT_BEDROOM_COMMAND = "OFF"

# commands for light switch , heating and illuminance level in rooms
control_living_room = {"heating": 0, "illuminance":0, "light_switch": 0, "comment": ""}
control_bed_room = {"heating": 0, "illuminance":0, "light_switch": 0, "comment": ""}
control_kitchen = {"heating": 0, "illuminance":0, "light_switch": 0, "comment": ""}
control_bath_room = {"heating": 0, "illuminance":0, "light_switch": 0, "comment": ""}


def connect_mysql(host_name, user_name, user_passwd, db_name):
    try:
        mysql_connect = MySQLdb.connect(host = host_name,
                                        user = user_name,
                                        passwd = user_passwd,
                                        db = db_name)
    except (MySQLdb.Error, MySQLdb.Warning) as err:
        print(f" SQL Error {err}")

    return mysql_connect


def get_single_outdoor_data():
    """ 
    Retrieve last value of outdoor data
    """

    connection =  connect_mysql("localhost", "mysql_user", "Internet1!", "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM generic_outside_conditions ORDER By Timestamp DESC LIMIT 1")
    records = cursor.fetchone()

    temperature = list(records)[0]
    humidity = list(records)[1]
    pressure = list(records)[2]

    cursor.close()
    return temperature, humidity, pressure


def get_single_room_data(db_name: str):
    """ 
    Retrieve last value of room's temperature & humidity
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    query = "SELECT * FROM " + db_name + " ORDER By Timestamp DESC LIMIT 1"

    cursor.execute(query)
    records = cursor.fetchone()

    temperature = list(records)[0]
    humidity = list(records)[1]
    motion = list(records)[2]

    if db_name == "room_kitchen":
        smoke_alarm = list(records)[3]
        cursor.close()
        return temperature, humidity, motion, smoke_alarm

    elif db_name == "room_bedroom":
        pm1_in = list(records)[4]
        pm2_5_in = list(records)[5]
        pm10_in = list(records)[6]
        cursor.close()
        return temperature, humidity, motion, pm1_in, pm2_5_in, pm10_in

    cursor.close()
    return temperature, humidity, motion

def get_single_outdoor_pm_data():
    """ 
    Retrieve single last value of PM outdoor data
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT * \
                    FROM generic_outside_particulate_matter \
                    ORDER By Timestamp DESC LIMIT 1")
    records = cursor.fetchone()

    pm1_out = list(records)[0]
    pm2_5_out = list(records)[1]
    pm10_out = list(records)[2]

    connection.close()
    return pm1_out, pm2_5_out, pm10_out

def get_single_elec_integral_data():
    """ 
    Retrieve single last value of electrical integral data
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM generic_current_integral ORDER By Timestamp DESC LIMIT 1")
    records = cursor.fetchone()

    l1_electrical = list(records)[0]
    l2_electrical = list(records)[1]
    l3_electrical = list(records)[2]

    connection.close()
    return l1_electrical, l2_electrical, l3_electrical


def get_hist_outdoor_temp_humid(number_samples):
    """ 
    Retrieve historical values of outdoor temperature and humidity 
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT Temperature, Humidity, Timestamp \
                    FROM generic_outside_conditions \
                    ORDER By Timestamp DESC LIMIT " + str(number_samples))
    records = cursor.fetchall()

    dates = []
    temperatures = []
    humidities = []

    for row in reversed(records):
        temperatures.append(row[0])
        humidities.append(row[1])
        dates.append(row[2])

    connection.close()
    return temperatures, humidities,  dates

def get_hist_temp_humid(number_samples, db_table_name):
    """ 
    Retrieve historical values of temperature and humidity
    from specified room or area (db_table_name)
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT Temperature, Humidity, Timestamp \
                    FROM " + db_table_name + " \
                    ORDER By Timestamp DESC LIMIT " + str(number_samples))
    records = cursor.fetchall()

    dates = []
    temperatures = []
    humidities = []

    for row in reversed(records):
        temperatures.append(row[0])
        humidities.append(row[1])
        dates.append(row[2])

    connection.close()
    return temperatures, humidities,  dates

def get_hist_outdoor_press(number_samples):
    """ retrieve historical values of outdoor pressure """

    connection =  connect_mysql("localhost", "mysql_user", "Internet1!", "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT Pressure, Timestamp \
                    FROM generic_outside_conditions \
                    ORDER By Timestamp DESC LIMIT " + str(number_samples))
    records = cursor.fetchall()

    dates = []
    pressures = []

    for row in reversed(records):
        pressures.append(row[0])
        dates.append(row[1])

    connection.close()
    return pressures, dates

def get_hist_outdoor_pm(number_samples):
    """ 
    Retrieve historical values of outdoor PM data
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT PM1_out, PM2_5_out, PM10_out, Timestamp \
                    FROM generic_outside_particulate_matter \
                    ORDER By Timestamp DESC LIMIT " + str(number_samples))
    records = cursor.fetchall()

    dates = []
    pm1_out = []
    pm2_5_out = []
    pm10_out = []

    for row in reversed(records):
        pm1_out.append(row[0])
        pm2_5_out.append(row[1])
        pm10_out.append(row[2])
        dates.append(row[3])

    connection.close()
    return pm1_out, pm2_5_out,pm10_out, dates


def get_hist_indoor_pm(number_samples):
    """ 
    Retrieve historical values of indoor PM data 
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()
    cursor.execute("SELECT PM1_in, PM2_5_in, PM10_in, Timestamp \
                    FROM room_bedroom \
                    ORDER By Timestamp DESC LIMIT " + str(number_samples))
    records = cursor.fetchall()

    dates = []
    pm1_in = []
    pm2_5_in = []
    pm10_in = []

    for row in reversed(records):
        pm1_in.append(row[0])
        pm2_5_in.append(row[1])
        pm10_in.append(row[2])
        dates.append(row[3])

    connection.close()
    return pm1_in, pm2_5_in, pm10_in, dates

def get_hist_electrical(number_samples):
    """ 
    Retrieve historical values of electrical data
    """

    connection =  connect_mysql("localhost",
                                "mysql_user",
                                "Internet1!",
                                "db_home_automation")

    #create a cursor object to execute queries
    cursor = connection.cursor()

    cursor.execute("SELECT L1, L2, L3, Timestamp \
                    FROM generic_current_integral \
                    ORDER By Timestamp DESC LIMIT " + str(number_samples))
    records = cursor.fetchall()

    dates = []
    l1_electrical = []
    l2_electrical = []
    l3_electrical = []

    for row in reversed(records):
        l1_electrical.append(row[0])
        l2_electrical.append(row[1])
        l3_electrical.append(row[2])
        dates.append(row[3])

    connection.close()
    return l1_electrical, l2_electrical,l3_electrical, dates

# main route - just test.
# @app.route("/", methods=['POST','GET'])
# def index():
#     if request.method == 'POST':
#         if request.form.get('action1') == 'VALUE1':
#             print(" button 1 pressed")
#         elif request.form.get('action2') == 'VALUE2':
#             print(" button 2 pressed")


#     temperature, humidity, pressure = 23, 45, 67
#     outdoor_data = {
#         'temperature': temperature,
#         'humidity': humidity,
#         'pressure': pressure
#         }
#     return render_template('index.html', **outdoor_data)


@app.route("/main", methods=['GET', 'POST'])
def main_page():
    number_samples = 100

    # get variable form html page
    if request.method == 'POST':
        number_samples = request.form['numbersamples']
        try:
            number_samples = int(float(number_samples))
        except ValueError:
            number_samples = 100

    if number_samples <= 0: number_samples = 100

    outdoor_temps, \
    outdoor_hums, \
    outdoor_dates = get_hist_outdoor_temp_humid(number_samples)

    outdoor_press, \
    outdoor_dates_press = get_hist_outdoor_press(number_samples)

    outdoor_pm1, \
    outdoor_pm2_5, \
    outdoor_pm10, \
    outdoor_dates_pm = get_hist_outdoor_pm(number_samples)

    # its [][] list
    hist_data_temp_humid = []
    hist_data_temp_humid.append(["Timstamp","Temperature", "Humidity" ])

    for idx in range(len(outdoor_temps)):
        date_conv = outdoor_dates[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_temp_humid.append( [date_conv, outdoor_temps[idx], outdoor_hums[idx]] )


    # its [][] list
    hist_data_press = []
    hist_data_press.append(["Timstamp","Pressure" ])

    for idx in range(len(outdoor_press)):
        date_conv = outdoor_dates_press[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_press.append( [date_conv, outdoor_press[idx] ] )

    # its [][] list
    hist_data_pm_out = []
    hist_data_pm_out.append(["Timstamp", "PM1", "PM2.5", "PM10" ])

    for idx in range(len(outdoor_pm1)):
        date_conv = outdoor_dates_pm[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_pm_out.append([date_conv,
                                 outdoor_pm1[idx],
                                 outdoor_pm2_5[idx],
                                 outdoor_pm10[idx]] )


    temperature, humidity, pressure = get_single_outdoor_data()
    pm1_out, pm2_5_out, pm10_out = get_single_outdoor_pm_data()

    outdoor_data = {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'pm1_out': pm1_out,
        'pm2_5_out': pm2_5_out,
        'pm10_out': pm10_out
    }

    return render_template('main.html',
                           **outdoor_data,
                           histDataTempHumid = hist_data_temp_humid,
                           histDataPressure = hist_data_press,
                           histDataPMout = hist_data_pm_out )


@app.route("/electrical", methods=['GET', 'POST'])
def electrical_page():
    number_samples = 500

    # get variable form html page
    if request.method == 'POST':
        number_samples = request.form['numbersamples']
        try:
            number_samples = int(float(number_samples))
        except ValueError:
            number_samples = 500

    if number_samples <= 0: number_samples = 500
    elec_integral_l1, \
    elec_integral_l2, \
    elec_integral_l3, \
    elec_integral_dates = get_hist_electrical(number_samples)


    # its [][] list
    hist_data_elec_integral = []
    hist_data_elec_integral.append(["Timstamp","L1", "L2", "L3" ])

    for idx in range(len(elec_integral_l1)):
        date_conv = elec_integral_dates[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_elec_integral.append([date_conv, elec_integral_l1[idx],
                                        elec_integral_l2[idx],
                                        elec_integral_l3[idx]] )


    l1_elec_integral, \
    l2_elec_integral, \
    l3_elec_integral = get_single_elec_integral_data()

    elec_integral_data = {
        'elec_integral_l1': l1_elec_integral,
        'elec_integral_l2': l2_elec_integral,
        'elec_integral_l3': l3_elec_integral
    }

    return render_template('electrical.html',
                           **elec_integral_data,
                           histDataElecIntegral = hist_data_elec_integral )


@app.route("/system_status", methods=['GET', 'POST'])
def status_page():
    sh_mem_dict_config = SharedMemoryDict(name='config', size=400)

    status = {
        'living_room_conn_ok': sh_mem_dict_config["con_status_livingroom"],
        'bed_room_conn_ok': sh_mem_dict_config["con_status_bedroom"],
        'kitchen_conn_ok': sh_mem_dict_config["con_status_kitchen"],
        'el_switchboard_conn_ok': sh_mem_dict_config["con_status_el_switchboard"],
        'bathroom_conn_ok': sh_mem_dict_config["con_status_bathroom"],
        'kitchen_light_switch_conn_ok': sh_mem_dict_config["con_status_kitchen_light_switch"],
        'living_light_switch_conn_ok': sh_mem_dict_config["con_status_living_light_switch"],
        'bedroom_light_switch_conn_ok': sh_mem_dict_config["con_status_bedroom_light_switch"]
    }

    service_status = {
                    'mqtt_publisher_service'    : sh_mem_dict_config["mqtt_publisher.service"],
                    'mqtt_subscriber_service'   : sh_mem_dict_config["mqtt_subscriber.service"],
                    'mosquitto_service'         : sh_mem_dict_config["mosquitto"],
                    'grafana_service'           : sh_mem_dict_config["grafana-server.service"],
                    'mysql_service'             : sh_mem_dict_config["mysql.service"],
                    'alarm_handler_service'     : sh_mem_dict_config["alarm_handler.service"]             
    }

    return render_template('status.html', **status, **service_status )


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_page():

    number_samples = 1200
    global SWITCH_LIGHT_LIVING_COMMAND, SWITCH_LIGHT_KITCHEN_COMMAND, SWITCH_LIGHT_BEDROOM_COMMAND

    # get variable from html page
    if request.method == 'POST':
        if request.form.get('switch_light_living') == 'OFF':
            sh_mem_dict_control['switch_light_living'] = True
            SWITCH_LIGHT_LIVING_COMMAND = "ON"
            print("living OFF")

        elif request.form.get('switch_light_living') == 'ON':
            sh_mem_dict_control['switch_light_living'] = False
            SWITCH_LIGHT_LIVING_COMMAND = "OFF"
            print("living ON")

        elif request.form.get('switch_light_kitchen') == 'OFF':
            sh_mem_dict_control['switch_light_kitchen'] = True
            SWITCH_LIGHT_KITCHEN_COMMAND = "ON"
            print("kitchen OFF")

        elif request.form.get('switch_light_kitchen') == 'ON':
            sh_mem_dict_control['switch_light_kitchen'] = False
            SWITCH_LIGHT_KITCHEN_COMMAND = "OFF"
            print("kitchen ON")

        elif request.form.get('switch_light_bedroom') == 'OFF':
            sh_mem_dict_control['switch_light_bedroom'] = True
            SWITCH_LIGHT_BEDROOM_COMMAND = "ON"
            print("bedroom OFF")

        elif request.form.get('switch_light_bedroom') == 'ON':
            sh_mem_dict_control['switch_light_bedroom'] = False
            SWITCH_LIGHT_BEDROOM_COMMAND = "OFF"
            print("bedroom ON")

        try:
            number_samples = request.form['numbersamples']
            number_samples = int(float(number_samples))
        except Exception as e:
            number_samples = 1200
            print(" exception ", str(e))

        print("requested form: ", request.form)

    print(f"number of samples {number_samples}")
    print(sh_mem_dict_control)

    temperature_living, \
    humidity_living, \
    motion_living = get_single_room_data("room_living")

    print(temperature_living, "  ", humidity_living, "  ", motion_living)

    temperature_kitchen, \
    humidity_kitchen, \
    motion_kitchen, \
    smoke_alarm_kitchen = get_single_room_data("room_kitchen")

    temperature_bedroom, \
    humidity_bedroom, \
    motion_bedroom, \
    pm1_in_bedroom, \
    pm2_5_in_bedroom, \
    pm10_in_bedroom = get_single_room_data("room_bedroom")

    print(f" temp bedroom: {temperature_bedroom}, \
            humid bedroom:{humidity_bedroom}, \
            {pm1_in_bedroom} {pm2_5_in_bedroom} {pm10_in_bedroom}")

    temperature_bathroom, \
    humidity_bathroom, \
    motion_bathroom = get_single_room_data("room_bathroom")

    room_data = {
        'temperature_living': temperature_living,
        'humidity_living': humidity_living,
        'motion_living': motion_living,

        'temperature_kitchen': temperature_kitchen,
        'humidity_kitchen': humidity_kitchen,
        'motion_kitchen': motion_kitchen,
        'smoke_alarm_kitchen': smoke_alarm_kitchen,

        'temperature_bedroom': temperature_bedroom,
        'humidity_bedroom': humidity_bedroom,
        'pm1_in_bedroom': pm1_in_bedroom,
        'pm2_5_in_bedroom': pm2_5_in_bedroom,
        'pm10_in_bedroom': pm10_in_bedroom,

        'temperature_bathroom': temperature_bathroom,
        'humidity_bathroom' : humidity_bathroom,

        'alarm_enabled': sh_mem_dict_config["alarm_enabled"],
        'camera_enabled': sh_mem_dict_config["camera_enabled"],
        'alarm_detected': sh_mem_dict_config["alarm_detected"],

        'SWITCH_LIGHT_LIVING_COMMAND': SWITCH_LIGHT_LIVING_COMMAND,
        'SWITCH_LIGHT_KITCHEN_COMMAND': SWITCH_LIGHT_KITCHEN_COMMAND,
        'SWITCH_LIGHT_BEDROOM_COMMAND': SWITCH_LIGHT_BEDROOM_COMMAND
        }

    if number_samples <= 0: number_samples = 1200

    living_room_temps, \
    living_room_hums, \
    living_room_dates = get_hist_temp_humid(number_samples, "room_living")

    kitchen_temps, \
    kitchen_hums, \
    kitchen_dates = get_hist_temp_humid(number_samples, "room_kitchen")

    bed_room_temps, \
    bed_rooms_hums, \
    bed_rooms_dates = get_hist_temp_humid(number_samples, "room_bedroom")

    bedroom_pm1, \
    bedroom_pm2_5, \
    bedroom_pm10, \
    bedroom_dates_pm = get_hist_indoor_pm(number_samples)

    bath_room_temps, \
    bath_rooms_hums, \
    bath_rooms_dates = get_hist_temp_humid(number_samples, "room_bathroom")

    # its [][] list
    hist_data_living_room_temp_humid = []
    hist_data_living_room_temp_humid.append(["Timstamp","Temperature", "Humidity" ])

    for idx in range(len(living_room_temps)):
        date_conv = living_room_dates[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_living_room_temp_humid.append( [date_conv,
                                                  living_room_temps[idx],
                                                  living_room_hums[idx]] )

    hist_data_kitchen_temp_humid = []
    hist_data_kitchen_temp_humid.append(["Timstamp","Temperature", "Humidity" ])

    for idx in range(len(kitchen_temps)):
        date_conv = kitchen_dates[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_kitchen_temp_humid.append([date_conv,
                                             kitchen_temps[idx],
                                             kitchen_hums[idx]] )

    hist_data_bedroom_temp_humid = []
    hist_data_bedroom_temp_humid.append(["Timstamp","Temperature", "Humidity" ])

    for idx in range(len(bed_room_temps)):
        date_conv = bed_rooms_dates[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_bedroom_temp_humid.append([date_conv,
                                             bed_room_temps[idx],
                                             bed_rooms_hums[idx]] )

    # its [][] list
    hist_data_pm_bedroom = []
    hist_data_pm_bedroom.append(["Timstamp", "PM1", "PM2.5", "PM10" ])

    for idx in range(len(bedroom_pm1)):
        date_conv = bedroom_dates_pm[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_pm_bedroom.append([date_conv,
                                     bedroom_pm1[idx],
                                     bedroom_pm2_5[idx],
                                     bedroom_pm10[idx]] )


    hist_data_bathroom_temp_humid = []
    hist_data_bathroom_temp_humid.append(["Timstamp","Temperature", "Humidity" ])

    for idx in range(len(bath_room_temps)):
        date_conv = bath_rooms_dates[idx].strftime('%Y-%m-%d %H:%M:%S')
        hist_data_bathroom_temp_humid.append([date_conv,
                                              bath_room_temps[idx],
                                              bath_rooms_hums[idx]] )

    alarm_enable_status = False
    alarm_activated = True

    return render_template('rooms.html', **room_data,
                           histDataTempHumidLivingRoom = hist_data_living_room_temp_humid,
                           histDataTempHumidKitchen = hist_data_kitchen_temp_humid,
                           histDataTempHumidBedRoom = hist_data_bedroom_temp_humid,
                           histDataPMBedroom = hist_data_pm_bedroom,
                           histDataTempHumidBathRoom = hist_data_bathroom_temp_humid,
                           alarm_enable_status = alarm_enable_status,
                           alarm_activated = alarm_activated)

@app.route("/camera")
def camera_monitor():
    return render_template('camera.html')

@app.route("/pushbutton", methods=["POST"])
def button_click():
    if request.is_json:
        payload = request.get_json()
        room = list(payload.keys())[0]

        if room == "button_living_room":
            sh_mem_dict_control['switch_light_living'] = not sh_mem_dict_control['switch_light_living']
        elif room == "button_kitchen_room":
            sh_mem_dict_control['switch_light_kitchen'] = not sh_mem_dict_control['switch_light_kitchen']
        elif room == "button_bed_room":
            sh_mem_dict_control['switch_light_bedroom'] = not sh_mem_dict_control['switch_light_bedroom']

        print(sh_mem_dict_control)
        print(list(payload.values())[0])
        print(payload)
        #sh_mem_dict_control['switch_light_living'] = True
        return payload, 201

    return {" error wrong request"}


@app.route("/control_living_room", methods=["POST"])
@app.route("/control_bed_room", methods=["POST"])
@app.route("/control_kitchen", methods=["POST"])
@app.route("/control_bath_room", methods=["POST"])
def control_command():
    dashboard_name = request.path[1:]
    match dashboard_name:
        case "control_living_room":
            dashboard = control_living_room
        case "control_bed_room":
            dashboard = control_bed_room
        case "control_kitchen":
            dashboard = control_kitchen
        case "control_bath_room":
            dashboard = control_bath_room

    if request.is_json:
        payload = request.get_json()
        print(f"control dashboard {dashboard_name} = {payload}")
        for key, value in payload.items():
            if key in dashboard:
                dashboard[key] = value

        if dashboard_name == "control_living_room":
            sh_mem_dict_control['switch_light_living'] = True if payload["light_switch"] == 1 else False

        elif dashboard_name == "control_kitchen":
            sh_mem_dict_control['switch_light_kitchen'] = True if payload["light_switch"] == 1 else False

        elif dashboard_name == "control_bed_room":
            sh_mem_dict_control['switch_light_bedroom'] = True if payload["light_switch"] == 1 else False

        return payload, 201
    return {" error wrong request"}

@app.route('/control_status_living_room', methods=['GET'])
@app.route('/control_status_bed_room', methods=['GET'])
@app.route('/control_status_kitchen', methods=['GET'])
@app.route('/control_status_bath_room', methods=['GET'])
def get_status():
    dashboard = request.path[1:]
    print(f"dashboard = {dashboard}")

    match dashboard:
        case "control_status_living_room":
            dashboard = control_living_room
        case "control_status_bed_room":
            dashboard = control_bed_room
        case "control_status_kitchen":
            dashboard = control_kitchen
        case "control_status_bath_room":
            dashboard = control_bath_room

    return jsonify(dashboard)


@app.route("/<device_name>/<action>")
def action(device_name, action):

    if device_name == 'btn1' and action =="on":
        if global_data.cmd_light_switch_bedroom == 0:
            global_data.cmd_light_switch_bedroom = 1
        elif global_data.cmd_light_switch_bedroom == 1:
            global_data.cmd_light_switch_bedroom = 255
        elif global_data.cmd_light_switch_bedroom == 255:
            global_data.cmd_light_switch_bedroom = 1

    if device_name == 'btn1' and action =="off":
        global_data.cmd_light_switch_bedroom = 255

    if device_name == 'btn2' and action =="on":
        global_data.cmd_light_switch_living = 1
    if device_name == 'btn2' and action =="off":
        global_data.cmd_light_switch_living = 255

    template_data = {
              'btn1_sts'  : global_data.cmd_light_switch_bedroom,
              'btn2_sts'  : global_data.cmd_light_switch_living
    }

    print (global_data.cmd_light_switch_bedroom, global_data.cmd_light_switch_living)
    return render_template('index.html', **template_data)


if __name__ == "__main__":

    try:
        # create shared memory object to get data from mqtt_subscriber
        sh_mem_dict_config = SharedMemoryDict(name='config', size=600)

        sh_mem_dict_control = SharedMemoryDict(name='control', size=100)
        sh_mem_dict_control["switch_light_living"] = False
        sh_mem_dict_control["switch_light_kitchen"] = False
        sh_mem_dict_control["switch_light_bedroom"] = False


        app.run(host='0.0.0.0', port=5000, debug=False)

    except KeyboardInterrupt:
        sh_mem_dict_config.shm.close()
        sh_mem_dict_config.shm.unlink()
        del sh_mem_dict_config

        sh_mem_dict_control.shm.close()
        sh_mem_dict_control.shm.unlink()
        del sh_mem_dict_control

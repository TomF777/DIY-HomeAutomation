#!/usr/bin/python3

"""
   Check status of different services.
   If service is running (active state) return `True` otherwise `False`
"""

import subprocess

# list of services to check
services = ["mqtt_publisher.service",
            "mqtt_subscriber.service",
            "mosquitto",
            "flask_app.service",
            "grafana-server.service",
            "mysql.service",
            "alarm_handler.service"]

services_status = {}

def check_service(service_name:str):
    """
    Check if service has Active status i.e. is running
    """

    result = subprocess.run( ["systemctl", "is-active", service_name],
                                universal_newlines = False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    result = result.stdout.decode("utf-8")

    if result.startswith("active"):
        return "OK"
    return "NOK"


# for service in services:
#    #print (check_service(service))
#    services_status.update({service: check_service(service) })


# print (services_status)

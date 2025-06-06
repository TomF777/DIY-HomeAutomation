"""
This script streams picamera video over flask app
and records images & video locally on the RPi
as soon as motion is detected.

Motion detection activation/deactivation via GET REST API
from alarm_handler.py

"""

#import os
#import datetime
import time
#import glob
import threading
import signal
import statistics
import logging
import numpy as np
import cv2
import io
from flask import Flask, Response, request, url_for
from flask_cors import CORS
import picamera
import picamera.array
from settings import *


motion_detection_enabled = False


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# picamera config
camera=picamera.PiCamera()
camera.resolution = (streamWidth, streamHeight)
camera.vflip = imageVFlip
camera.hflip = imageHFlip
camera.exposure_mode = 'auto'
camera.awb_mode = 'auto'
camera.framerate = 15


def generate_frames(camera):
    """ Generate jpeg stream """
    
    stream = io.BytesIO()
    try:
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
            stream.seek(0)
            stream.truncate()

    except Exception as e:
        logging.ERROR(" Video JPEG streaming stopped",)
        
        
def generate_video_noise():
    """ Random noisy image stream """
    while True:
        time.sleep(0.2)
        img = np.random.randint(0, 255, size=(300, 300, 3), dtype=np.uint8)
        _, frame = cv2.imencode('.jpg', img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
        

def get_stream_array(camera):
    """ Take a stream image and return the image data array"""
    with picamera.array.PiRGBArray(camera) as stream:

        camera.capture(stream, format='rgb')
        #camera.close()
        return stream.array

def scan_motion(camera):
    """ Compare two image scans and return differences as indication of motion """
    data1 = get_stream_array(camera)
    while True:
        data2 = get_stream_array(camera)
        diff_count = 0
        for y_pixel in range(0, streamHeight):
            for x_pixel in range(0, streamWidth):
                # get pixel differences. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[y_pixel][x_pixel][1]) - int(data2[y_pixel][x_pixel][1]))
                if  diff > threshold:
                    diff_count += 1
                    #if diff_count > sensitivity:
                        # x,y is a very rough motion position
                        #return x, y

        logging.debug("stream differences: %i", diff_count)
        data1 = data2
        return diff_count


def motion_detection():
    """ detect motion in camera stream """
    init_count = 0
    scan_list = []
    init_image_done = False

    while True:
        if motion_detection_enabled:
            value = scan_motion(camera)
            logging.info("stream differences: %i", value)
            time.sleep(0.01)
            # start analytics from 3rd camera scan. Two first are scrap after activating camera.
            if init_count > 3:

                if not init_image_done:
                    scan_list.append(value)
                else:
                    if value < avg * 3:
                        scan_list.append(value)
                    else:
                        # differences between images bigger i.e. start recording video and snap a foto
                        camera.capture('/home/pi/home_automation_project/src/picamera_motion/motion_videos/' +
                                      'image_' + str(init_count) + '.jpg', use_video_port=True)
                        camera.start_recording('/home/pi/home_automation_project/src/picamera_motion/motion_videos/' +
                                              'video_' + str(init_count) + '.h264')

                        camera.wait_recording(20)
                        camera.stop_recording()

                if len(scan_list) > 1:
                    stdev = round(statistics.stdev(scan_list), 2)

                # keep only 5 elements in the list with image scans
                if len(scan_list) == 6:
                    del scan_list[0]
                    avg = round(statistics.mean(scan_list), 2)
                    init_image_done = True
                    logging.info("avg: %s  stdev: %s", avg, stdev)
            init_count += 1

def run_app():
    """ flask app """
    app.run(host='0.0.0.0', port=5001, threaded=True)

@app.route('/motion_detect_disabled', methods=["GET"])
@app.route('/motion_detect_enabled', methods=["GET"])
def control_motion_detection():
    """ On/Off motion detection """
    global motion_detection_enabled

    command = request.path[1:]
    if command == 'motion_detect_enabled':
        motion_detection_enabled = True
    elif command == 'motion_detect_disabled':
        motion_detection_enabled = False

    return f" motion detect status: {motion_detection_enabled}" , 201

@app.route('/video_stream')
def video_stream():
    """ web stream """
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/video_noise")
def video_noise():
    return Response(generate_video_noise(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    try:
        flask_thread = threading.Thread(target=run_app)
        motion_detection_thread = threading.Thread(target=motion_detection)
        flask_thread.start()
        motion_detection_thread.start()
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        camera.close()
        print("Quitting threads")
      
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from picamera2 import Picamera2, Preview
import time
import cv2
import os
from threading import Thread
from yolov5 import YOLOv5
import multiprocessing
import serial
import struct

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)
lock = multiprocessing.Lock()

# Serial communication with Arduino
ser1 = serial.Serial('/dev/ttyAMA5', 9600, timeout=1)
ser2 = serial.Serial("/dev/ttyACM0", 9600)

# Global variables to store the current values
ultra_sonic_distance = 0
camera_feed = None
obstacle_type = None
system_status = 1
# Initial system state
car_locked = 2  # 1: unlocked, 2: locked
door_status = 1  # 1: closed, 2: open

# Control variable for serial communication
serial_comm_control = 1 # 0: write, 1: read

# Function to read ultra_sonic_distance from serial periodically
def read_distance_serial():
    global ultra_sonic_distance
    while True:
        try:
#             with lock:
                if ser1.in_waiting >= 4:
                    data = ser1.read(4)
                    value = struct.unpack('I', data)[0]
                    if value >= 1000000:
                        ser1.reset_input_buffer()
                        continue
                    ultra_sonic_distance = value / 100
                    ser1.reset_input_buffer()
                time.sleep(0.5) # Adjust the interval as needed
        except struct.error as e:
            print(f"Error unpacking data: {e}")
            ser1.reset_input_buffer()
        except Exception as e:
            print(f"Unexpected error: {e}")
            ser1.reset_input_buffer()

# Function to read and write door status from serial periodically
def read_write_door_serial():
    global system_status, car_locked, door_status
    while True:
        try:
            #  with lock:
                if ser2.in_waiting >= 4:
                    print("read1")
                    line = ser2.readline().decode('gbk').strip()
                    print("read2",line)
                    if line and len(line) >= 3:
                        print("read3")
                        system_status = int(line[0])
                        door_status = int(line[1])
                        car_locked = int(line[2])
                        print(system_status,"--",door_status,"--",car_locked)
                time.sleep(1)  # Adjust the interval as needed
        except Exception as e:
            print(f"Error in read_write_door_serial: {e}")

        
# Function to calculate system status
def calculate_system_status():
    global ultra_sonic_distance, obstacle_type, system_status
    if ultra_sonic_distance is None or obstacle_type is None:
        system_status = 1
        print("ultra_sonic_distance or obstacle_type is None", system_status)
        update_serial_status()
        return

    if obstacle_type.lower() == 'pedestrian':
        if 0 <= ultra_sonic_distance < 20:
            system_status = 3
            print("system_status: ", system_status)
        elif 20 <= ultra_sonic_distance < 35:
            system_status = 2
            print("system_status: ", system_status)
        else:
            system_status = 1
            print("system_status: ", system_status)
    elif obstacle_type.lower() == 'car':
        if 0 <= ultra_sonic_distance < 20:
            system_status = 3
            print("system_status: ", system_status)
        elif 20 <= ultra_sonic_distance < 50:
            system_status = 2
            print("system_status: ", system_status)
        else:
            system_status = 1
            print("system_status: ", system_status)
    else:
        system_status = 1
        print("system_status: ", system_status)
    update_serial_status()
    return

# YOLOv5 Initialization
model = YOLOv5("/home/pi/DL-PART/DLP/yolov5s.pt")
# Function to handle YOLO model prediction
def yolo_prediction(picam2):
    global obstacle_type
    while True:
        frame = picam2.capture_array()
        if frame is None:
            app.logger.warning("Captured frame is None.")
            continue
        
        # Perform object detection
        results = model.predict(frame)
        detected_objects = []
        for *xyxy, conf, cls in results.xyxy[0]:
            label = f'{model.model.names[int(cls)]} {conf:.2f}'
            print(f"置信度最高项： {label}")
            class_label = label.split(' ')[0]
            if class_label.lower() == 'person':
                detected_objects.append('pedestrian')
            else:
                detected_objects.append('car')

        # Update the global obstacle_type with the detected objects
        if detected_objects:
            obstacle_type = detected_objects[0]  # Use the first detected object
        else:
            obstacle_type = "None"

        calculate_system_status()
        time.sleep(1)  # Adjust the interval as needed

def initialize_camera():
    retries = 5
    for i in range(retries):
        try:
            picam2 = Picamera2()
            picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
            picam2.start()
            app.logger.info("Camera started successfully.")
            return picam2
        except Exception as e:
            app.logger.error(f"Failed to initialize camera (attempt {i+1}/{retries}): {e}")
            time.sleep(2)  # Wait before retrying
    raise RuntimeError("Failed to initialize camera after multiple attempts")

# Function to generate video feed for the web interface
def video_feed_generator(picam2):
    try:
        while True:
            frame = picam2.capture_array()
            if frame is None:
                app.logger.warning("Captured frame is None.")
                continue

            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                app.logger.warning("Failed to encode frame.")
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
    finally:
        picam2.stop()
        app.logger.info("Camera stopped successfully.")

@app.route('/api/video_feed')
def video_feed():
    picam2 = initialize_camera()
    Thread(target=yolo_prediction, args=(picam2,)).start()
    return Response(video_feed_generator(picam2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/ultra_sonic_distance', methods=['POST'])
def update_distance():
    global ultra_sonic_distance
    data = request.json
    ultra_sonic_distance = data.get('ultra_sonic_distance')
    calculate_system_status()
    return jsonify({'message': 'Distance updated', 'ultra_sonic_distance': ultra_sonic_distance})

@app.route('/api/obstacle_type', methods=['POST'])
def update_obstacle_type():
    global obstacle_type
    data = request.json
    obstacle_type = data.get('obstacle_type')
    calculate_system_status()
    return jsonify({'message': 'Obstacle type updated', 'obstacle_type': obstacle_type})

@app.route('/api/system_status', methods=['POST'])
def update_system_status():
    global system_status
    data = request.json
    system_status = data.get('system_status')
    return jsonify({'message': 'System status updated', 'system_status': system_status})

@app.route('/api/unlock', methods=['POST'])
def unlock_control():
    global car_locked, serial_comm_control
    if car_locked == 2:
        car_locked = 1
        serial_comm_control = 1
        print('UNLOCK PRESSED')
        update_serial_status()
        return jsonify({'message': 'Car unlocked', 'lock_status': car_locked})
    elif car_locked == 1:
        car_locked = 2
        serial_comm_control = 1
        print('LOCK PRESSED')
        update_serial_status()
        return jsonify({'message': 'Car locked', 'lock_status': car_locked})

@app.route('/api/open', methods=['POST'])
def open_door():
    global car_locked, door_status, system_status, serial_comm_control
    if door_status == 1:
        if car_locked == 2:
            return jsonify({'message': 'Car door cannot be opened as the car is locked'})
        elif car_locked == 1 and (system_status == 1 or 2):
            door_status = 2

            serial_comm_control = 1
            update_serial_status()
            return jsonify({'message': 'Car door opened', 'lock_status': car_locked, 'door_status': door_status})
        elif car_locked == 1 and system_status == 3:
            door_status = 2
            update_serial_status()
            # time.sleep(0.2)
            door_status = 1
            car_locked = 2

            serial_comm_control = 1
            update_serial_status()
            return jsonify({'message': 'Cannot open door due to urgent status. Door locked.', 'lock_status': car_locked, 'door_status': door_status})
    else:
        door_status = 1

        serial_comm_control = 1
        update_serial_status()
        return jsonify({'message': 'Car door closed', 'lock_status': car_locked, 'door_status': door_status})


@app.route('/api/current_data', methods=['GET'])
def get_current_data():
    global ultra_sonic_distance, obstacle_type, system_status, car_locked, door_status
    return jsonify({
        'ultra_sonic_distance': ultra_sonic_distance,
        'obstacle_type': obstacle_type,
        'system_status': system_status,
        'lock_status': car_locked,
        'door_status': door_status
    })

def update_serial_status():
    global system_status, car_locked, door_status, serial_comm_control
    try:
#         with lock:
            pdu = 100 * system_status + 10 * door_status + car_locked
            ser2.write(str(pdu).encode('utf-8'))
            print("update_serial_status: ", pdu)
            serial_comm_control = 1
    except Exception as e:
        print(f"Error updating serial status: {e}")

    
if __name__ == '__main__':
    # Start the threads to read/write serials periodically
    Thread(target=read_distance_serial).start()
    Thread(target=read_write_door_serial).start()

    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
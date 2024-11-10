# **Blind Spot Detection Enhanced with IoT and ML**

## **Overview**
The Blind Spot Detection (BSD) system is designed to enhance vehicle safety by providing real-time alerts about objects entering the car's blind spot. The system uses a combination of IoT (Internet of Things) and Machine Learning (ML) to detect and identify objects (vehicles, pedestrians, etc.) in the blind spot and notify the driver of potential hazards. The solution aims to deliver proactive visual and auditory alerts to ensure the safety of vehicle occupants.

### **Objective**
This project integrates object detection through machine learning, ultrasonic sensor-based distance measurement, and IoT-based notification systems to create an effective blind spot warning system. The system provides alerts when objects enter the vehicle's blind spot and estimates the distance to potential hazards, allowing the driver to take preventive action.

## **Key Features**
- **Real-time Object Detection**: The system uses YOLOv5s (You Only Look Once) for detecting objects such as vehicles, pedestrians, or stationary objects in the blind spot.
- **Distance Estimation**: Ultrasonic sensors estimate the distance between the car and objects approaching the blind spot.
- **Alerts**: The system triggers visual and auditory alerts through a micro:bit when a potential collision risk is detected.
- **Local Processing**: The image processing and object detection are handled locally on a Raspberry Pi, enabling fast and efficient decision-making without relying on cloud computing.

## **System Architecture**
- **Raspberry Pi 4 Model B**: Acts as the central processing unit for handling image processing and object detection using the YOLOv5s model.
- **Camera Module**: A Raspberry Pi Camera Module captures real-time images of the car’s surroundings to detect objects in the blind spot.
- **Ultrasonic Sensors**: These sensors provide distance measurements, which help assess the proximity of detected objects.
- **ESP32**: A microcontroller that helps manage communication between sensors, the Raspberry Pi, and the micro:bit.
- **Micro:bit**: A small programmable device that is used to activate visual and auditory alerts when potential risks are detected.

## **Installation & Setup**

### 1. **Hardware Setup**:
   - Attach the Raspberry Pi Camera Module to the Raspberry Pi 4 Model B.
   - Connect the ultrasonic sensors to the GPIO pins of the Raspberry Pi.
   - Connect the ESP32 and micro:bit for communication.
   - Ensure all components are securely mounted on the vehicle.

### 2. **Software Setup**:
   - Install the necessary dependencies on the Raspberry Pi for YOLOv5s model and object detection:
     - Python 3.x
     - OpenCV for image processing
     - PyTorch for running the YOLO model
   - Set up the ultrasonic sensor libraries to communicate with the Raspberry Pi.
   - Program the micro:bit to handle alert signals from the Raspberry Pi.

### 3. **Running the System**:
   - Once the system is set up, power on the Raspberry Pi and ensure all components are connected correctly.
   - The Raspberry Pi will start capturing images, processing them through the YOLOv5s model, and checking the proximity of detected objects using the ultrasonic sensors.
   - If an object enters the blind spot and is deemed a risk, the micro:bit will trigger an alert to the vehicle occupants.

## **Future Improvements**
- **Cloud Integration**: Implement cloud-based processing for additional data analytics and improving object recognition accuracy.
- **Advanced Alert Systems**: Use haptic feedback or integrate the system with the vehicle's existing alert mechanisms (e.g., steering wheel vibration).
- **Additional Sensors**: Add more sensors to cover a larger area and improve detection accuracy.

## **License**
This project is licensed under the MIT License. See LICENSE for more details.

## **Contact**
For more information, issues, or contributions, please contact [aaravrana@outlook.com]. 

## **References**

1. **YOLOv5: You Only Look Once (v5)**
   - "YOLOv5" is a state-of-the-art real-time object detection model. YOLO is used here for detecting vehicles, pedestrians, and other objects in the blind spot.
     - [YOLOv5 on GitHub](https://github.com/ultralytics/yolov5)
     - [YOLOv5: A Guide to Object Detection](https://towardsdatascience.com/yolov5-object-detection-for-beginners-4b1d2ff377d9)

2. **Raspberry Pi 4 Model B**
   - The Raspberry Pi 4 is the main processing unit in this system. It provides sufficient computational power for running object detection locally.
     - [Raspberry Pi 4 Documentation](https://www.raspberrypi.org/documentation/)
     - [Raspberry Pi 4 Model B Overview](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)

3. **Ultrasonic Sensors for Distance Measurement**
   - Ultrasonic sensors are used to measure the distance between objects and the vehicle, helping assess the risk of collision.
     - [HC-SR04 Ultrasonic Sensor Datasheet](https://www.electronicwings.com/nodemcu/hc-sr04-ultrasonic-sensor)
     - [How Ultrasonic Sensors Work](https://www.robotshop.com/community/forum/t/understanding-ultrasonic-sensors/18119)

4. **micro:bit**
   - The micro:bit is used to trigger visual and auditory alerts based on the detection results from the Raspberry Pi.
     - [micro:bit Official Website](https://microbit.org/)
     - [micro:bit Documentation](https://microbit.org/guide/)

5. **Blind Spot Detection Systems**
   - An overview of how modern blind spot detection systems work in vehicles, including IoT and sensor integration.
     - [How Blind Spot Detection Works](https://www.safety.com/blind-spot-detection/)
     - [Blind Spot Detection: How It Helps and Why You Need It](https://www.autobahnautomotive.com/blog/blind-spot-detection/)
     - [Advanced Driver Assistance Systems (ADAS)](https://www.nhtsa.gov/technology-innovation/advanced-driver-assistance-systems)

6. **ESP32 Microcontroller**
   - The ESP32 is used for communication between the Raspberry Pi and the micro:bit, as well as for general IoT functionality.
     - [ESP32 Overview](https://www.espressif.com/en/products/socs/esp32)
     - [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)

7. **OpenCV for Image Processing**
   - OpenCV is used for image manipulation and preprocessing before passing it to the YOLOv5 model for object detection.
     - [OpenCV Documentation](https://docs.opencv.org/master/)
     - [OpenCV Introduction and Tutorials](https://opencv-python-tutroals.readthedocs.io/en/latest/)

8. **PyTorch for Running YOLOv5**
   - PyTorch is the deep learning framework used for running the YOLOv5 model locally on the Raspberry Pi.
     - [PyTorch Official Website](https://pytorch.org/)
     - [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

#-*- coding:utf-8 -*-
import threading
import time
from sensor.distance_sensor import DistanceSensor

class DistanceSensorThread:

    distanceSensor = None

    def __init__(self, running, broker):
        self.broker = broker
        self.running = running
        self.start = False
        DistanceSensorThread.distanceSensor = DistanceSensor()
        self.exception = False
        threading.Thread(target=self.startThread, name="iot-sensor-thread", args=()).start()

    def startThread(self):
        print("Starting sensorThread")
        while (not self.start and self.running):
            print("Waiting for startMeasurement() call... ")
            time.sleep(1)
        print("Starting measurement")
        try:
            while self.running:
                valueRead = DistanceSensorThread.distanceSensor.read_value()
                self.broker.publish("iot-distance-sensor/data", valueRead)
                time.sleep(1.0)
            # Clean up!
            print("SensorThread stopped")
        except Exception:
            self.exception = True
        finally:
            del DistanceSensorThread.distanceSensor

    def set_running(self, running):
        self.running = running
        
    def startMeasurement(self):
        self.start = True
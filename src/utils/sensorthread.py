#-*- coding:utf-8 -*-
import threading
import time
from sensor.distance_sensor import DistanceSensor
from alerts.alert_service import AlertService
from dhbw_iot_csv.csv_writer import CsvWriter

class DistanceSensorThread:

    distanceSensor = None
    running = False

    def __init__(self, running, broker):
        DistanceSensorThread.broker = broker
        DistanceSensorThread.running = running
        print("Starting sensorThread: ", DistanceSensorThread.running)
        distanceSensor = DistanceSensor()
        threading.Thread(target=self.startThread, name="iot-sensor-thread", args=(distanceSensor,broker)).start()
        DistanceSensorThread.alertService = AlertService(30, broker)

    def startThread(self, distanceSensor, broker):
        DistanceSensorThread.distanceSensor = distanceSensor
        while DistanceSensorThread.running:
            valueRead = DistanceSensorThread.distanceSensor.read_value()
            self.broker.publish("iot-distance-sensor/data", valueRead)
            print(valueRead)
            time.sleep(1.0)
        # Clean up!
        print("SensorThread stopped")
        del DistanceSensorThread.distanceSensor

    def set_running(self, running):
        DistanceSensorThread.running = running

    def close(self):
        DistanceSensorThread.running = False
        
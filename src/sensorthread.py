#-*- coding:utf-8 -*-
import threading
import time
from sensor.distance_sensor import DistanceSensor
from alerts.alert_service import AlertService
from dhbw_iot_csv.csv_writer import CsvWriter

class DistanceSensorThread:

    distanceSensor = None
    running = False
    csv_writer = None

    def __init__(self, running, csv_writer):
        DistanceSensorThread.running = running
        DistanceSensorThread.csv_writer = csv_writer
        print("Starting sensorThread: ", DistanceSensorThread.running)
        distanceSensor = DistanceSensor()
        threading.Thread(target=self.startThread, name="iot-sensor-thread", args=(distanceSensor,)).start()
        DistanceSensorThread.alertService = AlertService(30)

    def startThread(self, distanceSensor):
        DistanceSensorThread.distanceSensor = distanceSensor
        while DistanceSensorThread.running:
            valueRead = DistanceSensorThread.distanceSensor.read_value()
            DistanceSensorThread.csv_writer.write_line(valueRead)
            if int(valueRead["distance"]) < int(AlertService.alertDistance):
                DistanceSensorThread.alertService.on_distance_threshold_passed(valueRead["distance"])
            print(valueRead)
            time.sleep(1.0)
        # Clean up!
        print("Cleaning up GPIO pins")
        DistanceSensorThread.distanceSensor.clean()

    def set_running(self, running):
        DistanceSensorThread.running = running
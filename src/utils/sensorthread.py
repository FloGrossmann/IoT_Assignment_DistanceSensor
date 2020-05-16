#-*- coding:utf-8 -*-
import threading
import time
from sensor.distance_sensor import DistanceSensor
from loguru import logger

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
        logger.info("Starting sensorThread")
        while (not self.start and self.running):
            logger.info("Waiting until mqtt is ready (startMeasurement() call) ")
            time.sleep(1)
        logger.info("Beginning measurement")
        try:
            while self.running:
                valueRead = DistanceSensorThread.distanceSensor.read_value()
                logger.debug(valueRead)
                if int(valueRead["distance"]) < 2 or int(valueRead["distance"]) > 300:
                    # Just print a warning if we measure things outside of the given sensor range
                    logger.warning("unsafe measurement {}, because it is < 2cm or > 300cm - outside of sensor spec!", valueRead)
                self.broker.publish("iot-distance-sensor/data", valueRead)
                time.sleep(1.0)

            # Clean up!
            logger.info("SensorThread stopped")
        except Exception:
            self.exception = True
        finally:
            del DistanceSensorThread.distanceSensor

    def set_running(self, running):
        self.running = running
        
    def startMeasurement(self):
        self.start = True
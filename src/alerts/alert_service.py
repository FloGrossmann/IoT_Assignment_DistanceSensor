#-*- coding:utf-8 -*-
import time
from loguru import logger

class AlertService: # Service Reagiert auf Messwerte

    alertDistance = 30
    #  Initialisierung
    def __init__(self, startDistance, broker):
        self.broker = broker
        self.broker.sub("iot-distance-sensor/data", self.checkAlert)
        self.broker.sub("iot-distance-sensor/alarmthreshold", self.setAlertThreshold)
        AlertService.alertDistance = startDistance

    #  value:  Neuer Schwellwert als einfache Zahl in der Einheit cm wird hier übergeben
    def setAlertThreshold(self, value):
        logger.info("Setting new alert threshold to {} cm", value)
        AlertService.alertDistance = value #min(300,value) # Der Sensorschwellwert darf nicht über die Grenzen der Hardware raus

    #  value:  Aktuell gemessener Wert (siehe DistanceSensor) wird übergeben und es wird ein Alarm gesendet
    def on_distance_threshold_passed(self, dictRead):
        logger.warning("Alert!! Distance is less than: {} cm: {} cm detected", AlertService.alertDistance, dictRead["distance"])
        self.broker.publish("iot-distance-sensor/alarm", dictRead)

    def checkAlert(self, dictRead):
        if int(dictRead["distance"]) < int(AlertService.alertDistance):
            self.on_distance_threshold_passed(dictRead)
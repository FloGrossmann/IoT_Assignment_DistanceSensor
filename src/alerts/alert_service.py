#-*- coding:utf-8 -*-
import time

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
        print("Setting new alert threshold to ", value, "cm")
        AlertService.alertDistance = value #min(300,value) # Der Sensorschwellwert darf nicht über die Grenzen der Hardware raus

    #  value:  Aktuell gemessener Wert (siehe DistanceSensor) wird übergeben und es wird ein Alarm gesendet
    def on_distance_threshold_passed(self, dictRead):
        print("Alert!! Distance is less than: ", AlertService.alertDistance, "cm")
        self.broker.publish("iot-distance-sensor/alarm", dictRead)

    def checkAlert(self, dictRead):
        if int(dictRead["distance"]) < int(AlertService.alertDistance):
            self.on_distance_threshold_passed(dictRead)
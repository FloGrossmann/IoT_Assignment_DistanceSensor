#-*- coding:utf-8 -*-
class AlertService: # Service Reagiert auf Messwerte

    alertDistance = 30

    #  Initialisierung
    def __init__(self, startDistance, broker):
        self.broker = broker
        broker.sub("iot-distance-sensor/data", self.checkAlert)
        AlertService.alertDistance = startDistance

    #  value:  Neuer Schwellwert als einfache Zahl in der Einheit cm wird hier übergeben
    def set_alert_threshold (self, value):
        AlertService.alertDistance = value

    #  value:  Aktuell gemessener Wert (siehe DistanceSensor) wird übergeben und es wird ein Alarm gesendet
    def on_distance_threshold_passed(self, value):
        print("Alert!! Distance is less than: ", AlertService.alertDistance)
        self.broker.publish("iot-distance-sensor/alarm", value)

    def checkAlert(self, dictRead):
        if int(dictRead["distance"]) < int(AlertService.alertDistance):
            self.on_distance_threshold_passed(dictRead)
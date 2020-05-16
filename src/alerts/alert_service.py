#-*- coding:utf-8 -*-
class AlertService: # Service Reagiert auf Messwerte

    alertDistance = 30

    #  Initialisierung
    def __init__(self, startDistance):
        AlertService.alertDistance = startDistance
        pass

    #  value:  Neuer Schwellwert als einfache Zahl in der Einheit cm wird hier übergeben
    def set_alert_threshold (self, value):
        AlertService.alertDistance = value
        pass

    #  value:  Aktuell gemessener Wert (siehe DistanceSensor) wird übergeben und es wird ein Alarm gesendet
    def on_distance_threshold_passed(self, value):
        print("Alert!! Distance is less than: ", AlertService.alertDistance)
        pass
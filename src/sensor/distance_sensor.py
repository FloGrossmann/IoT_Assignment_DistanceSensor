#-*- coding:utf-8 -*-

import time, datetime
import RPi.GPIO as GPIO
import threading
from loguru import logger

class DistanceSensor:

    # Hier können die jeweiligen Eingangs-/Ausgangspins ausgewählt werden
    Trigger_AusgangsPin = 17
    Echo_EingangsPin    = 27

    # Trigger-Pin: Benötigt ein 10µs langes Startsignal (rotes Kabel)
    # Danach wird am Echo-Ausgangspin das Signal aktiviert, bis die Messung erfolgt ist (gelbes Kabel)
    # --> Active High solange, bis Signal zurück ist
    #  Initialisierung
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DistanceSensor.Trigger_AusgangsPin, GPIO.OUT)
        GPIO.setup(DistanceSensor.Echo_EingangsPin, GPIO.IN)
        GPIO.output(DistanceSensor.Trigger_AusgangsPin, False)
        logger.trace("DistanceSensor setup")

    #  return Wert als Dictionary entsprechend folgendem JSON:
    #   { 
    #     "sensorId"  : "KY-050", 
    #     "timestamp" : "2020-03-01T12:00:01.345+01:00",
    #     "distance" : 42,
    #     "unit" : "cm"
    #   }
    def read_value(self):
        logger.trace("read new value")
        # Abstandsmessung wird mittels des 10us langen Triggersignals gestartet
        GPIO.output(DistanceSensor.Trigger_AusgangsPin, True)
        time.sleep(0.00001)
        GPIO.output(DistanceSensor.Trigger_AusgangsPin, False)

        # Hier wird die Stopuhr gestartet
        starttime = time.time()
        while GPIO.input(DistanceSensor.Echo_EingangsPin) == 0:
            starttime = time.time() # Es wird solange die aktuelle Zeit gespeichert, bis das Signal aktiviert wird
 
        while GPIO.input(DistanceSensor.Echo_EingangsPin) == 1:
            stoptime = time.time() # Es wird die letzte Zeit aufgenommen, wo noch das Signal aktiv war
 
        # Die Differenz der beiden Zeiten ergibt die gesuchte Dauer
        took = stoptime - starttime
        # Mittels dieser kann nun der Abstand auf Basis der Schallgeschwindigkeit der Abstand berechnet werden
        distance = format((took * 34300) / 2,'0.0f')

        return {
                "sensorId": "KY-050",
                "timestamp": datetime.datetime \
                .fromtimestamp(time.time()).isoformat(),
                "distance": distance,
                "unit": "cm"
                }

    def __del__(self):
        logger.info("Cleaning up GPIO pins")
        GPIO.cleanup()
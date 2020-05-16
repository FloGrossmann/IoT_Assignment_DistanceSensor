#-*- coding:utf-8 -*-
import time
from dhbw_iot_csv.csv_writer import CsvWriter
from utils.sensorthread import DistanceSensorThread
from utils.messageBroker import MessageBroker
# Start der Anwendung

if __name__ == "__main__":
    
    running = True 
    broker = MessageBroker()

    csvHeader = ['sensorId', 'timestamp', 'distance', 'unit']
    csv_writer = CsvWriter("log.csv", csvHeader, broker)

    handlers = [
        DistanceSensorThread(running, broker)
        ]

    #if handlers[0].exception: 
    #    handlers[0].set_running(False)
    #    raise Exception("Exception while reading data")

    try:
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        handlers[0].set_running(False)
        for handler in handlers:
            if hasattr(handler, "close"):
                handler.close()
                del handler
        print("\nKeyboardInterrupt in Main Loop")
        del csv_writer
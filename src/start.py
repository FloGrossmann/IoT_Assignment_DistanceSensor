#-*- coding:utf-8 -*-
import time, sys
from dhbw_iot_csv.csv_writer import CsvWriter
from alerts.alert_service import AlertService
from utils.sensorthread import DistanceSensorThread
from utils.messageBroker import MessageBroker
from utils.mqtt import MQTTManager
from loguru import logger
import json

# Start der Anwendung
if __name__ == "__main__":

    logger.add
    logger.info('Started distance Measure Application')
    # Read config
    with open('./config/brokerConfig.json') as config_file:
        config = json.load(config_file)
        logger.info('Loaded config {}', config)
    
    running = True 
    broker = MessageBroker()

    csvHeader = ['sensorId', 'timestamp', 'distance', 'unit']
    csv_writer = CsvWriter("data.csv", csvHeader, broker)
    alert_service = AlertService(30, broker)

    threatHandler = [
        DistanceSensorThread(running, broker),
        MQTTManager(running, broker, config)
        ]

    try:
        
        # Wait until the connection to the broker has been established
        while not threatHandler[1].connected:
            logger.info("Connecting to mqtt host...")
            if threatHandler[1].exception:
                running = False
                threatHandler[0].set_running(False)
                logger.critical("Could not connect to mqtt broker. Configured Host: {} and port: {}", config["broker_host"], config["broker_port"])
                raise Exception("Could not connect to mqtt broker. Configured Host: ", config["broker_host"], " and port: ", config["broker_port"])
            time.sleep(1)

        # Now we can start the measurement
        threatHandler[0].startMeasurement()

        # Main loop
        while running:
            for handler in threatHandler:
                if handler.exception:
                    logger.error("threatHandler {} threw exception", handler)
                    for handler in threatHandler:
                        handler.set_running(False)
                    raise Exception("Exception in thread: ", handler, "stopping all..")
            time.sleep(5)

    except (KeyboardInterrupt, Exception) as e:
        for handler in threatHandler:
            handler.set_running(False)
            del handler
        logger.error("Stopping Main Loop\n {}", str(e))
        del csv_writer
        del alert_service
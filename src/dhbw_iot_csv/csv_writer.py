#-*- coding:utf-8 -*-
import os
import json
import csv
from loguru import logger

class CsvWriter:

    #  Initialisierung
    def __init__(self, filename, fieldnames, broker):
        self.broker = broker
        self.broker.sub("iot-distance-sensor/data", self.write_line)
        self.filename = filename
        self.fieldnames = fieldnames
        # Need to os.path.exists before opening file -> opening file creates it if it is not there
        writeheaders = False
        if not os.path.exists(self.filename):
            logger.info("Creating the csv-file {} to store data", self.filename)
            writeheaders = True
        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            # Check if the csv-file already exists
            if writeheaders:
                writer.writeheader()


    #  line: ist die bereits formatierte Zeile, die nur noch geschrieben wird.
    def write_line (self, line):
        logger.trace("Writing line: {} to csv", line)
        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writerow(line)

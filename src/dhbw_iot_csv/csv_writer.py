#-*- coding:utf-8 -*-
import os
import json
import csv

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
            writeheaders = True
        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            # Check if the csv-file already exists
            if writeheaders:
                writer.writeheader()


    #  line: ist die bereits formatierte Zeile, die nur noch geschrieben wird.
    def write_line (self, line):
        print(self.fieldnames)
        print("Writing line: ", line)
        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, self.fieldnames)
            writer.writerow(line)

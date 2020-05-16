import paho.mqtt.client as mqtt
import json
import threading

class MQTTManager:
	
	mqttClient = None

	def __init__(self, running, broker, config):
		try:
			self.running = running
			self.connected = False
			# Setup the mqtt client
			self.config = config
			self.mqttClient = mqtt.Client()
			self.mqttClient.connect(self.config["broker_host"], self.config["broker_port"])
			self.mqttClient.on_message = self.on_MQTTMessage
			self.mqttClient.subscribe(self.config["config_topic"], qos=1)
			print("Subscribed to mqtt topic: ", self.config["config_topic"])

			# Listen to the broker topics
			self.broker = broker
			self.broker.sub("iot-distance-sensor/data", self.writeData)
			self.broker.sub("iot-distance-sensor/alarm", self.writeAlarm)
			
			self.exception = False
			self.connected = True
			threading.Thread(target=self.run, name="iot-mqtt-thread", args=()).start()
			
		except Exception:
			self.exception = True

	def run(self):
		print("Starting MQTT Thread")
		while self.running:
				self.mqttClient.loop_start()
		print("MQTT Thread stopped")

	def set_running(self, running):
		self.running = running

	def writeData(self, message):
		#print("Publishing data to topic " + self.config["data_topic"])
		self.mqttClient.publish(topic=self.config["data_topic"], payload=json.dumps(message), qos=1, retain=False)

	def writeAlarm(self, message):
		#print("Publishing alarm to topic " + self.config["alert_topic"])
		self.mqttClient.publish(topic=self.config["alert_topic"], payload=json.dumps(message), qos=1, retain=False)

	def on_MQTTMessage(self, client, userdata, message):
		newThreshold = int(message.payload.decode())
		print("Received new alert threshold setting: ", newThreshold)
		if message.topic == self.config["config_topic"]:
			self.broker.publish("iot-distance-sensor/alarmthreshold", newThreshold)
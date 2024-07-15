import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

BROKER = 'localhost'
PORT = 1883

def publish_sensor_data():
    client = mqtt.Client()
    try:
        client.connect(BROKER, PORT)
    except Exception as e:
        print(e)
    sensor_ids = ["sensor_1", "sensor_2", "sensor_3"]

    while True:
        for sensor_id in sensor_ids:
            temperature = round(random.uniform(20.0, 30.0), 2)
            humidity = round(random.uniform(30.0, 60.0), 2)
            payload_temp = {
                "sensor_id": sensor_id,
                "value": temperature,
                "timestamp": datetime.now().isoformat()
            }
            payload_humidity = {
                "sensor_id": sensor_id,
                "value": humidity,
                "timestamp": datetime.now().isoformat()
            }
            client.publish("sensors/temperature", json.dumps(payload_temp))
            client.publish("sensors/humidity", json.dumps(payload_humidity))
            print(f"Published temperature: {json.dumps(payload_temp)}")
            print(f"Published humidity: {json.dumps(payload_humidity)}")
            #time.sleep(5)
        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()

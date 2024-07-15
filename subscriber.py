import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import redis

BROKER = 'localhost'
PORT = 1883
MONGO_URI = "mongodb://localhost:27017"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.sensor_data
collection = db.readings

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("sensors/#")
from bson import ObjectId

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)

        print(f"Received message: {json.dumps(payload)}")
        print(payload)
        
        # Convert ObjectId to string for JSON serialization

        
        try:
            collection.insert_one(payload)
            print("Collection Inserted")
        except Exception as e:
            print(e)
        sensor_id = payload["sensor_id"]
        print(sensor_id)
        redis_key = f"sensor:{sensor_id}:last_10_readings"
        redis_client.lpush(redis_key, {json.dumps(payload)})

        redis_client.ltrim(redis_key, 0, 9)
        # print(f"Stored in Redis (last 10 readings for {sensor_id}): {json.dumps(payload)}")
    
    except Exception as e:
        print(f"Exception occurred while processing message: {e}")

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()

except KeyboardInterrupt:
    print("Program interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.disconnect()
    mongo_client.close()

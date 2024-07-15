from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import redis
import json
from datetime import datetime

app = FastAPI()

MONGO_URI = "mongodb://localhost:27017"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.sensor_data
collection = db.readings

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

@app.get("/sensor_readings/")
def get_sensor_readings(start: str, end: str):
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    readings = list(collection.find({
        "timestamp": {
            "$gte": start,
            "$lte": end
        }
    }))
    for reading in readings:
        reading["_id"] = str(reading["_id"])
    return readings

@app.get("/last_ten_readings/{sensor_id}")
def get_last_ten_readings(sensor_id: str):
    redis_key = f"sensor:{sensor_id}:last_10_readings"
    readings = redis_client.lrange(redis_key, 0, -1)
    parsed_readings = []
    for reading in readings:
        reading_str = reading.decode('utf-8').strip() 
        if reading_str.startswith('{') and reading_str.endswith('}'):
            try:
                parsed_reading = {}
                parts = reading_str[1:-1].split(', ')
                for part in parts:
                    key, value = part.split(': ')
                    key = key.strip("'")
                    if key == '_id':
                        value = value.strip("ObjectId('").strip("')")
                    else:
                        value = value.strip("'")
                    parsed_reading[key] = value
                parsed_readings.append(parsed_reading)
            except Exception as e:
                print(f"Error parsing reading: {e}")
    return parsed_readings

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# mqqt

## introduction
Purpose: Simulate the behaviour of sensors, monitor their readings, and provide APIs to retrieve data based on specific criteria.
MQTT Broker Setup: Deploy a Mosquitto MQTT broker using Docker.
MQTT Publisher: Create a Python MQTT client to mimic multiple sensor readings, publishing to topics like sensors/temperature and sensors/humidity.
Structure of the JSON payload

{ "sensor_id": "unique_sensor_id", "value": "<reading_value>", "timestamp": "ISO8601_formatted_date_time" }

MQTT Subscriber: Construct a Python MQTT subscriber to store the received messages in a MongoDB collection.
Data Storage: Initiate a MongoDB instance using Docker and save the incoming MQTT messages.
In-Memory Data Management: Implement Redis using Docker to store the latest ten sensor readings.

## Prerequisites

Ensure you have installed following on your machine:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/) (if running Python scripts outside Docker)

- pull mongodb and redis from docker


## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Build and start the Docker containers:

    ```bash
    docker-compose up -d --build
    ```

    This command will build the Docker images as defined in your `docker-compose.yml` file and start the containers in detached mode.

## Running the Python Scripts

After the containers are up and running, you can execute your Python scripts.
python publisher.py
python subscriber.py


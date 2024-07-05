import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import time
import json
import random
from ServerRaumHTTPHandler import ServerRaumHTTPHandler

try:
    import RPi.GPIO as gpio
    gpio.setmode(gpio.BCM)
    pin = 23
    gpio.setup(pin, gpio.IN)

    ISRASPI = True
except:
    ISRASPI = False


def getWaterValue():
    if not ISRASPI:
        return random.random() > 0.5

    rain = gpio.input(pin)
    return rain

def getTempValue(id):
    if not ISRASPI:
        return random.randint(0, 40) * random.random()

    path = f"/sys/bus/w1/devices/{id}/w1_slave"
    fin = open(path, "r")
    fin.readline()
    line = fin.readline().strip()
    pos = line.rfind("=") +1
    try:
        temp = float(line[pos:]) / 1000
    except:
        temp = float("Nan")
    fin.close()
    return temp


def run(client: mqtt.Client, room: int, interval:int, tempLimit: float, sensorID):
    while True:
        data = (room,
                getWaterValue(),
                getTempValue(sensorID),
                tempLimit)

        client.publish("sensorclient/data", json.dumps(data))
        print("Data send: " + str(data))

        time.sleep(interval)

        ServerRaumHTTPHandler.temp = getTempValue(sensorID)
        ServerRaumHTTPHandler.water = getWaterValue()


def main(room, start_server=True):
    load_dotenv()
    broker_ip = os.getenv("BROKER_IP")
    interval = os.getenv("INTERVAL_TIME")
    temp_limit = os.getenv("TEMP_LIMIT")
    sensor_id = os.getenv("SENSOR_ID")

    if room is None: raise
    if broker_ip is None: raise
    if interval is None: raise
    if temp_limit is None: raise
    if sensor_id is None: raise

    room = int(room)
    interval = int(interval)
    temp_limit = int(temp_limit)
    
    print("Client starting")
    print(f"room: {room}")
    print(f"brokerIP: {broker_ip}")
    print(f"interval: {interval}")
    print(f"limit: {temp_limit}")

    # MQTT Setup
    client = mqtt.Client("SensorClient Raum: " + str(room))
    client.connect(broker_ip)
    client.loop_start()
    

    if start_server:
        ServerRaumHTTPHandler.run(1111)
        ServerRaumHTTPHandler.room = room
        ServerRaumHTTPHandler.tlimit = temp_limit 

    run(client, room, interval, temp_limit, sensor_id)


if __name__ == '__main__':
    load_dotenv()
    room = os.getenv("ROOM")

    main(room)

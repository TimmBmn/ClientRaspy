import paho.mqtt.client as mqtt
import time
import json
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
        return 1

    rain = gpio.input(pin)
    return rain

def getTempValue(id):
    if not ISRASPI:
        return 30

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

        time.sleep(interval)

        ServerRaumHTTPHandler.temp = getTempValue(sensorID)
        ServerRaumHTTPHandler.water = getWaterValue()


def main():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found")
        return

    try:
        room: int = data["room"]
        brokerIP: str = data["brokerIP"]
        interval: int = data["intervalTime"]
        tempLimit: float = data["tempLimit"]
        ownIP: str = data["ownIP"]
        sensorID: str = data["sensorID"]
    except KeyError:
        print("config.json configured wrong")
        return

    
    print("Client starting")
    print(f"room: {room}")
    print(f"brokerIP: {brokerIP}")
    print(f"interval: {interval}")
    print(f"limit: {tempLimit}")

    # MQTT Setup
    client = mqtt.Client("SensorClientRoom" + str(room))
    client.connect(brokerIP)
    client.loop_start()
    

    ServerRaumHTTPHandler.run(ownIP, 1111)
    ServerRaumHTTPHandler.room = room
    ServerRaumHTTPHandler.tlimit = tempLimit 

    run(client, room, interval, tempLimit, sensorID)


if __name__ == '__main__':
    main()

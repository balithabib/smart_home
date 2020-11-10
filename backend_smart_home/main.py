import time

import aiohttp as aiohttp
import serial

import requests

HOST = '127.0.0.1'
PORT = '5000'
URL = 'http://' + HOST + ':' + PORT + '/_get_weather'

client = aiohttp.ClientSession()


def get_temperature_and_humidity(msg):
    # [temperature, humidity]
    return msg.decode('utf-8').split(';')[0].split(',')


def read():
    while True:
        current_char = ser.readline()
        [temperature, humidity] = get_temperature_and_humidity(current_char)
        print('------------------------->', [temperature, humidity])
        result = requests.get(URL, {'temperature': temperature, 'humidity': humidity}, stream=True)
        print(result)


async def update_weather(data):
    async with client.get(URL, data=data) as response:
        return await response.json()


if __name__ == '__main__':
    print("Initialisation ...")
    port = '/dev/ttyACM1'

    try:
        ser = serial.Serial(port)
        time.sleep(2)
        read()
    except serial.SerialException:
        print("could not open port :", port)

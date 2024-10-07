import board
import time
import json
import busio
from adafruit_bmp280 import  Adafruit_BMP280_I2C
def sensor():
    i2c = busio.I2C(board.SCL, board.SDA)
    data = Adafruit_BMP280_I2C(i2c,address=0x76)

    while True:
        temperature=data.temperature
        pressure=data.pressure
        print("temperature:",temperature)
        time.sleep(6)
        print("pressure",pressure)

def convert_data_to_json(datas):
    return json.dumps(datas)
       

if __name__ == "__main__":
    sensor()
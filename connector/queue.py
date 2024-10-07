import sys
import os
sys.path.append(os.path.abspath('/home/pi/RABLIVE'))
import pika
from temp_hum_pr import  sensor
from temp_hum_pr import Adafruit_BMP280_I2C
import busio,time
import json
import pandas as pd
import board
class Message:
    def __init__(self,ip_add,user_name=None,password=None,exchange=None):
        self.ip_add="192.168.0.122"
        self.user_name="username"
        self.password="password"
        self.connection =None
        self.channel= None
        self.exchange = exchange
    def amqp_server(self):
        credentials =pika.PlainCredentials(self.user_name,self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip_add,5672,'/',credentials))
        self.channel = self.connection.channel()
    def declare_queue(self):
        self.channel.queue_declare (queue="TEMP_PRESSURE",durable=True)
        print("Queue declared")
    def publish(self,message):
        props = pika.BasicProperties(content_type='data',content_encoding='utf-8',delivery_mode=2)
        self.channel.basic_publish(exchange='',routing_key='TEMP_PRESSURE',body=message,properties=props)
        print("Message published")
    def close_connection(self):
        if self.connection:
            self.connection.close()
def sensor():
        i2c = busio.I2C(board.SCL, board.SDA)
        bmp280 = Adafruit_BMP280_I2C(i2c, address=0x76)
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        data = {
            "temperature": temperature,
            "pressure": pressure
            }
        return json.dumps(data)

if __name__ == "__main__":
    try:
        msg = Message(ip_add="192.168.0.122", user_name="username", password="password")
        msg.amqp_server()
        msg.declare_queue()
        #while True:
        sensor_data = sensor()
        print(f"Sensor Data: {sensor_data}")
        msg.publish(sensor_data)
        time.sleep(1)
            

    except Exception as e:
      print(f"An error occurred: {e}")
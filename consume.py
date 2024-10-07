import pika
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tflite_runtime.interpreter import Interpreter
from connector import queue
model= Interpreter("/home/pi/RABLIVE/regression.tflite")
model.allocate_tensors()
input_details = model.get_input_details()
output_details = model.get_output_details()
def TEMP_PRESSURE(data):
    print("sensor_data")
    print("RECIVED"+str(data))
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='TEMP_PRESSURE',durable=True)
def callback_1(ch,method,properties,body):
    message=body.decode('utf-8')
    data=json.loads(message)
    TEMP_PRESSURE((data))
    input_data=np.array([[data['temperature'],data['pressure']]],dtype=np.float32)
    model.set_tensor(input_details[0]['index'],input_data)
    model.invoke()
    prediction=model.get_tensor(output_details[0]['index'])
    print(f"Model prediction:{prediction}")
    channel.basic_consume('TEMP_PRESSURE',callback_1,auto_ack=True)
print("waiting for messages. TO exit press CTRL+C")
channel.start_consuming()
connection.close()

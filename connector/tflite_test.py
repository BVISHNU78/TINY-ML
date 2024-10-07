import numpy as np
from tflite_runtime.interpreter import Interpreter
model=Interpreter("/home/pi/RABLIVE/regression.tflite")
model.allocate_tensors()
input_details = model.get_input_details()
output_details = model.get_output_details()
print("Input Details:", input_details)
print("Output Details:", output_details)

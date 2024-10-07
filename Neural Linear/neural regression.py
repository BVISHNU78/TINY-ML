import tensorflow as tf 
import numpy as np
import keras
from keras.src import ops
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras import layers
from keras import activations
from sklearn.model_selection import train_test_split 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tf2onnx

data= pd.read_json("D:\coding\Linear Regression\sensor_data.json")
print(data)
print(data.info())
print(data.describe())
print(data.notnull())

x=data[["temperature","pressure"]].values
y=data[["temperature"]].values
scaler = MinMaxScaler()
x_scaled=scaler.fit_transform(x)
y_scaled =scaler.fit_transform(y)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.5,random_state=0)
  
model=tf.keras.Sequential([
    tf.keras.layers.Dense(64,activation='relu',input_shape=(2,)),
    tf.keras.layers.Dense(32,activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(2,activation='linear'),
    ])
early_stopping=keras.callbacks.EarlyStopping(monitor='val_loss',patience=8,verbose=1,mode="auto",restore_best_weights=True)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),loss='mean_squared_error')
model.fit(x_train,y_train,epochs=50,batch_size=32,validation_data=(x_test,y_test),callbacks=[early_stopping])
test_loss =model.evaluate(x_test,y_test)
model.summary()
#model.save("regression.h5")
print(f"Test Loss:{test_loss:4f}")
new_dat= {"temperature": [29.023],"temperature ": [24.045]}
new_data_scaled=pd.DataFrame(new_dat)
predictions =model.predict(new_data_scaled)
predictions=predictions.reshape(1,-1)
predictions_orginal_scale=scaler.inverse_transform(predictions)
print(f"Predictions (Original Scale): {predictions_orginal_scale}")

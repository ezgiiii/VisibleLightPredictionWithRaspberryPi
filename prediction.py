import Adafruit_DHT
import smbus
import time
import datetime
import csv
import sys
from time import sleep
from gpiozero import InputDevice
import board
import busio as io
import pyrebase

import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

config = {
  "apiKey": "gGUUYHeFg8uBBOWMv9jgwOVA61HcDAIVKMp8R1kR",
  "authDomain": "rasp-deneme.firebaseapp.com",
  "databaseURL": "https://rasp-deneme-default-rtdb.firebaseio.com",
  "storageBucket": "rasp-deneme.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()


DHT_SENSOR= Adafruit_DHT.DHT11
DHT_PIN = 17
no_rain = InputDevice(23)


bus = smbus.SMBus(1)
 
bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

dataset=pd.read_csv('/home/pi/iot proje/model/duzenlikisa.csv')

features=["Temperature","Humidity"]

x=dataset[features]
y=dataset.Lux

x_scaled=preprocessing.scale(x)
poly=PolynomialFeatures(7)

x_final=poly.fit_transform(x_scaled)
x_train, x_test, y_train, y_test = train_test_split(x_final, y, test_size=0.10, random_state=42)

regr=linear_model.Ridge(alpha=5)
regr.fit(x_train,y_train)



while True:
    
    data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
    data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
     
    # Convert the data
    ch0 = data[1] * 256 + data[0]
    ch1 = data1[1] * 256 + data1[0]
    visibleSpectrum= ch0 - ch1
        
    if not no_rain.is_active:
        rain=1
        print("fail")
    else:
        rain=0
        
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    
    sleep(5)
    
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature,humidity))
    else:
        print("DHT11 fails")
        
    observation=[[temperature,humidity]]
    observation_scaled=preprocessing.scale(observation)
    observation_final=poly.fit_transform(observation_scaled)

    y_pred = regr.predict(observation_final)
    
#     number_string= "{:.2f}".format(y_pred)
    number_float=float(y_pred)
    
    data = {
        "float": number_float,
        
      }
    db.child("data").child("1-set").set(data)
    db.child("data").child("2-push").push(data)
    
    print("Send Data to Firebase Using Raspberry Pi")
    print(y_pred)
       
    sleep(5)
    
    

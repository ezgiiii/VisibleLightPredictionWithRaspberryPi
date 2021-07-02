import Adafruit_DHT
import smbus
import time
import datetime
import csv
import sys
from time import sleep
from gpiozero import InputDevice

csvFile="trainingData.csv"

DHT_SENSOR= Adafruit_DHT.DHT11
DHT_PIN = 17
no_rain = InputDevice(23)


bus = smbus.SMBus(1)
 
bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)



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
        
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature,humidity))
    else:
        print("DHT11 fails")
            
        
    time = datetime.datetime.now().__str__()
    time=time[:-7]
    dateAndTime=time.split(" ")
        
    trainingData=[dateAndTime[0],dateAndTime[1],temperature,humidity,visibleSpectrum,rain]
        
    with open(csvFile, "a") as output:
        writer = csv.writer(output,delimiter=",",lineterminator='\n')
        writer.writerow(trainingData)
        
    print("sensor data logging...")
    print(rain)
    print(visibleSpectrum)
    
    sleep(60)

    
    
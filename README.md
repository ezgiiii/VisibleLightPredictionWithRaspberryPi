# VisibleLightPredictionWithRaspberryPi
Prediction using Linear Regression

This project gets the temperature, humidity, precipitation, and light intensity data of Adana and predicts the visible light according to temperature and humidity values that are get from raspberry pi live. 

System Design and Features: 
-DHT11 Temperature and Humidity Sensor
-Raindrop Sensor
-TSL2561 Luminosity Sensor
-Raspberry Pi 3 Model B+ 
-Breadboard
-Jumpers

All the sensors are connected to Raspberry Pi. Live temperature, humidity, precipitation, and light intensity data are logged in Raspberry Pi to built a dataset. Then, using this dataset, train and test samples are generated. By appling Linear Regression the predicted data is sent to Firebase. Also, I displayed the predicted data on a WinForms App. 

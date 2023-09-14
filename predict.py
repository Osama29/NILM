import time
import serial
import pandas as pd
import numpy as np
import joblib
from collections import deque
import os

# Load the pre-trained KNN model
model_filename = 'knn_model.joblib'
if not os.path.exists(model_filename):
    raise Exception("The pre-trained model file 'knn_model.joblib' does not exist. Please run the training code first.")

knn_classifier = joblib.load(model_filename)

# Initialize variables and data structures
sensor_port = '/dev/ttyUSB0'  # Replace with the actual port of your PZEM-004T sensor
baud_rate = 9600  # Adjust the baud rate if needed
data_buffer = deque(maxlen=100)  # Store the last 100 rows of measurements

# Open a connection to the sensor
ser = serial.Serial(sensor_port, baud_rate)

try:
    while True:
        # Read a line of data from the sensor
        data = ser.readline().decode('utf-8').strip()
        # Parse and store the data in a DataFrame
        if data:
            measurements = [float(val) for val in data.split(',')]
            if len(measurements) == 7:  # Assuming there are 7 measurements
                data_buffer.append(measurements)
        
        # Check if we have collected 100 measurements
        if len(data_buffer) == 100:
            # Convert the data buffer into a DataFrame
            df = pd.DataFrame(data_buffer, columns=['voltage', 'current', 'power', 'energy', 'frequency', 'power_factor', 'overload'])
            
            # Select the features for prediction
            X = df[['voltage', 'current', 'energy', 'std_voltage', 'std_current', 'std_power', 'power_factor']]
            
            # Make a prediction using the pre-trained model
            y_pred = knn_classifier.predict(X)
            
            # Create a mapping of STATE numbers to appliance names (customize based on your dataset)
            state_to_appliance = {
                0: "Everything Off",
                1: "Air Conditioner",
                2: "Air Conditioner & Washing Machine",
                3: "Air Conditioner & Washing Machine & Light",
                4: "Air Conditioner & Light",
                5: "Light"
            }
            
            # Count the predictions and find the most frequent one
            prediction_counts = pd.Series(y_pred).value_counts()
            
            # Find the most frequent prediction
            most_frequent_prediction = prediction_counts.idxmax()
            
            # Map the most frequent prediction to an appliance name
            most_frequent_appliance = state_to_appliance[most_frequent_prediction]
            
            # Create a payload or take any action based on the prediction
            dict_payload = {
                "prediction": most_frequent_appliance,
                "measurements": df.values.tolist()
            }
            
            # Print or send the payload to your desired destination
            print(dict_payload)
            
            # Clear the data buffer to start collecting a new set of measurements
            data_buffer.clear()
        
        # Add a delay between readings to control the collection rate
        time.sleep(1)

except KeyboardInterrupt:
    ser.close()
    print("Script terminated by user.")

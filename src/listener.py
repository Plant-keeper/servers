"""
Project Name: PlantKeeper

@created 03.09.2024
@file listener.py
@version 1.0.0
@description 
    Flask-based server to receive sensor data from the Arduino devices 
    and forward it to the backend server.
    
@authors
  - Rafael Dousse
  - Eva Ray
  - Quentin Surdez
  - Rachel Tranchida

@dependencies
  - Flask 2.x
  - Requests 2.x

"""
from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

# Function to send data to the backend asynchronously
def send_to_backend(data):
    backend_url = "http://backend-phi-drab-76.vercel.app/api/v1/sensors/" 
    backend_url += str(data['id'])
    
    # Send data to backend and print backend response
    response = requests.patch(backend_url, json=data, verify=False)

    if response.status_code == 200:
        print("Data forwarded to backend successfully:", response.json())
    else:
        print("Failed to forward data to backend:", response.status_code)

# Route for receiving POST requests
@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.json
    print("Data received:", data)

    # Check if data is valid
    if not data:
        print("Received an invalid or empty JSON request")
        return jsonify({"error": "Invalid JSON data"}), 400

    # Check if the ID is present
    if 'id' in data:
        print("Data received from sensor id:", data['id'])
    else:
        return jsonify({"error": "No id in data"}), 400

    # Immediately send 200 status back to the Arduino
    response_arduino = jsonify({"message": "Data successfully received"}), 200

    # Create a new thread to handle sending data to the backend
    thread = threading.Thread(target=send_to_backend, args=(data,))
    thread.start()

    # Return response to Arduino without waiting for backend request
    return response_arduino

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

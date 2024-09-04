from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
    # This tells the Arduino that the data was received successfully
    response_arduino = jsonify({"message": "Data successfully received"}), 200

    
    backend_url = "http://backend-phi-drab-76.vercel.app/api/v1/sensors/" 
    backend_url += str(data['id'])
    
    # Send data to backend and print backend response
    response = requests.patch(backend_url, json=data, verify=False)

    if response.status_code == 200:
        print("Data forwarded to backend successfully:", response.json())
    else:
        print("Failed to forward data to backend:", response.status_code)

    # Return the response to Arduino 
    return response_arduino

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Route pour recevoir les requêtes POST sur le port 80
@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.json
    print("Data received:", data)
    if not data:
        print("Received an invalid or empty JSON request")
        return jsonify({"error": "Invalid JSON data"}), 400
    
    print("Data received:", data)
    if 'id' in data:
        print("Data received from sensor id:", data['id'])
    else:
        return jsonify({"error": "No id in data"}), 400

    # Transmit the data to the backend via HTTPS
    backend_url = "http://backend-phi-drab-76.vercel.app/api/v1/sensors/" 
    backend_url += str(data['id'])
    response = requests.patch(backend_url, json=data, verify=False)

    if response.status_code == 200:
        print(response.json())
        return jsonify({"message": "Data successfully forwarded to backend"}), 200
    else:
        return jsonify({"error": "Failed to forward data"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

from flask import Flask, request, jsonify, make_response
import requests

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def get_health():
  return make_response(jsonify({'message': 'Service is running'}), 200)

@app.route('/telemetry/temperature/<int:id>', methods=['GET'])
def get_sensor_value(id):
  try:
    sensor_value = float(requests.get('http://temperature-api:8081/temperature?sensor_id=' + str(id)).text.strip())
    if sensor_value:
      requests.patch('http://sensor-service:8082/sensors/' + str(id) + '/value', json={"value": sensor_value})
      return make_response(jsonify({'temperature': sensor_value}), 200)
    return make_response(jsonify({'message': 'sensor not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating sensor'}), 500)

@app.route('/telemetry/temperature/<string:location>', methods=['GET'])
def get_location_value(location):
  try:
    sensor_value = float(requests.get('http://temperature-api:8081/temperature?location=' + str(location)).text.strip())
    if sensor_value:
        return make_response(jsonify({'temperature': sensor_value}), 200)
    return make_response(jsonify({'message': 'location not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting location'}), 500)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8083)

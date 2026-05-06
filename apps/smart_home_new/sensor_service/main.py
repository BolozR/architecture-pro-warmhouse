from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@smarthome-postgres:5432/smarthome'
db = SQLAlchemy(app)

class Sensors(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='inactive')
    last_updated = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def json(self):
        return {'id': self.id,'name': self.name, 'type': self.type, 'location': self.location, 'value': self.value, 'unit': self.unit, 'status': self.status}

with app.app_context():
  db.create_all()

@app.route('/health', methods=['GET'])
def get_health():
  return make_response(jsonify({'message': 'Service is running'}), 200)

@app.route('/sensors', methods=['GET'])
def get_all_sensors():
  sensors = Sensors.query.all()
  return make_response(jsonify([sensor.json() for sensor in sensors]), 200)

@app.route('/sensors/<int:id>', methods=['GET'])
def get_sensor_by_id(id):
  try:
    sensor = Sensors.query.filter_by(id=id).first()
    if sensor:
      return make_response(jsonify({'sensor': sensor.json()}), 200)
    return make_response(jsonify({'message': 'sensor not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting sensor'}), 500)

@app.route('/sensors', methods=['POST'])
def create_sensor():
  try:
    data = request.get_json()
    new_sensor = Sensors(name=data['name'], type=data['type'], location=data['location'], unit=data['unit'], status=data['status'])
    db.session.add(new_sensor)
    db.session.commit()
    return make_response(jsonify({'message': 'sensor created'}), 201)
  except e:
    return make_response(jsonify({'message': 'error creating sensor'}), 500)

@app.route('/sensors/<int:id>', methods=['PUT'])
def update_sensor(id):
  try:
    sensor = Sensors.query.filter_by(id=id).first()
    if sensor:
      data = request.get_json()
      sensor.name = data['name']
      sensor.type = data['type']
      sensor.location = data['location']
      sensor.unit = data['unit']
      sensor.status = data['status']
      db.session.commit()
      return make_response(jsonify({'message': 'sensor updated'}), 200)
    return make_response(jsonify({'message': 'sensor not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating sensor'}), 500)

@app.route('/sensors/<int:id>', methods=['DELETE'])
def delete_sensor(id):
  try:
    sensor = Sensors.query.filter_by(id=id).first()
    if sensor:
      db.session.delete(sensor)
      db.session.commit()
      return make_response(jsonify({'message': 'sensor deleted'}), 200)
    return make_response(jsonify({'message': 'sensor not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting sensor'}), 500)

@app.route('/sensors/<int:id>/value', methods=['PATCH'])
def patch_sensor_value(id):
  try:
    sensor = Sensors.query.filter_by(id=id).first()
    if sensor:
      data = request.get_json()
      sensor.value = data['value']
      db.session.commit()
      return make_response(jsonify({'message': 'sensor updated'}), 200)
    return make_response(jsonify({'message': 'sensor not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating sensor'}), 500)

@app.route('/sensors/temperature/<string:location>', methods=['GET'])
def get_temperature_by_location(location):
  try:
    sensor = Sensors.query.filter_by(location=location).first()
    if sensor and sensor.type == 'temperature':
      return make_response(jsonify({
		"location":    sensor.json().get('location'),
		"value":       sensor.json().get('value'),
		"unit":        sensor.json().get('unit'),
		"status":      sensor.json().get('status'),
		"timestamp":   sensor.json().get('timestamp'),
		"description": sensor.json().get('description'),
	}), 200)
    return make_response(jsonify({'message': 'sensor not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting sensor'}), 500)


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8082)

from flask import Flask, render_template, Response, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import models
import os
import json
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x1do\xae\xca^\x01U\r\xdfP>tt\xff$r\x1f\xc1\xe3<\x9e\xd5ou'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sensorsDB.sqlite3')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)


@app.route('/')
@app.route('/index')
def index():
    # TODO change sensortype_id on sensortype_name
    co2_level = models.SensorData.query.filter_by(sensor_type_id=1)[-1]
    temperature = models.SensorData.query.filter_by(sensor_type_id=2)[-1]
    humidity = models.SensorData.query.filter_by(sensor_type_id=3)[-1]

    return render_template('index.html', co2_level=co2_level, temperature=temperature, humidity=humidity)


@app.route('/api')
@app.route('/api/sensor')
def sensor():
    sensors = models.Sensor.query.all()
    sensors_list = []
    for sensor in sensors:
        sensor_dict = {'id': sensor.id, 'name': sensor.name}
        sensors_list.append(sensor_dict)
    return Response(json.dumps(sensors_list),  mimetype='application/json')


@app.route('/api/sensortype')
def sensortype():
    sensor_types = models.SensorType.query.all()
    sensor_types_list = []
    print sensor_types
    for sensor_type in sensor_types:
        sensor_type_dict = {'id': sensor_type.id, 'type': sensor_type.type, 'sensor_id': sensor_type.sensor_id}
        sensor_types_list.append(sensor_type_dict)
    return Response(json.dumps(sensor_types_list),  mimetype='application/json')


@app.route('/api/sensordata', methods=['GET', 'POST'])
def sensordata():
    if request.method == 'GET':
        sensor_data = models.SensorData.query.all()
        sensor_data_list = []
        for data in sensor_data:
            data_dict = {'id': data.id,
                         'value': data.value,
                         'time': datetime.datetime.strftime(data.time, "%d-%m-%Y %H:%M:%S"),
                         'sensor_type_id': data.sensortype_id}
            sensor_data_list.append(data_dict)
        return Response(json.dumps(sensor_data_list),  mimetype='application/json')
    if request.method == 'POST':
        if request.args:
            sensor_type_id = int(request.args['sensor_type_id'])
            value = float(request.args['value'])
            time = datetime.datetime.utcnow()
            sensor_data = models.SensorData(value=value, time=time, sensor_type_id=sensor_type_id)
            db.session.add(sensor_data)
            db.session.commit()
        return Response(json.dumps([]), mimetype='application/json')
    # if request.method == 'POST':
    #     return Response(json.dumps({"im back": ""}),  mimetype='application/json')


if __name__ == "__main__":
    app.run()

from climatemgmt import db
from datetime import datetime


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    type = db.relationship('SensorType', backref='sensor', lazy='dynamic')

    def __repr__(self):
        return "<Sensor '{}':{}>".format(self.id, self.name)


class SensorType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

    data = db.relationship('SensorData', backref='sensor_type', lazy='dynamic')

    def __repr__(self):
        return "<SensorType '{}':{},  sensor_id:{}>".format(self.id, self.type, self.sensor_id)


class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    sensor_type_id = db.Column(db.Integer, db.ForeignKey('sensor_type.id'))

    def __repr__(self):
        return "<SensorData {}:{} - {}, sensor_type_id: {}>".format(self.id, self.value, self.time, self.sensor_type_id)

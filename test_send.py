import requests

r = requests.post('http://127.0.0.1:5000/api/sensordata?sensor_type_id=3&value=700')
print r.status_code
print r.text
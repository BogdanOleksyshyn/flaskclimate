import requests

r = requests.post('http://127.0.0.1:5000/api/sensordata?sensortype_id=2&value=31.5')
print r.status_code
print r.text
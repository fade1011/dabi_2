import os
from google.cloud import pubsub_v1

credentials_path = 'KEYS/weather_dabi.privateKey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/dscb420-rira1011/topics/weather_dabi'


data = 'New data is ready!. High temperature'
data = data.encode('utf-8')
attributes = {
    'sensorName': 'Berlin',
    'temperature': '75.0',
    'humidity': '60'
}

future = publisher.publish(topic_path, data, **attributes)
print(f'published message id {future.result()}')

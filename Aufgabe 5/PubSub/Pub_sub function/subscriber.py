import os
import json
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = 'KEYS/weather_dabi.privateKey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


timeout = 20.0 

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/dscb420-rira1011/subscriptions/weather_dabi-sub'


def callback(message):
    print("Received message:")
    data = json.loads(message.data.decode("utf-8"))
    
    print("Weather Forecast for the next days:")
    print("-------------------------------------------------------------")
    print("| Date       | Max Temp | Min Temp | Showers | Snowfall |")
    print("-------------------------------------------------------------")
    for i in range(len(data["time"])):
        date = data["time"][i]
        max_temp = data["temperature_2m_max"][i]
        min_temp = data["temperature_2m_min"][i]
        showers = data["showers_sum"][i]
        snowfall = data["snowfall_sum"][i]
        print(f"| {date} | {max_temp}    | {min_temp}    | {showers}    | {snowfall}    |")
    print("-------------------------------------------------------------")
    
    message.ack()           


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')


with subscriber:                                                # wrap subscriber in a 'with' block to automatically call close() when done
    try:
        streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()                          # going without a timeout will wait & block indefinitely
    except TimeoutError:
        streaming_pull_future.cancel()                          # trigger the shutdown
        streaming_pull_future.result() 

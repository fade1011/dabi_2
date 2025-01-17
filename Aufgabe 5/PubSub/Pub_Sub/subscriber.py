import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = '/Users/rafaelriesle/Downloads/Pub:Sub/KEYS/Serivce-Account/weather_dabi.privateKey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


timeout = 5.0 

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/dscb420-rira1011/subscriptions/weather_dabi-sub'


def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')

    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")

    message.ack()           


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')


with subscriber:                                                # wrap subscriber in a 'with' block to automatically call close() when done
    try:
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()                          # going without a timeout will wait & block indefinitely
    except TimeoutError:
        streaming_pull_future.cancel()                          # trigger the shutdown
        streaming_pull_future.result() 

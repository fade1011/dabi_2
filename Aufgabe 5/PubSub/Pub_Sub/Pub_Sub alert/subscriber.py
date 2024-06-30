import os
import json
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

credentials_path = 'KEYS/weather_dabi.privateKey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


timeout = 20.0 

# Initialize the Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/dscb420-rira1011/subscriptions/weather_dabi-sub'


def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()

def main():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

if __name__ == "__main__":
    main()
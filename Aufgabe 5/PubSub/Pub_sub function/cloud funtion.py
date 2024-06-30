import requests
import pandas as pd
from google.cloud import storage, pubsub_v1
from datetime import datetime
import json

def fetch_weather_data(request):
    url = "https://api.open-meteo.com/v1/dwd-icon"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "daily": ["temperature_2m_max", "temperature_2m_min","showers_sum", "snowfall_sum"],
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        daily = data['daily']
        json_data = json.dumps(daily)
        
        # Publish JSON data to Pub/Sub
        topic_path = 'projects/dscb420-rira1011/topics/weather_dabi'
        publisher = pubsub_v1.PublisherClient()
        publish_future = publisher.publish(topic_path, data=json_data.encode('utf-8'))
        publish_future.result()  # Verify that the publish succeeded
        return "Weather data published to Pub/Sub successfully."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}", 500
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}", 500
    except Exception as err:
        return f"An error occurred: {err}", 500

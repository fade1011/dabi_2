import requests
from google.cloud import pubsub_v1
import os


credentials_path = 'KEYS/weather_dabi.privateKey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Initialize the Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/dscb420-rira1011/topics/weather_dabi'



# API Anfrage Parameter
url = "https://api.open-meteo.com/v1/dwd-icon"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "daily": ["temperature_2m_max", "temperature_2m_min", "showers_sum", "snowfall_sum"],
    "timezone": "auto"
}

# Definierte Schwellenwerte
thresholds = {
    "temperature_2m_max": 20,  
    "temperature_2m_min": 10,  
    "showers_sum": 10,  
    "snowfall_sum": 5  
}

def check_thresholds(daily_data, thresholds):
    alerts = []
    for key, value in thresholds.items():
        if key in daily_data:
            for i, val in enumerate(daily_data[key]):
                if val > value:
                    date = daily_data["time"][i]
                    alerts.append(f"Warning: {key} exceeds {value} on {date}")
    return alerts

def main():
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        daily_data = data['daily']

        # Check if any value exceeds the thresholds
        alerts = check_thresholds(daily_data, thresholds)

        if alerts:
            # If any alert is triggered, send a message to Pub/Sub
            alert_message = "\n".join(alerts)
            publish_future = publisher.publish(topic_path, alert_message.encode('utf-8'))
            publish_future.result()  # Verify that the publish succeeded
            print("Alert published to Pub/Sub successfully.")
        else:
            print("No thresholds exceeded.")

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")


if __name__ == "__main__":
    main()

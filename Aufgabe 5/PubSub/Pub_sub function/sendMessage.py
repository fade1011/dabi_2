import requests
import json

def send_message_to_google_cloud():
    url = "https://us-central1-dscb420-rira1011.cloudfunctions.net/weather_data_reading"

    r = requests.post(url)
    print(f'r = {r}')

if __name__ == '__main__':
    send_message_to_google_cloud()

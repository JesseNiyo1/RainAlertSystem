import requests
from twilio.rest import Client
import os
API_KEY = os.environ.get("API_KEY")
MY_LATITUDE = os.environ.get("MY_LATITUDE")
MY_LONGITUDE = os.environ.get("MY_LONGITUDE")
MY_ACCOUNT_SID = os.environ.get("MY_ACCOUNT_SID")
MY_AUTH_TOKEN = os.environ.get("MY_AUTH_TOKEN")
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
MY_TRIAL_PHONE_NUMBER = os.environ.get("MY_TRIAL_PHONE_NUMBER")
# Step 2: Send an SMS message using Twilio API if it will
def send_text_message(description):

    client = Client(MY_ACCOUNT_SID, MY_AUTH_TOKEN)

    message = client.messages.create(
        body= f"Bring an umbrella today! {description}",
        from_=MY_TRIAL_PHONE_NUMBER,
        to=MY_PHONE_NUMBER,
    )

    print(message.status)

# Step 1: Use OpenWeather API to see if it's going to rain in the next 12 hours

parameters = {
    "lat": float(MY_LATITUDE),
    "lon": float(MY_LONGITUDE),
    "appid": API_KEY,
    "cnt": 4 # 12-hour window
}
response = requests.get(url= "https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()

data = response.json()["list"]

is_going_to_rain = False
desc = None
for entry in data:
    list = entry["weather"]
    for dict in list:
        id, description = dict["id"], dict["description"]
        if id < 700:
            is_going_to_rain = True
            desc = description
            break

if is_going_to_rain:
    send_text_message(desc)




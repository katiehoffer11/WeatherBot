# Dependencies
import tweepy
import time
import json
import os
import random
import requests as req
import datetime
from config import consumer_key, consumer_secret, access_token, access_token_secret, weather_api_key


# Twitter API Keys
consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_token_secret = access_token_secret

# Create a function that gets the weather in London and Tweets it
def WeatherTweet():

    # Construct a Query URL for the OpenWeatherMap
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    city = 'Washington, D.C.'
    units = 'imperial'
    query_url = (f'{url}appid={weather_api_key}&q={city}&units={units}')

    # Perform the API call to get the weather
    weather_response = req.get(query_url)
    weather_json = weather_response.json()
    print(weather_json)

    # Twitter credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Tweet the weather
    api.update_status(
        "Khoffer - Weather in DC " +\
        (datetime.datetime.now().strftime("%I:%M %p") + " " +\
         str(weather_json["main"]["temp"])+"F"))

    # Print success message
    print("Tweeted successfully!")

# Test out the function
# WeatherTweet()

    # Tweet out the weather every one minute
while(True):
    WeatherTweet()
    time.sleep(60)
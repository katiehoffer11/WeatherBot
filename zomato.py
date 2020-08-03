"""
Zomato API
Version: 1.0

By: Todd Karr,
    Katie Hoffer,
    Heather Moore,
    Tom Stark

This script retrieves data from the Zomato API
and outputs it to our MongoDB
"""

import codecs
import os
import json
import logging
import requests
import pymongo

LOGPATH = os.path.join('foodie_app.log')
logging.basicConfig(format='%(asctime)s : %(lineno)d : %(levelname)s : %(message)s',
                    level=logging.DEBUG,
                    filename=LOGPATH)

CONN = "mongodb://ec2-18-224-51-189.us-east-2.compute.amazonaws.com:27017"
CLIENT = pymongo.MongoClient(CONN)
DB = CLIENT["food_fighters"]
ZOMATO = DB["zomato"]

def query_zomato(lat='38.89076',
                 lon='-77.084755',
                 user_key="key"):
    try:
        headers = {'Accept': 'application/json', 'user-key': user_key}
        #Get /cities
        city_url = "https://developers.zomato.com/api/v2.1/cities?"
        response = requests.get(f'{city_url}lat={lat}&lon={lon}', headers=headers)
        results = response.json()
        city_id = results["location_suggestions"][0]["id"]

        #GET /cuisines
        cuisines_url = "https://developers.zomato.com/api/v2.1/cuisines?"
        response = requests.get(f'{cuisines_url}city_id={city_id}', headers=headers)
        cuisines_results = response.json()
        cuisines = cuisines_results['cuisines']

        #save list of cuisines to loop through in search query
        cuisine_ids = []

        for cuisine in cuisines:
            cuisine_id = cuisine['cuisine']["cuisine_id"]
            cuisine_ids.append(cuisine_id)

        #Get /search
        restaurants = []
        for cuisine_id in cuisine_ids:
            search_url = "https://developers.zomato.com/api/v2.1/search?"
            search_response = requests.get(f'{search_url}lat={lat}&lon={lon}&cuisines={cuisine_id}', headers=headers)
            search_results = search_response.json()
            restaurants.append(search_results)

        for restaurant in restaurants:
            search_results = restaurant["restaurants"]

            ZOMATO.insert_one(json.dumps(search_results))
            #logging.info("MongoDB Updated: Database - {}, Collection - {}".format("food_fighters", ZOMATO))
            print(search_results)
    except Exception as error:
        logging.error(error)
        raise

query_zomato(lat='38.89076',
             lon='-77.084755',
             user_key=codecs.decode('p0np6orr3n073rr23nq460472qo43qn6', 'rot-13'))

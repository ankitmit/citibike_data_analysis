import sys
import numpy as np
import scipy.stats as ss
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from collections import OrderedDict

intent_dict = {"travel" : [0] * 24, "entertainment" : [0] * 24, "business" : [0] * 24, "health_care" : [0] * 24, "shopping" : [0] * 24, "education" : [0] * 24, "restaurant" : [0] * 24, "luxury" : [0] * 24}


def getTopServicesInVicinity(lat, lon):
    relevant_types = ["airport", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "book_store",
                      "bowling_alley", "bus_station", "cafe", "car_rental", "city_hall", "clothing_store",
                      "convenience_store", "dentist", "department_store", "doctor", "electronics_store", "finance",
                      "food", "grocery_or_supermarket", "gym", "hair_care", "hospital", "library", "liquor_store",
                      "local_government_office", "meal_delivery", "movie_theater", "museum", "night_club", "park",
                      "parking", "pharmacy", "post_office", "restaurant", "school", "shopping_mall", "spa", "stadium",
                      "subway_station", "taxi_stand", "train_station", "transit_station", "university"]
    intent_dict = {"airport": "travel", "bus_station": "travel", "train_station": "travel", "car_rental": "travel",
                   "subway_station": "travel", "transit_station": "travel", "taxi_stand": "travel", "parking": "travel",
                   "aquarium": "entertainment", "art_gallery": "entertainment", "bowling_alley": "entertainment",
                   "park": "entertainment", "stadium": "entertainment", "museum": "entertainment",
                   "movie_theater": "entertainment", "atm": "business", "bank": "business", "post_office": "business",
                   "meal_delivery": "business", "city_hall": "business", "local_government_office": "business",
                   "finance": "business", "pharmacy": "health_care", "hospital": "health_care",
                   "dentist": "health_care", "doctor": "health_care", "shopping_mall": "shopping",
                   "clothing_store": "shopping", "convenience_store": "shopping", "grocery_or_supermarket": "shopping",
                   "electronics_store": "shopping", "department_store": "shopping", "book_store": "shopping",
                   "liquor_store": "shopping", "university": "education", "school": "education", "library": "education",
                   "bakery": "restaurant", "bar": "restaurant", "restaurant": "restaurant", "food": "restaurant",
                   "cafe": "restaurant", "hair_care": "luxury", "gym": "luxury", "night_club": "luxury",
                   "spa": "luxury"}
    types_filter = '|'.join(relevant_types)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    url += lat + ',' + lon + '&rankby=prominence&types=' + types_filter+ '&radius=200&key=' + 'AIzaSyAmdYjmCcgPp3MSJOu27xURQsFhB37Nhmg'

    myResponse = requests.get(url)
    if myResponse.ok:
        json_obj_list = json.loads(myResponse.content)
        result = []
        cat_freq = {}
        for res in json_obj_list['results']:
            for type in  res['types']:
                if type  in relevant_types:
                    if type in cat_freq.keys():
                        cat_freq[type] += 1
                    else:
                        cat_freq[type] = 1

        d_sorted_by_value = OrderedDict(sorted(cat_freq.items(), key=lambda x: x[1]))
        keys = d_sorted_by_value.keys()
        rev_keys = keys[::-1]
        if len(rev_keys) > 5 :
            rev_keys = rev_keys[:5]
        result = []
        for k in rev_keys:
            key = str(k)
            if intent_dict[key] is not None and intent_dict[key]  not in result:
                result.append(intent_dict[key])
        return result

filename = '201609-citibike-tripdata.csv'
#Create a dataframe from CSV file using pandas
df = pd.read_csv(filename, low_memory = False)
count = 0
for index, row in df.iterrows():
    intents = getTopServicesInVicinity(str(row['end station latitude']), str(row['end station longitude']))
    time = int((row['stoptime'].split(' '))[1].split(':')[0])
    for intent in intents:
        intent_dict[intent][time] += 1
    count = count + 1
    if count == 100:
        break



print intent_dict
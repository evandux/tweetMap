"""
This script allows the user to use a keyword to filter and obtain real-time tweets
that contain that keyword (can be as part of the tweet or a hashtag) and converts 
these tweets to a point shapefile. This script only searches for tweets that contain
the user entered keyword and have location coordinates attached to them.

TweetMap v6.0
Author: Evan Dux
As of November 29th, 2018
Edited: November 30th, 2018
Edited: December 1st, 2018
Edited: December 3rd, 2018

"""
# Import modules
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import arcpy
from arcpy import env
import os
from os import path

# Necessary authentication keys from Twitter
consumer_key ="4JwxciB9kDz7MOldVl6GjRsrc"
consumer_secret = "pNpM2p29AQikAoF10tfB5l9khH67CYF52gs4VH8CNtpIgRQAzA"
access_token = "1060765563784323072-2qcyK8PgnZ2bkpjTmNiwD6vMbc3c1K"
access_secret = "hdsGEZdW7fgzQUMq4KsxYalpKQ8qs16aJKJkyuQmHXkqJ"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Local variables based on user input and check to see if given directories exist
output = input("Enter a folder directory to save your tweets into: ")
if os.path.isdir(output):
    pass
else:
    print("That output directory does not exist")

tweet_shape = input("Enter a directory to save your shapefile into: ")
if os.path.isdir(tweet_shape):
    pass
else:
    print("That shapefile directory does not exist.")
    
tweet_shape = tweet_shape + "\\" 
tweet_file_name = input("What do you want to call your json file that holds the tweets? ")
output = output + "\\" + tweet_file_name + ".json"
file_name = input("What would you like to call your output shapefile? ")

# Allow overwrite for shapefiles and set workspace
arcpy.env.overwriteOutput = True


search_key = input("Enter a keyword to filter tweets: ") # Keyword for filtering tweets
how_many = int(input("How many tweets would you like? ")) # User specified number of tweets to collect


print("Please wait while your tweets are collected, this can take some time...")

# Class to stream tweets and write them as JSON filetype to user specified directory
class MyListener(StreamListener):

    def __init__(self, num_tweets_to_grab, output_file):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.output_file = output


    def on_data(self,data):
        json_data = json.loads(data)
        coords = json_data.get("coordinates")
        try:
            if coords is not None:                
                print(data)
                with open(self.output_file, "a") as f:
                    f.write(data)
                    self.counter += 1
                    print (self.counter)
                    return True
            if self.counter == self.num_tweets_to_grab:
                print("Tweets collected! Creating points, please wait... ")
                return False
        except KeyError:
            pass
            return True    
        except BaseException as e:
            print("Error on_data: {}".format(e))
        return True
    
    def on_error(self, status):
        print(status)
        return True
    
# Initiate stream of tweets using input as search parameters
twitter_stream = Stream(auth, MyListener(num_tweets_to_grab=how_many, output_file=output))
twitter_stream.filter(track=[search_key])

# Convert and save JSON file with tweets to a geoJSON format to be converted into a shapefile
with open(output, "r",newline="\r\n") as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet["coordinates"]:
            geo_json_feature = {
                "type":"Feature",
                "geometry": tweet["coordinates"],
                "properties": {
                    "text": tweet["text"],
                    "created_at": tweet["created_at"]
                }
            }
            geo_data["features"].append(geo_json_feature)

with open(output,"w") as fout:
    fout.write(json.dumps(geo_data, indent=4))

arcpy.JSONToFeatures_conversion(output, os.path.join(tweet_shape, file_name)) # Converts geoJSON to a point shapefile
print("All done, your file can be found at {}\{}.shp".format(tweet_shape, file_name))

# File for input Q:\evandux\GIS329_Programming\FinalProject\outputs
# File to use for shapefile output Q:\evandux\GIS329_Programming\FinalProject\outputs\shapefile


Tweet Map Readme
GIS 329 Final Project
Author: Evan Dux

This script allows users to filter a global "real-time" stream of tweets using a keyword of their choosing, it saves these tweets as a JSON format to a user specified directory (essentially a place to store the tweets so that they can be converted to points later). The script then takes these JSON tweet files, converts them into geoJSON format, and ultimately uses the JSONtofeatures arcpy tool to convert each tweet into a point feature to be used in mapping. The user is also able to dictate how many tweets they would like returned for their keyword.

This script will prompt the user for 6 specific inputs. In order, these inputs are:

1. Directory to save the initial JSON file to, this file is used later in the script. 

2. Directory or workspace or geodatabase to save the final tweet points shapefile to.
 
3. Your desired name of the JSON file that will contain the tweets you gather (eg. jsontweets)*
 * do not add a .json extension to your filename, the script will do this automatically.

4. A keyword to filter tweets. Only tweets that contain this keyword, whether it be a hashtag or part of the tweet, will be returned. (eg. snow)

5. How many tweets would you like to collect? (eg. 5, 100, 500, etc)

6. What you would like to name your final shapefile containing the tweets as points (eg. tweets)**
 **do not include a .shp extension in your filename, the script automatically adds this.

If successful, the script will print a confirmation message as well as the filepath to your new shapefile. 

 
Third Party Tools

-tweepy - http://www.tweepy.org/ 

-arcpy - http://pro.arcgis.com/en/pro-app/arcpy/get-started/what-is-arcpy-.html

-json - https://www.json.org/

Re: Test data
Test data for this script is inherently hard to provide due to the fact that data for this script comes in the form of tweets, which cannot be provided until they are collected when the script is run. I would recommend using a fairly common keyword such as "morning", "coffee", etc. and a tweet number of 1 to test the script quickly.

Final Thoughts
Given more time, I would have tried to break the script down into individual functions, however I think it does flow rather smoothly as one file. I also feel that I could have made this script more "Pythonic" by following guidelines in PEP8, unfortunately the time was just not there for that level of polish.


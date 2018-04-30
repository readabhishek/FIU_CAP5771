import json
import sys

def getAuthenticationInfo():

    with open('Authentication.json') as json_data:    # Open the JSON file and get the authentication info
        jdata = json.load(json_data)
        for row in jdata:
            tw_access_token = jdata[row]["tw_access_token"]
            tw_access_token_secret = jdata[row]["tw_access_token_secret"]
            tw_consumer_key = jdata[row]["tw_consumer_key"]
            tw_consumer_secret = jdata[row]["tw_consumer_secret"]

    return tw_access_token, tw_access_token_secret, tw_consumer_key, tw_consumer_secret


getAuthenticationInfo()
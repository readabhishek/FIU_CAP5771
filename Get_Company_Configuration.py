import json
import sys


def getCompanyDetailsList():
    companyList = []; count=0
    companyList.append("Dummy Data to create sequence from 1")
    with open('Keywords.json') as json_data:
        jdata = json.load(json_data)
        for row in jdata:
            # print(jdata[row]["name"])
            companyDetails = {}
            companyDetails["sequence"] = jdata[row]["sequence"]
            companyDetails["name"] = jdata[row]["name"]
            companyDetails["shortNm"] = jdata[row]["shortNm"]
            companyDetails["app"] = jdata[row]["app"]
            companyDetails["keys"] = jdata[row]["keys"]
            companyDetails["sentiment_title"] = jdata[row]["sentiment_title"]
            companyDetails["trend_title"] = jdata[row]["trend_title"]
            companyDetails["twitter_data_file"] = jdata[row]["twitter_data_file"]
            companyDetails["twitter_trend_file"] = jdata[row]["twitter_trend_file"]
            companyDetails["temp_file"] = jdata[row]["temp_file"]
            companyList.append(companyDetails)
            count = count + 1
    return companyList, count


companyList, count = getCompanyDetailsList()




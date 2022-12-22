import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://hackathon.pirimidtech.com/hackathon"

def init_req(phonenum, templateType):
    url=f"{BASE_URL}/init/redirection"
    body = {
        "vuaId": f"{phonenum}@dashboard-aa-uat",
        "templateType": templateType,
        "trackingId": os.environ.get("trackingId"),
        "redirectionUrl": "https://devfolio.co/bobworld-hackathon/dashboard"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": os.environ.get("API_KEY")
    }

    response = requests.post(url, json=body, headers=headers)  
    referenceId = response.json()["referenceId"]
    return referenceId,response 


def fetch_data(phonenum, templateType):
    url=f"{BASE_URL}/consent/data/fetch"
    referenceId,_=init_req(phonenum, templateType)

    params={
        "referenceId":referenceId,
        "trackingId": os.environ.get("trackingId")
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": os.environ.get("API_KEY")
    }

    getrequest = requests.get(url, params=params, headers=headers)
    print(getrequest)

    return getrequest.json()

def fetch_analysed_data(phonenum, templateType):
    url=f"{BASE_URL}/consent/analytics/fetch"
    referenceId,_=init_req(phonenum, templateType)
    params={
        "referenceId":referenceId,
        "trackingId": os.environ.get("trackingId")
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": os.environ.get("API_KEY")
    }

    getanalysedrequest = requests.get(url, params=params, headers=headers)

    return getanalysedrequest.json()

data=fetch_data("9205231677", "ONETIME")
print(data)
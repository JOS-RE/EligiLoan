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
    print(response.json())
    referenceId = response.json()["referenceId"]
    print(type(referenceId))
    return referenceId


def fetch_data(phonenum, templateType):
    url=f"{BASE_URL}/consent/data/fetch"
    params={
        "referenceId":init_req(phonenum, templateType),
        "trackingId": os.environ.get("trackingId")
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": os.environ.get("API_KEY")
    }
    print(params)
    print(headers)
    getrequest = requests.get(url, params=params, headers=headers)
    print(getrequest)

    return getrequest.json()

def fetch_analysed_data(phonenum, templateType):
    url=f"{BASE_URL}/consent/analytics/fetch"
    params={
        "referenceId":init_req(phonenum, templateType),
        "trackingId": os.environ.get("trackingId")
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": os.environ.get("API_KEY")
    }

    getanalysedrequest = requests.get(url, params=params, headers=headers)

    return getanalysedrequest.json()

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()


def bobinitreq(phonenum, templateType):
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

    response = requests.post(
        "https://hackathon.pirimidtech.com/hackathon/init/redirection", json=body, headers=headers)  
    print(response)
    return response.json()

def fetch_data(phonenum, templateType,bobinitreq):
    params={
        "referenceId":bobinitreq(phonenum, templateType)["referenceId"],
        "trackingId": os.environ.get("trackingId")
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": os.environ.get("API_KEY")
    }

    getrequest = requests.get("https://hackathon.pirimidtech.com/hackathon/consent/data/fetch", params=params, headers=headers)
    print(getrequest)

    return getrequest.json()

print(fetch_data("9205231677", "ONETIME",bobinitreq))
    
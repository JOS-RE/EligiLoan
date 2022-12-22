import os
import requests
from dotenv import load_dotenv
load_dotenv()

from post_initreq import bobinitreq


def fetch_data(phonenum, templateType):
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

print(fetch_data("9205231677", "ONETIME"))
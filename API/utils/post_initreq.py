import streamlit as st
import os
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://hackathon.pirimidtech.com/hackathon"

def init_req(phonenum, templateType):
    url=f"{BASE_URL}/init/redirection"
    body = {
        "vuaId": f"{phonenum}@dashboard-aa-uat",
        "templateType": templateType,
        "trackingId": st.secrets["trackingId"],
        "redirectionUrl": "https://devfolio.co/bobworld-hackathon/dashboard"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": st.secrets["API_KEY"]
    }

    response = requests.post(url, json=body, headers=headers)  
    referenceId = response.json()["referenceId"]
    return response


def fetch_data(phonenum, templateType):
    url=f"{BASE_URL}/consent/data/fetch"
    params={
        "referenceId":init_req(phonenum, templateType)["referenceId"],
        "trackingId": st.secrets["trackingId"]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": st.secrets["API_KEY"]
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
        "trackingId": st.secrets["trackingId"]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "API_KEY": st.secrets["API_KEY"]
    }

    getanalysedrequest = requests.get(url, params=params, headers=headers)

    return getanalysedrequest.json()

req=init_req("9922700288","ONETIME")
print(req.json()["redirectionUrl"])
# req=init_req("9205231677","ONETIME")
# print(req)
# data=fetch_data("9205231677","ONETIME")
# print(data)


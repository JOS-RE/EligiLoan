import streamlit as st

from API.utils.post_initreq import init_req, fetch_data, fetch_analysed_data

st.title("Login")

st.markdown("""
    ## Login to your account""")

phone_number = st.text_input("Phone Number")
template_type = st.selectbox("Template Type", ["ONETIME", "PERIODIC"])

if st.button("Login"):
    req=init_req(phone_number, template_type)
    if req.json()["redirectionUrl"]:
        st.write(req.json()["redirectionUrl"])
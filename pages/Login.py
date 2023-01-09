import streamlit as st
from PIL import Image 

image2=Image.open('assets/logo2.png')
st.set_page_config(
    page_title="Login",
    page_icon=image2,
)


from API.utils.post_initreq import init_req, fetch_data, fetch_analysed_data

st.title("Login")

st.markdown("""
    ## Login to your account""")

phone_number = st.text_input("Phone Number")
template_type = st.selectbox("Template Type", ["ONETIME", "PERIODIC"])

col11, col22, col3 = st.columns(3)

with col11:
    if st.button("Verify"):
        req=init_req(phone_number, template_type)
        if req.json()["redirectionUrl"]:
            linkk = req.json()["redirectionUrl"]
        with col22:
            st.write(f'''
                        <a target="blank" href="{linkk}">
                            <button style=" border-color: orange; padding:10px 20px;   background-color: #fa6400f0; color:white;  border: none;  border-radius: .25rem;" >
                                Go to accept consent
                            </button>
                        </a>
                        ''',
                        unsafe_allow_html=True
                    )       
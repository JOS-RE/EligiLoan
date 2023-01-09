import streamlit as st
from PIL import Image 

image2=Image.open('assets/logo2.png')
st.set_page_config(
    page_title="EligiLoan",
    page_icon=image2,
)

image = Image.open('assets/poster.jpg')
st.image(image, caption='ELIGILOAN')
st.write("# Welcome to Eligiloan! 👋")


with st.sidebar:
    st.write(f'''
                        <a target="blank" href="https://eligiloan-eda.vercel.app/">
                            <button style=" border-color: orange; padding:10px 20px;   background-color: #fa6400f0; color:white;  border: none;  border-radius: .25rem;" >
                                View EDA report
                            </button>
                        </a>
                        ''',
                        unsafe_allow_html=True
                    ) 




st.markdown(
    """

    ## A step-by-step guide 

    The process is quite straightforward. BOB offers loans to eligible applicants with strong financial profiles. 
    Individuals need to provide their basic personal, employment, income and property details to know if you are fit to apply for a loan.

    ### 1 . Login 

    Step one is the login part, you just have to work your way through the following simple steps.
    - Enter your mobile number
    - Enter the OTP recieved 
    - accept consent in the Safe portal

    ### 2. Loan page

    Once you login, you will be redirected to the loan page.
    - Offer all relevant details such as loan amount, loan history, income, etc.
    - Click on the submit option once you have filled in all the details.
    - Our algorithm will assess your eligibility based on the details provided by you and you will be awarded with a `yes` or a `no`.
"""
)


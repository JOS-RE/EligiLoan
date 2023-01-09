import streamlit as st
from API.services.loadModel import LoanDefaultPrediction

import torch
import time
import numpy as np

LABEL_DICT={0:'Not Eligible',1:'Eligible'}
# -------------------------------------------------------------------------------

st.title('Welcome to Eligiloan 🏦')
# orange text

st.subheader('We are here to help you get the best loan counseling')
# -------------------------------------------------------------------------------

col1, col2 = st.columns(2)
with col1:
    # 1 loan amount
    la1 = st.number_input(
    'Please enter the Loan amount you want',
    0,
    help='Help message goes here'
    )

with col2:
    # 2 expected interest rate
    la2 = st.number_input(
        'Expected interest rate',
        0,
        help='Please enter the interest rate you wish to pay'
    )


# 3 current monthly income thats is already being deducted from your salary
la3 = st.slider(
    'Please enter the percentage income to debt ratio',
    0,
    100,
    10,
    help='Please enter the percentage of your income that is already being deducted from your salary'
)

col11, col22 = st.columns(2)

with col11:
    # 4 property verification status
    la4 = st.selectbox(
        'Please confirm your property verification status',
        options=('Not Verified', 'Verified', 'Source Verified'),
        help='Please select the option that best describes your property verification status'
        )

with col22:
    # 5 property mortgage value
    la5 = st.number_input(
        'Property mortgage value',
        0,
        help='Please enter the mortgage value of your verified property'
    )

# ------------------------------
st.subheader('Now let us look at your past performance to give you :orange[more personalised results]')
# ------------------------------


col111, col222 = st.columns(2)

with col111:
    # 6 how many active loans you have
    lb1 = st.number_input(
        'How many active loans do you have',
        0,
        help='Please enter the number of active loans you have'
    )

with col222:
    # 7 what range is your current loan amount 
    lb2 = st.number_input(
        'What is your existing loan amount',
        0,
        help='Please enter the range of your current loan amount'
    )

# 8 "  "   "  have you repaid your previous loan
lb3 = st.slider( 
    'What percentage of your previous loan have you repaid',
    0,
    100,
    10,
    help='Please enter the percentage of your previous loan that you have repaid'
)
lb3 = lb2 * lb3 / 100

# 9 "  "   "  have you repaid your previous interest

lb4 = st.number_input(
    'What is the interest amount of your previous loan',
    0,
    help='Please enter the interest amount of your previous loan'
)

# 10 "  "   "  repaied in recoveries and collection recovery fees
lb5 = st.number_input(
    'What is the recoveries and collection recovery fees of your previous loan',
    0,
    help='Please enter the recoveries and collection recovery fees of your previous loan'
)

# ------------------------------
st.subheader('We :orange[totally believe you]! We just need a few more things to give you the most accurate results.')
# ------------------------------


# 11 range of revolving balance
lc1 = st.number_input(
    'Please enter your existing revolving balance',
    0,
    help='Please enter your existing revolving balance')
    # write help string


col1111, col2222 = st.columns(2)

with col1111:
    # 12 range of revolving utilization
    lc2 = st.slider(
        'What is your revolving utilization',
        0,
        100,
        10,
        help='Please enter the percentage of your revolving utilization'
    )

with col2222:
    # 13 range of revolving credit limit
    lc3 = st.number_input(
        'What is your revolving credit limit',
        0,
        help='Please enter the range of your revolving credit limit'
    )

# 14 times had to face enquires from bank
lc4 = st.slider(
    'How many times did you overcome enquires from the bank',
    0,
    10,
    1
)
# ------------------------------

st.subheader(':orange[Perfect !] We are almost done. Just 2 more questions')

col11111, col22222 = st.columns(2)

with col11111:
    # 15 delinquency status in last 2 years
    ld1 = st.slider(
        'What is your delinquency rate in last 2 years',
        0,
        10,
        1,
        help='Please enter the number of times you have been delinquent in the last 2 years'
    )



with col22222:
    # 16 late payment status in last 2 years
    ld2 = st.slider(
        'What is your late payment percentage',
        0,
        100,
        10,
        help='Please enter the percentage of your late payments in the last 2 years'
    )
    print(type(ld2))

# Now add a submit button to the form:
if st.button('Check my chances'):
    st.write('Thank you')

    model=LoanDefaultPrediction.load_model()
    with st.spinner('Predicting your chances of loan default...'):
        time.sleep(2)
        prediction=LoanDefaultPrediction.predict(torch.tensor([[la1,la2,la3,la4,la5,lb1,lb2,lb3,lb4,lb5,lc1,lc2,lc3,lc4,ld1,ld2]],dtype=torch.float32),model)
        st.success('Your chances of loan default are {}'.format(LABEL_DICT[prediction[0]]))



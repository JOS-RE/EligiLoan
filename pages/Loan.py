import streamlit as st
from API.services.loadModel import LoanDefaultPrediction

import torch
import time
import numpy as np

LABEL_DICT={0:'Not Eligible',1:'Eligible'}
veri_status_mapping={'Not Verified':0,'Verified':1,'Source Verified':2}
Initial_List_Status_mapping={'w':0,'f':1}
# -------------------------------------------------------------------------------

st.title('Welcome to Eligiloan 🏦')
# orange text

st.subheader('We are here to help you get the best loan counseling')
# -------------------------------------------------------------------------------

col1, col2 = st.columns(2)
with col1:
    # 1 loan amount
    loan_amount = st.number_input(
    'Please enter the Loan amount you want',
    0,
    help='Help message goes here'
    )

with col2:
    # 2 expected interest rate
    expected_interest_rate = st.number_input(
        'Expected interest rate',
        0,
        help='Please enter the interest rate you wish to pay'
    )


# 3 current monthly income thats is already being deducted from your salary
income_to_debt_ratio = st.slider(
    'Please enter the percentage income to debt ratio',
    0,
    100,
    10,
    help='Please enter the percentage of your income that is already being deducted from your salary'
)

col11, col22 = st.columns(2)

with col11:
    # 4 property verification status
    verification_status = st.selectbox(
        'Please confirm your property verification status',
        options=('Not Verified', 'Verified', 'Source Verified'),
        help='Please select the option that best describes your property verification status'
        )

with col22:
    # 5 property mortgage value
    mortgage_value = st.number_input(
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
    active_loans = st.number_input(
        'How many active loans do you have',
        0,
        help='Please enter the number of active loans you have'
    )

with col222:
    # 7 what range is your current loan amount 
    current_loan_amount = st.number_input(
        'What is your existing loan amount',
        0,
        help='Please enter the range of your current loan amount'
    )

# 8 "  "   "  have you repaid your previous loan
loans_repaid = st.slider( 
    'What percentage of your previous loan have you repaid',
    0,
    100,
    10,
    help='Please enter the percentage of your previous loan that you have repaid'
)
loans_repaid = loans_repaid/100 * current_loan_amount

# 9 "  "   "  have you repaid your previous interest

interest_repaid = st.number_input(
    'What is the interest amount of your previous loan',
    0,
    help='Please enter the interest amount of your previous loan'
)

recoveries = st.number_input(
    'What is your recoveries',
    0
)

# 10 "  "   "  repaied in recoveries and collection recovery fees
collection_recovery_fee = st.number_input(
    'What is the recoveries and collection recovery fees of your previous loan',
    0,
    help='Please enter the recoveries and collection recovery fees of your previous loan'
)

# ------------------------------
st.subheader('We :orange[totally believe you]! We just need a few more things to give you the most accurate results.')
# ------------------------------

# number input for 'Funded Amount', 'Funded Amount Investor', 'Term', 'Initial List Status', 'Total Accounts', 'Loan Status'

Funded_Amount = st.number_input(
    'Please enter your Funded Amount',
    0,
    help='Please enter your Funded Amount'
)

Funded_amount_invester = st.number_input(
    'Please enter your Funded Amount Investor',
    0,
    help='Please enter your Funded Amount Investor'
)

Term = st.slider(
    'Please enter your Term',
    0,
    100,
    10,
    help='Please enter your Term'
)

Initial_List_Status = st.selectbox(
    'Please select your Initial List Status',
    options=('f', 'w'),
    help='Please select your Initial List Status'
)

Total_Accounts = st.number_input(
    'Please enter your Total Accounts',
    0,
    help='Please enter your Total Accounts'
)

# 0, 1 slider for loan status
Loan_status = st.slider(
    'Please enter your loan status',
    0,
    1,
    0,
    help='Please enter your loan status'
)

# 11 range of revolving balance
revolving_balance = st.number_input(
    'Please enter your existing revolving balance',
    0,
    help='Please enter your existing revolving balance')
    # write help string


col1111, col2222 = st.columns(2)

with col1111:
    # 12 range of revolving utilization
    revolving_utilization = st.slider(
        'What is your revolving utilization',
        0,
        100,
        10,
        help='Please enter the percentage of your revolving utilization'
    )

with col2222:
    # 13 range of revolving credit limit
    revolving_credit_limit = st.number_input(
        'What is your revolving credit limit',
        0,
        help='Please enter the range of your revolving credit limit'
    )

# 14 times had to face enquires from bank
enquires = st.slider(
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
    delinquency = st.slider(
        'What is your delinquency rate in last 2 years',
        0,
        10,
        1,
        help='Please enter the number of times you have been delinquent in the last 2 years'
    )



with col22222:
    # 16 late payment status in last 2 years
    late_payment = st.slider(
        'What is your late payment percentage',
        0,
        100,
        10,
        help='Please enter the percentage of your late payments in the last 2 years'
    )

# Now add a submit button to the form:
if st.button('Check my chances'):
    st.write('Thank you')

    model=LoanDefaultPrediction.load_model()
    with st.spinner('Predicting your chances of loan default...'):
        time.sleep(2)
        prediction=LoanDefaultPrediction.predict(torch.tensor([[loan_amount,Funded_Amount,Funded_amount_invester,Term,expected_interest_rate,mortgage_value,veri_status_mapping[verification_status],income_to_debt_ratio,delinquency,enquires,active_loans,revolving_balance,revolving_utilization,Total_Accounts,Initial_List_Status_mapping[Initial_List_Status],interest_repaid,late_payment,recoveries,collection_recovery_fee,revolving_credit_limit,loans_repaid,current_loan_amount]],dtype=torch.float32),model)

        st.success('Your chances of loan default are {}'.format(LABEL_DICT[prediction.item()]))



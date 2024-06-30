# Import necessary libraries
import streamlit as st
import requests

# Remove spaces from the input params
def sanitize_input(input):
    # Remove spaces from input
    return input.replace(" ", "")

# Streamlit page title
st.title('Snowflake Sample API App')

# URLS for REST calls
BASE_URL = st.text_input('Enter the Base URL here:', 'http://localhost:5000', key='base_url_input')
cust_by_phone_url = f"{BASE_URL}/customer/details_by_phone"
cust_orders_by_phone_url = f"{BASE_URL}/order/orders_by_cust_phone"
order_summary_url = f"{BASE_URL}/order/details_by_orderkey"

# Input box for the user to enter the customer's phone number
phone_st = st.text_input('Enter the Customer Phone Number here:', '', key='cust_input')
phone = sanitize_input(phone_st)

# Button to make the GET request for Customer Details
if st.button('Customer Details'):
    if phone:
        # Construct the full URL with the parameter
        full_url = f"{cust_by_phone_url}?phone={phone}"

        try:
            # Make the GET request
            response = requests.get(full_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Display the response content as HTML
                st.markdown(response.text, unsafe_allow_html=True)
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a parameter.")


# Input box for the user to enter the customer's phone number
phone_st_o = st.text_input('Enter the Customer Phone Number here:', '', key='cust_order_input')
phone_o = sanitize_input(phone_st_o)

# Button to make the GET request for Customer Details
if st.button('Customer Orders'):
    if phone_o:
        # Construct the full URL with the parameter
        full_url = f"{cust_orders_by_phone_url}?phone={phone_o}"

        try:
            # Make the GET request
            response = requests.get(full_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Display the response content as HTML
                st.markdown(response.text, unsafe_allow_html=True)
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a parameter.")

# Input box for the user to enter the customer's phone number
okey_st = st.text_input('Enter the Order Key here:', '', key='order_summary_input')
okey = sanitize_input(okey_st)

# Button to make the GET request for Customer Details
if st.button('Order Summary'):
    if okey:
        # Construct the full URL with the parameter
        full_url = f"{order_summary_url}?okey={okey}"

        try:
            # Make the GET request
            response = requests.get(full_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Display the response content as HTML
                st.markdown(response.text, unsafe_allow_html=True)
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a parameter.")
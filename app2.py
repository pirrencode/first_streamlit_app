import streamlit as st

# Title of the application
st.title('Simple Streamlit App')

# Input section
name = st.text_input('Enter your name:')
number = st.number_input('Enter a number:', min_value=0, value=0)

# Button to trigger actions
if st.button('Submit'):
    st.write(f'Hello, {name}!')
    st.write(f'The square of {number} is {number ** 2}')

# Display some static text
st.write('This is a simple Streamlit application example.')

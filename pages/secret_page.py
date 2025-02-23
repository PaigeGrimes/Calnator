import streamlit as st

def secret_page():
    st.title("This is the Secret Page")

    if st.button("Say Hello"):
        st.write("Hello there, my friend!")

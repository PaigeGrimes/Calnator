# pages/secret_page.py
import streamlit as st
# Import your DB functions (adjust the import path as needed)
from modify_db import create_user_table, add_user

def secret_page():
    st.title("This is the Secret Page")

    # 1) Make sure the table exists
    create_user_table()

    # 2) Use a form for the username & password fields
    with st.form(key="secret_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Create User")

    # 3) If they submit, call add_user (which writes to the DB)
    if submit_button:
        if new_username and new_password:
            add_user(new_username, new_password)
        else:
            st.error("Please enter both username and password.")

    # Optional: A separate button for some other action
    if st.button("Say Hello"):
        st.write("Hello there, my friend!")

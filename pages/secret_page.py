import streamlit as st

def secret_page():
    st.title("This is the Secret Page")

    # A simple form for usernames and passwords
    with st.form(key="secret_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Submit")

    # If user clicks "Submit" inside the form
    if submit_button:
        # Do whatever you need here
        st.write(f"**You entered:**\n- Username: `{username}`\n- Password: `{password}`")
        
    # Optional: a separate "Say Hello" button outside the form
    if st.button("Say Hello"):
        st.write("Hello there, my friend!")
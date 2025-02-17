import streamlit as st
from pages.home_page import home_page 

###############################################################################
# 1. Credentials (hard-coded for demo)
###############################################################################
VALID_USERNAME = "john"
VALID_PASSWORD = "secret123"

###############################################################################
# 2. Streamlit UI tweaks
###############################################################################
def hide_default_streamlit_ui():
    """
    Hide Streamlit's default top-right hamburger menu
    plus the footer.
    """
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def hide_entire_sidebar():
    """
    Hide the entire sidebar region so it's not visible at all.
    """
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

###############################################################################
# 3. Login screen
###############################################################################
def login_screen():
    """
    Prompts the user for username and password.
    Sets `logged_in` to True in session_state if credentials match.
    """
    st.title("Please log in to continue")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")

    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.stop()  # Try to instantly refresh

        else:
            st.error("Invalid username or password.")

###############################################################################
# 4. Main flow
###############################################################################
def main():
    # Hide Streamlit's default menus on every load
    hide_default_streamlit_ui()

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # If the user is NOT logged in, hide sidebar & show login form
    if not st.session_state.logged_in:
        hide_entire_sidebar()
        login_screen()
        st.stop()  # Ensure we don't display the home page code below

    # If the user *is* logged in, load the home page from home_page.py
    home_page()


###############################################################################
# 5. Run the app
###############################################################################
if __name__ == "__main__":
    main()

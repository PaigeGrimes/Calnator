import streamlit as st
from modify_db import check_user_credentials
import secret_page as secret


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
    # if st.button("Secret Button"):
    #     st.session_state.active_page = "secret_page"
    #     st.session_state.need_rerun = True

    with st.form(key="login_form", border=False):
        st.title("Please log in to continue")

        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        user = check_user_credentials(username, password)
        # Check the database
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]  # Store the user’s database ID
            st.session_state.user_name = user[1]
            st.success("Login successful!")
            st.rerun()  # Trigger rerun flag
        else:
            st.error("Invalid username or password.")


###############################################################################
# 4. Main flow
###############################################################################
def main():
    # st.set_page_config(page_title="Calendarnator9001")
    hide_default_streamlit_ui()

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"  # default
        # Handle rerun based on session state flag
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    # -------------------------------------------------------
    # Only force the login screen if user isn't logged in
    # AND they are trying to access something other than the secret page
    # -------------------------------------------------------
    if not st.session_state.logged_in:  # and st.session_state.active_page != "secret_page":
        hide_entire_sidebar()
        login, new_user = st.tabs(["Login", "Create Account"])
        with login:
            login_screen()
        with new_user:
            secret.secret_page()


###############################################################################
# 5. Run the app
###############################################################################
if __name__ == "__main__":
    main()

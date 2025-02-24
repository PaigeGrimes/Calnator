import streamlit as st
from pages import home_page as h
from modify_db import check_user_credentials

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
    if st.button("Secret Button"):
        st.session_state.active_page = "secret_page"
        st.st.experimental_rerun()  # or st.experimental_rerun() if you want an immediate page reload

    with st.form(key="login_form", border=False):
        st.title("Please log in to continue")

        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        # Check the database
        if check_user_credentials(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")


###############################################################################
# 4. Main flow
###############################################################################
def main():
    st.set_page_config(page_title="Calendarnator9001")
    hide_default_streamlit_ui()

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"  # default

    # -------------------------------------------------------
    # Only force the login screen if user isn't logged in
    # AND they are trying to access something other than the secret page
    # -------------------------------------------------------
    if not st.session_state.logged_in and st.session_state.active_page != "secret_page":
        hide_entire_sidebar()
        login_screen()
        st.stop()

    # -------------------------------------------------------
    # If they want the secret page:
    #   - They can see it whether or not they are logged in
    #   - Otherwise, load the normal home page
    # -------------------------------------------------------
    if st.session_state.active_page == "secret_page":
        from pages import secret_page as s
        s.secret_page()
    else:
        from pages import home_page as h
        h.home_page()


###############################################################################
# 5. Run the app
###############################################################################
if __name__ == "__main__":
    main()

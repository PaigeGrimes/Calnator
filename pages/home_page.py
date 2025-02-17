import streamlit as st


def home_page():
    """
    This function displays the home page content.
    Including the sidebar and main body content.
    """
    hide_menu = """
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
"""
    st.markdown(hide_menu, unsafe_allow_html=True)

    # MAIN CONTENT
    st.subheader("Hello John!")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image("/Users/trunk/Documents/Calnator/img/image_08IKWGM3.png")

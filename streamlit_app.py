import streamlit as st

name = "Jane"


def hide_menu():
    # Hide default multipage navigation
    hidemenu = """
        <style>
            [data-testid="stSidebarNav"] { display: none; }
        </style>
    """
    st.markdown(hidemenu, unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.title("Calendarnator9001")
        st.page_link("streamlit_app.py", label="Home")
        st.page_link("pages/calendar.py", label="Calendar")
        st.page_link("pages/todo.py", label="To-Do List")


hide_menu()
sidebar()
st.subheader(f"Hello {name}!")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.image("img/image_08IKWGM3.png")

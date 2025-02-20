import streamlit as st
import modify_db as db
from datetime import datetime
from streamlit_calendar import calendar
import pandas as pd

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
        st.page_link("pages/add_event.py", label="Add Calendar Events")
        st.page_link("pages/calendar.py", label="Calendar")
        st.page_link("pages/todo.py", label="To-Do List")
        st.page_link("pages/hours.py", label="Hours of Operation")


st.set_page_config(page_title="Calendarnator9001")
hide_menu()
sidebar()

st.subheader(f"Hello :grey[{name}]!", divider="grey")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.image("img/pushyourself.jpg")
    with col2:
        st.subheader("Current Assignments")
        calendar_events = db.show_events()
        assignments = {'Title': ['HW1', 'HW2', 'HW3', 'HW4'],
                       'Due': ["2/20", "2/21", "2/22", "2/23"],
                       "Complete": [True, True, False, False]}
        df = pd.DataFrame(assignments)
        st.data_editor(df, use_container_width=True, hide_index=True)

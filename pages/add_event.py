import streamlit as st
import modify_db as db
from datetime import datetime
import streamlit_app as sapp

st.set_page_config(page_title="Calendarnator9001")
sapp.hide_menu()
sapp.sidebar()
st.subheader("Add Important Events and Assignments")
tab1, tab2 = st.tabs(["Add To Calendar", "Add Assignments"])
with tab1:
    event_name = st.text_input("Event Name")
    event_date = st.date_input("Event Date")
    event_start = st.time_input("Event Start Time")
    event_end = st.time_input("Event End Time")

    start_datetime = datetime.combine(event_date, event_start)
    end_datetime = datetime.combine(event_date, event_end)

    # Convert datetime to string in "DD/MM/YYYY HH:MM:SS" format
    start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Add event to database
    if st.button("Add Event"):
        if event_start <= event_end:
            db.add_event(event_name, start_datetime_str, end_datetime_str)
        else:
            st.code(f"Invalid input. \nStart time {event_start} cannot be less than the end time {event_end}.")
with tab2:
    hw_title = st.text_input("Assignment title")
    hw_due_date = st.date_input("Date due")
    if st.button("Add Assignment"):
        # TODO: Add logic for adding assignment to db
        pass



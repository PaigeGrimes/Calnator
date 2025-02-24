import pandas as pd
import streamlit as st
import modify_db as db
from datetime import datetime
from datetime import time
from home_page import hide_menu, sidebar
import streamlit_app


# Convert the time input from 12-hour to 24-hour format
def convert_to_24hr_format(t_str, period):
    # Parse the string time to a time object
    t = datetime.strptime(t_str, "%I:%M").time()  # 12-hour format parsing

    if period == "AM" and t.hour == 12:
        return time(0, t.minute)  # Convert 12 AM to 00:MM
    elif period == "PM" and t.hour != 12:
        return time(t.hour + 12, t.minute)  # Convert PM to 24-hour format
    return t  # Return as is if already in 24-hour format


def update_titles():
    st.session_state.selected_title = None
    st.session_state.selected_time = None  # Reset time selection when date changes


# Callback function to reset time when title changes
def update_times():
    st.session_state.selected_time = None


#####################################################################
#       Initialize the sidebar and header for the page              #
#####################################################################
if not st.session_state.logged_in:
    streamlit_app.main()
# TODO: Why does the df not update when an assignment is added??????????
elif st.session_state.logged_in:
    st.set_page_config(page_title="Calendarnator9001")
    hide_menu()
    sidebar()

    db.create_event_db()
    db.create_assignment_db()

    addCal, removeCal, addHw = st.tabs(["Add To Calendar", "Remove Calendar Event", "Add Assignments"])
    #####################################################################
    # tab addCal: Add an event to the events database for the Calendar
    #####################################################################
    with addCal:
        # Create a list of time options with a set of 0:15 for a 12-hour time frame
        time_options = [
            "12:00", "12:15", "12:30", "12:45",
            "01:00", "01:15", "01:30", "01:45",
            "02:00", "02:15", "02:30", "02:45",
            "03:00", "03:15", "03:30", "03:45",
            "04:00", "04:15", "04:30", "04:45",
            "05:00", "05:15", "05:30", "05:45",
            "06:00", "06:15", "06:30", "06:45",
            "07:00", "07:15", "07:30", "07:45",
            "08:00", "08:15", "08:30", "08:45",
            "09:00", "09:15", "09:30", "09:45",
            "10:00", "10:15", "10:30", "10:45",
            "11:00", "11:15", "11:30", "11:45"
        ]
        # Get the event name and date from the user
        event_name = st.text_input("Event Name")
        event_date = st.date_input("Event Date")

        col1, col2 = st.columns(2)
        with col1:
            event_start = st.selectbox("Event Start Time", time_options)  # default to 12:00
            event_end = st.selectbox("Event End Time", time_options)  # default to 12:00
        with col2:
            # Dropdown for AM/PM selection
            start_period = st.selectbox("Start Time Period", ["AM", "PM"], index=0)
            end_period = st.selectbox("End Time Period", ["AM", "PM"], index=0)

        # Convert the selected time to 24-hour format
        start_time_24hr = convert_to_24hr_format(event_start, start_period)
        end_time_24hr = convert_to_24hr_format(event_end, end_period)

        # Combine date with time in 24-hour format to get datetime objects
        start_datetime = datetime.combine(event_date, start_time_24hr)
        end_datetime = datetime.combine(event_date, end_time_24hr)

        # Convert datetime to string in "DD/MM/YYYY HH:MM:SS" format
        start_datetime_str = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        end_datetime_str = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Display the final event datetime strings
        st.write("Start Date and Time:", start_datetime_str)
        st.write("End Date and Time:", end_datetime_str)
        # Add event to database
        if st.button("Add Event"):
            # If there's an overlapping time, display an error
            if db.check_time_exists(st.session_state.user_id, start_datetime_str, end_datetime_str):
                st.error("The time you have selected overlaps with another event")
            # If the start time is less than the end time, add the event
            elif start_time_24hr < end_time_24hr:
                db.add_event(st.session_state.user_id, event_name, event_date, start_datetime_str, end_datetime_str)
            # Display an error for the final case in-which the start time is greater than the end time
            else:
                st.code(f"Invalid input. \nStart time {event_start} cannot be less than the end time {event_end}.")

    #####################################################################
    # tab removeCal: Remove an event from the events database
    #####################################################################
    with removeCal:
        # Get the contents of the database
        events = db.show_events(st.session_state.user_id)
        # Create a set of event dates so that they are unique and add them to a drop-down menu
        event_dates = set(events['date'].to_list())
        # Initialize session state for dropdown selections
        if "selected_date" not in st.session_state:
            st.session_state.selected_date = None
        if "selected_title" not in st.session_state:
            st.session_state.selected_title = None
        if "selected_time" not in st.session_state:
            st.session_state.selected_time = None
        st.session_state.selected_date = st.selectbox("Select a date", options=event_dates, key="date_select",
                                                      on_change=update_titles)

        if st.session_state.selected_date:
            # If they have selected a date, display those values in the drop-down of event titles.
            event_titles = events.loc[events['date'] == st.session_state.selected_date, 'title'].unique().tolist()
            st.session_state.selected_title = st.selectbox("Available assignments", options=event_titles,
                                                           key="title_select", on_change=update_times)
            if st.session_state.selected_title:
                event_times = events.loc[(events["date"] ==
                                          st.session_state.selected_date) &
                                         (events["title"] ==
                                          st.session_state.selected_title), "datetime_start"].to_list()
                print(len(event_times))
                if len(event_times) > 1:
                    st.session_state.selected_time = st.selectbox("Choose a corresponding time", options=event_times,
                                                                  key="time_select")

        if st.button("Remove Event"):
            # If the event exists, remove it.
            if st.session_state.selected_date and st.session_state.selected_title:
                print("button pressed and session state passed")
                db.remove_event(
                    st.session_state.user_id,
                    st.session_state.selected_title,
                    st.session_state.selected_date,
                    st.session_state.selected_time
                )

                st.rerun()

    #####################################################################
    # tab addHw: Add an assignment to the assignments database that
    # keeps track of the assignments the user needs to complete.
    #####################################################################
    with addHw:
        # Get the title and due date of an assignment from the user.
        hw_title = st.text_input("Assignment title")
        hw_due_date = st.date_input("Date due")

        if st.button("Add Assignment"):
            # Add the assignment to database.
            if hw_title:
                db.add_hw(st.session_state.user_id, hw_title, hw_due_date)

        st.subheader("Current Assignments")
        df = pd.DataFrame(db.get_hw(st.session_state.user_id,).iloc[:, 2:].to_numpy(),
                          columns=list(["Assignments", "Due Date"]))
        st.data_editor(df, hide_index=True)

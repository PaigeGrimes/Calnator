from datetime import datetime
import streamlit as st
from streamlit_calendar import calendar
import modify_db as db
from login import streamlit_app

#####################################################################
#       Initialize the sidebar and header for the page
#####################################################################
if not st.session_state.logged_in:
    streamlit_app.main()
# TODO: Why does the df not update when an assignment is added??????????
elif st.session_state.logged_in:
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    st.title(f"{st.session_state.user_name}'s Calendar")    # TODO: Change to users name

    # Define the calendar mode that is to be used. Can be a list if different options are needed.
    mode = "daygrid"

    # Get the calendar events
    calendar_events = db.show_events(st.session_state.user_id)

    # Create a list of events
    events = [
        {
            "allDay": False,
            "title": row["title"],
            "start": datetime.strptime(row["datetime_start"], "%Y-%m-%d %H:%M:%S").isoformat(),
            # Convert to ISO8601 string
            "end": datetime.strptime(row["datetime_end"], "%Y-%m-%d %H:%M:%S").isoformat(),
            # Convert to ISO8601 string
        }
        for _, row in calendar_events.iterrows()
    ]

    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "selectable": "true",
    }
    # Define the different options to change the calendar view - specific options for daygrid
    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": "2025-02-02",
        "initialView": "dayGridMonth",
    }

    state = calendar(
        events=st.session_state.get("events", events),
        options=calendar_options,
        custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
        """,
        key=mode,
    )


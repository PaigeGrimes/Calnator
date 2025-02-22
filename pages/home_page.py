from datetime import datetime
import streamlit as st
import modify_db as db
import numpy as np
import pandas as pd


###############################################################################
# Hide the default streamlit sidebar.
###############################################################################
def hide_menu():
    # Hide default multipage navigation
    hidemenu = """
        <style>
            [data-testid="stSidebarNav"] { display: none; }
        </style>
    """
    st.markdown(hidemenu, unsafe_allow_html=True)


###############################################################################
# Show each streamlit page on the sidebar
###############################################################################
def sidebar():
    with st.sidebar:
        st.title("Calendarnator9001")
        st.page_link("streamlit_app.py", label="Home")
        st.page_link("pages/add_event.py", label="Add/Drop")
        st.page_link("pages/calendar.py", label="Calendar")
        st.page_link("pages/todo.py", label="To-Do List")
        st.page_link("pages/hours.py", label="Hours of Operation")


# TODO: Why does the df not update when an assignment is added??????????
def home_page():
    """
    This function displays the home page content.
    Including the sidebar and main body content.
    """
    hide_menu()
    sidebar()

    # MAIN CONTENT # TODO: Have it load the users name
    st.subheader(f"Hello :grey[John]!", divider="grey")

    with st.container():
        col1, col2 = st.columns(2)
        # Col1 displays a motivational image to the user
        with col1:
            st.image("img/pushyourself.jpg")

        # Col2 displays the assignments that the user has not yet completed.
        with col2:
            st.subheader("Current Assignments")
            df = db.get_hw()

            df['date_due'] = pd.to_datetime(df['date_due']).dt.date  # Convert String to date
            current_date = datetime.today().date()  # Get today's date

            # Check if any assignment due date has passed. If yes, display an error
            if (df['date_due'] < current_date).any():
                print(df["date_due"])
                st.error("There are assignments that are overdue!", icon="⚠️")

            if len(df) > 0:
                # Create a column of False boolean values for the assignments
                complete = [False] * len(df)
                is_complete = np.array(complete).reshape(-1, 1)  # Ensure the list is a column vector

                # Drop the first column before concatenation
                df_without_first_col = df.iloc[:, 1:].to_numpy()

                # Concatenate along columns
                df_new = np.concatenate((df_without_first_col, is_complete), axis=1)

                # Create a new df
                df = pd.DataFrame(df_new, columns=list(["Assignment", "Due Date", "Complete"]))
                df["Complete"] = False      # Ensure all values start as boolean
                st.session_state.df = df    # Initialize session state

                # Display the users homework
                edited_df = st.data_editor(st.session_state.df, use_container_width=True, hide_index=True)

                # Ensure "Complete" column is properly formatted
                edited_df["Complete"] = edited_df["Complete"].astype(bool)

                if st.button("Complete",
                             help="Check the box next to the completed assignment, then select the Complete button"):
                    # Get titles of completed homework
                    filtered_df = edited_df.loc[edited_df["Complete"], :]

                    completed_titles = filtered_df["Assignment"].tolist()
                    print("Completed Titles:", completed_titles)  # Debugging output

                    # If there exists an assignment that has been completed
                    if completed_titles:
                        # Remove the completed assignments
                        db.remove_hw(completed_titles)

                        # Refresh the data after deletion
                        df = db.get_hw()
                        df['date_due'] = pd.to_datetime(df['date_due'])  # Convert to datetime format
                        if len(df) > 0:
                            df_without_first_col = df.iloc[:, 1:].to_numpy()
                            is_complete = np.array([False] * len(df)).reshape(-1, 1)
                            df_new = np.concatenate((df_without_first_col, is_complete), axis=1)
                            df = pd.DataFrame(df_new, columns=["Assignment", "Due Date", "Complete"])
                            df["Complete"] = False

                        # Update session state and refresh
                        st.session_state.df = edited_df
                        st.rerun()
                    else:
                        # Handle when no assignment has been selected.
                        st.code("You have not selected an assignment.")
            else:
                # Let the user know that no assignments are due
                st.markdown('You have *no assignment due* :smile:🎉')
                st.markdown('''If you have a new assignment, go to the :green[Add/Drop] 
                tab and add the assignment so you wont forget!''')

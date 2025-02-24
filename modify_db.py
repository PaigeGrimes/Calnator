import sqlite3
import streamlit as st
import pandas as pd


#####################################################################
#                Methods for storing and retrieving user data
#####################################################################

def create_user_table():
    """Creates the user table if it does not already exist."""
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_user(username, password):
    """
    Registers a new user into the database.
    NOTE: This stores plaintext passwords. For production, store a hashed password.
    """
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success(f"User '{username}' created successfully!")
    except sqlite3.IntegrityError:
        st.error(f"Username '{username}' is already taken. Please choose a different username.")
    conn.close()


def check_user_credentials(username, password):
    """
    Returns True if username+password exist in the database, else False.
    """
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    row = cursor.fetchone()
    conn.close()
    # return row is not None
    return row

#####################################################################
#       Methods to add, retrieve, and remove calendar events
#####################################################################
def create_event_db():
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # Create a table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            date TEXT,
            datetime_start TEXT,
            datetime_end TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()

    # Close the connection
    conn.close()


def add_event(user_id, title, date, date_start, date_end):
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (user_id, title, date, datetime_start, datetime_end) VALUES (?, ?, ?, ?, ?)",
                   (user_id, title, date, date_start, date_end))
    conn.commit()
    st.success(f"Event '{title}' added!")

    # Close the connection
    conn.close()


def check_time_exists(user_id, date_start, date_end):
    try:
        conn = sqlite3.connect("Calendar.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM events WHERE (datetime_start = ? OR datetime_end = ?) AND user_id=?",
            (date_start, date_end, user_id)
        )
        result = cursor.fetchone()[0]
        conn.close()
        if result > 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def show_events(user_id):
    # Connect to SQLite database
    conn = sqlite3.connect("Calendar.db")
    try:
        # Create a dataframe of calendar events
        df = pd.read_sql_query(f"SELECT * FROM events WHERE user_id={user_id}", conn)
        return df
    except sqlite3.IntegrityError:
        print("No events available")

    conn.close()
    # Return the dataframe
    return


def remove_event(user_id, title, date, time):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        if title and date and time:
            cursor.execute("DELETE FROM events WHERE user_id = ? AND title = ? AND date = ? AND datetime_start = ?",
                           (user_id, title, date, time))
        elif title and date:
            cursor.execute("DELETE FROM events WHERE user_id=? AND title = ? AND date = ?",
                           (user_id, title, date))
            st.success(f"{title} removed")
        conn.commit()
        st.success(f"The following event has been removed: '{title}' ")
    except sqlite3.IntegrityError:
        print("That assignment does not exist.")

    # Close the connection
    conn.close()


#####################################################################
#       Methods to add and remove homework assignments due          #
#####################################################################
def create_assignment_db():
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS assignments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            title TEXT UNIQUE,
                            date_due TEXT,
                            FOREIGN KEY(user_id) REFERENCES users(id)
                        )
                    """)
    conn.commit()
    conn.close()


def add_hw(user_id, title, due_date):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO assignments (user_id, title, date_due) VALUES (?, ?, ?)",
                       (user_id, title, due_date))
        conn.commit()
        st.success("Your assignment due date has been scheduled.")
    except sqlite3.IntegrityError:
        st.code("Could not add the assignment. That assignment may already exist.")

    conn.close()


def get_hw(user_id):
    # Connect to SQLite database
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # conn.execute("DROP TABLE assignments")
    try:
        # Create a dataframe of calendar events
        df = pd.read_sql_query(f"SELECT * FROM assignments WHERE user_id={user_id}", conn)
        return df
    except sqlite3.IntegrityError:
        print("No assignment are currently due.")

    conn.close()
    # Return the dataframe
    return


def remove_hw(user_id, title):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        for hw in title:
            cursor.execute("DELETE FROM assignments WHERE user_id = ? AND title = (?) ", (user_id, hw))
            conn.commit()
    except sqlite3.IntegrityError:
        print("That assignment does not exist.")

    # Close the connection
    conn.close()


#####################################################################
#       Methods to add and remove tasks from the to-do list         #
#####################################################################
def create_todo_db():
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # Create a table if not exists
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS todo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
    conn.commit()
    conn.close()


def add_todo(user_id, task):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # conn.execute("DROP TABLE todo") # for testing
    cursor.execute("INSERT INTO todo (user_id, title) VALUES (?,?)", (user_id, task))
    conn.commit()
    st.success(f"Task '{task}' added!")

    # Close the connection
    conn.close()


def remove_task(user_id, task):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM todo WHERE title = ? AND user_id=?", (task, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print()

    # Close the connection
    conn.close()


def get_todos(user_id):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    tasks = []  # Initialize tasks as an empty list
    try:
        cursor.execute("SELECT title FROM todo WHERE user_id =?", (user_id,))
        tasks = cursor.fetchall()  # tasks is a list of tuples
    except sqlite3.Error as e:
        print(e)
    conn.close()
    # Return a list of task titles
    return [task[0] for task in tasks]

import sqlite3
import streamlit as st
import pandas as pd


#####################################################################
#       Methods to add and retrieve calendar events                 #
#####################################################################
def add_event(title, date_start, date_end):
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # conn.execute("DROP TABLE events")
    # Create a table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            datetime_start TEXT,
            datetime_end TEXT
        )
    """)
    conn.commit()
    cursor.execute("INSERT INTO events (title, datetime_start, datetime_end) VALUES (?, ?, ?)",
                   (title, date_start, date_end))
    conn.commit()
    st.success(f"Event '{title}' added!")

    # Close the connection
    conn.close()


def show_events():
    # Connect to SQLite database
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    datetime_start TEXT,
                    datetime_end TEXT
                )
            """)
        conn.commit()
        # Create a dataframe of calendar events
        df = pd.read_sql_query("SELECT * FROM events", conn)
        return df
    except sqlite3.IntegrityError:
        print("No events available")

    conn.close()
    # Return the dataframe
    return


#####################################################################
#       Methods to add and remove tasks from the to-do list         #
#####################################################################
def add_todo(task):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # conn.execute("DROP TABLE todo") # for testing
    # Create a table if not exists
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT
            )
        """)
    conn.commit()
    cursor.execute("INSERT INTO todo (title) VALUES (?)",
                   (task))
    conn.commit()
    st.success(f"Event '{task}' added!")

    # Close the connection
    conn.close()


def remove_task(task):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS todo (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT
                    )
                """)
        cursor.execute("DELETE FROM todo WHERE (title) = (?)", task)
        conn.commit()
    except sqlite3.IntegrityError:
        print()
    st.success(f"Event '{task}' removed!")

    # Close the connection
    conn.close()

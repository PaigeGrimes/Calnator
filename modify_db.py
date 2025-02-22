import sqlite3
import streamlit as st
import pandas as pd


#####################################################################
#       Methods to add, retrieve, and remove calendar events
#####################################################################
def add_event(title, date, date_start, date_end):
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # conn.execute("DROP TABLE events")
    # Create a table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT,
            datetime_start TEXT,
            datetime_end TEXT
        )
    """)
    conn.commit()
    cursor.execute("INSERT INTO events (title, date, datetime_start, datetime_end) VALUES (?, ?, ?, ?)",
                   (title, date, date_start, date_end))
    conn.commit()
    st.success(f"Event '{title}' added!")

    # Close the connection
    conn.close()


def check_time_exists(date_start, date_end):
    try:
        conn = sqlite3.connect("Calendar.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM events WHERE datetime_start = ? or datetime_end = ?",
                       (date_start, date_end))
        result = cursor.fetchone()[0]
        conn.close()
        if result > 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def show_events():
    # Connect to SQLite database
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    date TEXT,
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


def remove_event(title, date, time):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS events (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            date TEXT,
                            datetime_start TEXT,
                            datetime_end TEXT
                        )
                    """)
        if title and date and time:
            cursor.execute("DELETE FROM events WHERE title = ? AND date = ? AND datetime_start = ?",
                           (title, date, time))
        elif title and date:
            cursor.execute("DELETE FROM events WHERE title = ? AND date = ?",
                           (title, date))
            st.success(f'{title} removed')
        conn.commit()
        st.success(f"The following event has been removed: '{title}' ")
    except sqlite3.IntegrityError:
        print("That assignment does not exist.")

    # Close the connection
    conn.close()


#####################################################################
#       Methods to add and remove homework assignments due          #
#####################################################################
def add_hw(title, due_date):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS assignments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE,
                        date_due TEXT
                    )
                """)
        conn.commit()
        cursor.execute("INSERT INTO assignments (title, date_due) VALUES (?, ?)",
                       (title, due_date))
        conn.commit()
        st.success("Your assignment due date has been scheduled.")
    except sqlite3.IntegrityError:
        st.code("Could not add the assignment. That assignment may already exist.")

    conn.close()


def get_hw():
    # Connect to SQLite database
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    # conn.execute("DROP TABLE assignments")
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS assignments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE,
                        date_due TEXT
                    )
                """)
        conn.commit()
        # Create a dataframe of calendar events
        df = pd.read_sql_query("SELECT * FROM assignments", conn)
        return df
    except sqlite3.IntegrityError:
        print("No assignment are currently due.")

    conn.close()
    # Return the dataframe
    return


def remove_hw(title):
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS assignments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT UNIQUE,
                            date_due TEXT
                        )
                    """)
        for hw in title:
            print(hw)
            cursor.execute("DELETE FROM assignments WHERE title = (?) ", (hw,))
            conn.commit()
    except sqlite3.IntegrityError:
        print("That assignment does not exist.")

    # Close the connection
    conn.close()


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
    cursor.execute("INSERT INTO todo (title) VALUES (?)", (task,))
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
        cursor.execute("DELETE FROM todo WHERE title = ?", (task,))
        conn.commit()
    except sqlite3.IntegrityError:
        print()


    # Close the connection
    conn.close()

def get_todos():
    conn = sqlite3.connect("Calendar.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS todo (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT
                    )
                """)
        cursor.execute("SELECT title FROM todo")
        tasks = cursor.fetchall()  # tasks is a list of tuples
    except sqlite3.Error as e:
        print(e)
    conn.close()
    # Return a list of task titles
    return [task[0] for task in tasks]

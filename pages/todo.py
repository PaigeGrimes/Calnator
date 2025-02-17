import streamlit as st
import streamlit_app as saap

# Hide default multipage navigation
hide_menu = """
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)


st.title("To-Do List")
saap.sidebar()
import streamlit as st

# Initialize tasks in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

with st.popover("Add task"):
    todo = st.text_input("What do you need to do? :)")
    if st.button("Add Task"):
        if todo:  # Avoid adding empty tasks
            st.session_state.tasks.append(todo)
            st.rerun()  # Refresh UI

# Display tasks with checkboxes
with st.container():
    for task in st.session_state.tasks:
        if st.checkbox(task, key=task):
            st.session_state.tasks.remove(task)
            st.rerun()  # Refresh UI after removing checked task

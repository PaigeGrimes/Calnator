import streamlit
import streamlit as st
from pages import home_page as home

st.set_page_config(page_title="Calendarnator9001")
home.hide_menu()
home.sidebar()

st.subheader("To-Do List")

# Initialize tasks in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
with st.popover("Add task"):
    todo = st.text_input("What do you need to do? :)")
    if st.button("Add Task"):
        if todo in st.session_state.tasks:
            st.error("You cannot enter duplicate tasks!")
        else:
            if todo:  # Avoid adding empty tasks
                st.session_state.tasks.append(todo)
                st.rerun()  # Refresh UI

# Display tasks with checkboxes
with st.container():
    for task in st.session_state.tasks:
        if st.checkbox(task, key=task):
            #st.session_state.tasks.remove(task)
            st.rerun()  # Refresh UI after removing checked task

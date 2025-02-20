import streamlit as st
from pages import home_page as home

st.set_page_config(page_title="Calendarnator9001")
home.hide_menu()
home.sidebar()

st.subheader("To-Do List")

# Initialize tasks in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = {}

with st.popover("Add task"):
    todo = st.text_input("What do you need to do? :)")
    if st.button("Add Task"):
        if todo in st.session_state.tasks:
            st.error("You cannot enter duplicate tasks!")
        else:
            if todo:  # Avoid adding empty tasks
                st.session_state.tasks.append(todo)
                st.session_state.completed_tasks[todo] = False  # Initialize as unchecked
                st.rerun()  # Refresh UI


# Function to remove completed tasks
def remove_completed_tasks():
    st.session_state.tasks = [
        task for task in st.session_state.tasks if not st.session_state.completed_tasks[task]
    ]
    st.session_state.completed_tasks = {
        task: completed for task, completed in st.session_state.completed_tasks.items() if not completed
    }


# Display tasks with checkboxes
with st.container():
    for task in st.session_state.tasks:
        st.session_state.completed_tasks[task] = st.checkbox(
            task, key=task, value=st.session_state.completed_tasks.get(task, False)
        )

    st.button("Delete Completed Tasks", on_click=remove_completed_tasks)

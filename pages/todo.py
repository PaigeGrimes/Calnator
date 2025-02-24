import streamlit as st
from home_page import hide_menu, sidebar
from modify_db import remove_task, add_todo, get_todos, create_todo_db
import streamlit_app

if not st.session_state.logged_in:
    streamlit_app.main()
# TODO: Why does the df not update when an assignment is added??????????
elif st.session_state.logged_in:
    st.set_page_config(page_title="Calendarnator9001")
    hide_menu()
    sidebar()
    col1, col2 = st.columns(2)
    create_todo_db()


    # Initialize tasks in session state
    if "tasks" not in st.session_state:
        st.session_state.tasks = get_todos(st.session_state.user_id)
    if "completed_tasks" not in st.session_state:
        # Initialize as a dictionary, marking tasks as not completed
        st.session_state.completed_tasks = {task: False for task in st.session_state.tasks}

    with col2:
        st.subheader("Add New Task")
        todo = st.text_input("What do you need to do? :)")
        if st.button("Add Task"):
            if todo in st.session_state.tasks:
                st.error("You cannot enter duplicate tasks!")
            else:
                if todo:  # Avoid adding empty tasks
                    add_todo(st.session_state.user_id, todo)
                    st.session_state.tasks.append(todo)
                    st.session_state.completed_tasks[todo] = False  # Initialize as unchecked
                    st.rerun()  # Refresh UI


    # Function to remove completed tasks
    def remove_completed_tasks():
        # Only remove tasks that are marked as completed
        for task, is_completed in st.session_state.completed_tasks.items():
            if is_completed:
                remove_task(st.session_state.user_id, task)
        # Update session state to only include incomplete tasks
        st.session_state.tasks = [
            task for task in st.session_state.tasks if not st.session_state.completed_tasks.get(task, False)
        ]
        st.session_state.completed_tasks = {
            task: completed for task, completed in st.session_state.completed_tasks.items() if not completed
        }
        st.success("Completed tasks removed!")


    # Display tasks with checkboxes
    with col1:
        st.subheader("To-Do List")
        for task in st.session_state.tasks:
            st.session_state.completed_tasks[task] = st.checkbox(
                task, key=task, value=st.session_state.completed_tasks.get(task, False)
            )

        st.button("Delete Completed Tasks", on_click=remove_completed_tasks)

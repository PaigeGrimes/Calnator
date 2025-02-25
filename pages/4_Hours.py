import streamlit as st
from login import streamlit_app

if not st.session_state.logged_in:
    streamlit_app.main()
# TODO: Why does the df not update when an assignment is added??????????
elif st.session_state.logged_in:
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("Hours of Operation")
    st.markdown("[Campus Map](#campus-map)")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("HAM", help="Hamilton Cafeteria")
            st.write('__Monday – Friday Hours__')
            st.write('''
            * __Breakfast__: 8:00am – 10:00pm
            * __Lunch__: 11:00am – 2:00pm
            * __Dinner__: 5:00pm – 7:30pm''')
            st.write('__Saturday & Sunday Hours__')
            st.write('''
            * __Brunch__: 11:00am – 1:00pm
            * __Dinner__: 5:00pm – 7:00pm''')
        with st.container(border=True):
            st.subheader("U-Cook", help="Hamilton Cafeteria U-Cook")
            st.write('__Monday – Friday Hours__')
            st.write('''* 6:00am – 12:00am''')
            st.write('__Saturday Hours__')
            st.write('''* 10:00am – 9:00pm''')
            st.write('__Sunday Hours__')
            st.write('''* 10:00am – 12:00am''')
        with st.container(border=True):
            st.subheader("Social Roast Coffee")
            st.write('__Monday – Friday Hours__')
            st.write('''* 8:00am - 5:00pm''')
            st.write('__Saturday & Sunday Hours__')
            st.write('''* 10:00am – 9:00pm''')
        with st.container(border=True):
            st.subheader("Mama G’s Bakery & Coffee at Four Winds")
            st.write('__Monday – Friday Hours__')
            st.write('''* 9:00am – 3:30pm''')
            st.write('__Saturday & Sunday Hours__')
            st.write('''* CLOSED''')
    with col2:
        with st.container(border=True):
            st.subheader("Jane Bancroft Cook Library")
            st.write('__Monday – Thursday Hours__')
            st.write('* 8:00am- 11:00pm')
            st.write('__Friday Hours__')
            st.write('* 8:00am- 5:00pm')
            st.write('__Saturday Hours__')
            st.write('* 12:00pm- 6:00pm')
            st.write('__Sunday Hours__')
            st.write('* 3:00pm- 11:00pm')
        with st.container(border=True):
            st.subheader("WRC", help="Writing Resource Center")
            st.write("Library Hours, located at LBR 132")
            st.subheader("QRC", help="Quantitative Resource Center")
            st.write("Library Hours, located at LBR 119")
        with st.container(border=True):
            st.subheader("CEO", help="Counseling & Wellness Services")
            st.write('__Monday – Friday Hours__')
            st.write('* 8:00am- 5:00pm')
        with st.container(border=True):
            st.subheader("CWC", help="Career Engagement and Opportunity")
            st.write('__Monday – Friday Hours__')
            st.write('* 8:00am- 5:00pm')

    st.header("Campus Map")
    st.image("img/campusMap.jpg")

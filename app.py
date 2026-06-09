import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import hashlib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("skillbridge.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT UNIQUE,
password TEXT,
department TEXT
)
""")

conn.commit()

# ---------------- FUNCTIONS ----------------
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password, department):
    try:
        c.execute(
            "INSERT INTO users(name,email,password,department) VALUES(?,?,?,?)",
            (
                name,
                email,
                make_hash(password),
                department
            )
        )
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    c.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (
            email,
            make_hash(password)
        )
    )
    data = c.fetchone()
    return data

# ---------------- HEADER ----------------
st.title("🎓 SkillBridge AI")
st.subheader("SDG 4 : Quality Education")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------------- AUTH ----------------
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Account",
        [
            "Login",
            "Register"
        ]
    )

    if menu == "Register":

        st.header("Create Account")

        name = st.text_input("Name")

        email = st.text_input("Email")

        department = st.selectbox(
            "Department",
            [
                "CSE",
                "ECE",
                "EE",
                "ME"
            ]
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            if register_user(
                name,
                email,
                password,
                department
            ):
                st.success("Registration Successful")
            else:
                st.error("Email already exists")

    else:

        st.header("Login")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                email,
                password
            )

            if user:
                st.session_state.logged_in = True
                st.session_state.user_name = user[1]
                st.rerun()

            else:
                st.error("Invalid Credentials")

# ---------------- MAIN APP ----------------
else:

    st.sidebar.success(
        f"Welcome {st.session_state.user_name}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Career Guidance",
            "Study Planner",
            "Learning Resources",
            "Progress Tracker",
            "Profile"
        ]
    )

    # DASHBOARD
    if page == "Dashboard":

        st.header("Student Dashboard")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Student ID",
            "231001001091"
        )

        c2.metric(
            "Department",
            "CSE"
        )

        c3.metric(
            "SDG Goal",
            "SDG 4"
        )

        st.markdown("---")

        st.write("""
        SkillBridge AI helps students
        discover learning resources,
        create study plans,
        and explore career opportunities.
        """)

    # CAREER GUIDANCE
    elif page == "Career Guidance":

        st.header("Career Recommendation")

        coding = st.slider(
            "Coding Interest",
            1,
            10,
            5
        )

        maths = st.slider(
            "Math Interest",
            1,
            10,
            5
        )

        design = st.slider(
            "Design Interest",
            1,
            10,
            5
        )

        if st.button("Recommend Career"):

            if coding >= 8 and maths >= 8:
                career = "AI Engineer"

            elif coding >= 8:
                career = "Software Developer"

            elif design >= 8:
                career = "UI/UX Designer"

            else:
                career = "Data Analyst"

            st.success(
                f"Recommended Career: {career}"
            )

    # STUDY PLANNER
    elif page == "Study Planner":

        st.header("Smart Study Planner")

        days = st.number_input(
            "Days Left For Exam",
            1,
            365,
            30
        )

        subjects = st.text_area(
            "Subjects (one per line)"
        )

        if st.button("Generate Plan"):

            subject_list = [
                x.strip()
                for x in subjects.split("\n")
                if x.strip()
            ]

            plan = []

            for i, subject in enumerate(subject_list):
                plan.append(
                    [
                        f"Week {i+1}",
                        subject
                    ]
                )

            df = pd.DataFrame(
                plan,
                columns=[
                    "Week",
                    "Focus Subject"
                ]
            )

            st.dataframe(df)

    # RESOURCES
    elif page == "Learning Resources":

        st.header("Free Learning Resources")

        resources = {
            "Python":
            "https://www.w3schools.com/python/",

            "DSA":
            "https://www.geeksforgeeks.org/",

            "Web Development":
            "https://www.freecodecamp.org/",

            "AI":
            "https://www.kaggle.com/learn"
        }

        skill = st.selectbox(
            "Choose Skill",
            list(resources.keys())
        )

        st.info(resources[skill])

    # PROGRESS
    elif page == "Progress Tracker":

        st.header("Learning Progress")

        progress = st.slider(
            "Overall Progress %",
            0,
            100,
            50
        )

        st.progress(progress/100)

        data = pd.DataFrame(
            {
                "Subject":
                [
                    "Python",
                    "DSA",
                    "DBMS",
                    "OS",
                    "CN"
                ],
                "Completion":
                [
                    90,
                    75,
                    65,
                    50,
                    40
                ]
            }
        )

        fig = px.bar(
            data,
            x="Subject",
            y="Completion",
            title="Subject Progress"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # PROFILE
    elif page == "Profile":

        st.header("Student Profile")

        st.write(
            "Name:",
            st.session_state.user_name
        )

        st.write(
            "Department: CSE"
        )

        st.write(
            "Student ID: 231001001091"
        )

    # LOGOUT
    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.rerun()
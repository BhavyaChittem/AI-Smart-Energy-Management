import streamlit as st
import pandas as pd
import base64
from model import predict_energy


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Smart Energy Management",
    page_icon="⚡",
    layout="wide"
)


# --------------------------------------------------
# BACKGROUND ONLY - HTML + CSS
# --------------------------------------------------

with open("bg.png", "rb") as f:
    bg = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: #28a745;
        color: white;
        border: none;
    }}

    div.stButton > button[kind="primary"]:hover {{
        background-color: #218838;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "section" not in st.session_state:
    st.session_state.section = "Home"

if "units" not in st.session_state:
    st.session_state.units = 5.0

if "hours" not in st.session_state:
    st.session_state.hours = 5.0

if "appliances" not in st.session_state:
    st.session_state.appliances = 3

if "temperature" not in st.session_state:
    st.session_state.temperature = 27.0

if "previous_usage" not in st.session_state:
    st.session_state.previous_usage = 4.0

if "predicted" not in st.session_state:
    st.session_state.predicted = predict_energy(5, 3, 27, 4)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("⚡ Smart Energy")
    st.write("### Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.section = "Home"

    if st.button("📊 Energy Dashboard", use_container_width=True):
        st.session_state.section = "Dashboard"

    if st.button("🔌 Analyze Energy Usage", use_container_width=True):
        st.session_state.section = "Analyze"

    if st.button("💡 Smart Recommendations", use_container_width=True):
        st.session_state.section = "Recommendations"

    if st.button("📈 Energy Usage Trends", use_container_width=True):
        st.session_state.section = "Trends"

    st.divider()

    st.info(
        "This project uses Machine Learning to predict "
        "energy consumption and provide smart recommendations."
    )


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("⚡ AI-Based Smart Energy Management System")


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def dashboard():

    st.header("📊 Energy Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Today's Energy Usage",
            f"{st.session_state.units:.2f} kWh"
        )

    with col2:
        st.metric(
            "AI Predicted Usage",
            f"{st.session_state.predicted:.2f} kWh"
        )

    with col3:

        if st.session_state.predicted < 5:
            status = "LOW"
        elif st.session_state.predicted < 8:
            status = "MODERATE"
        else:
            status = "HIGH"

        st.metric("Energy Status", status)


def analyze_energy():

    st.header("🔌 Analyze Energy Usage")

    units = st.number_input(
        "Today's Energy Usage (kWh)",
        min_value=0.0,
        value=st.session_state.units,
        step=0.5
    )

    hours = st.number_input(
        "Usage Hours",
        min_value=0.0,
        value=st.session_state.hours,
        step=1.0
    )

    appliances = st.number_input(
        "Number of Appliances",
        min_value=1,
        value=st.session_state.appliances,
        step=1
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        value=st.session_state.temperature,
        step=1.0
    )

    previous_usage = st.number_input(
        "Previous Usage (kWh)",
        min_value=0.0,
        value=st.session_state.previous_usage,
        step=0.5
    )

    if st.button(
        "🔍 Analyze Energy Usage",
        type="primary",
        use_container_width=True
    ):

        prediction = predict_energy(
            hours,
            appliances,
            temperature,
            previous_usage
        )

        st.session_state.units = units
        st.session_state.hours = hours
        st.session_state.appliances = appliances
        st.session_state.temperature = temperature
        st.session_state.previous_usage = previous_usage
        st.session_state.predicted = prediction

        st.success("Energy analysis completed successfully!")

        st.subheader("🤖 AI Prediction")

        st.metric(
            "Predicted Energy Consumption",
            f"{prediction:.2f} kWh"
        )

        if prediction < 5:
            st.success("🟢 LOW Energy Usage")
        elif prediction < 8:
            st.warning("🟡 MODERATE Energy Usage")
        else:
            st.error("🔴 HIGH Energy Usage")


def recommendations():

    st.header("💡 Smart Recommendations")

    prediction = st.session_state.predicted

    if prediction < 5:

        st.success(
            "Your energy consumption is low. Keep following your current habits!"
        )

        st.write("• Switch off unused appliances.")
        st.write("• Use energy-efficient appliances.")
        st.write("• Continue monitoring your daily usage.")

    elif prediction < 8:

        st.warning(
            "Your energy consumption is moderate. Some improvements can reduce usage."
        )

        st.write("• Switch off appliances when not required.")
        st.write("• Reduce unnecessary usage hours.")
        st.write("• Prefer energy-efficient devices.")
        st.write("• Monitor high-consumption appliances.")

    else:

        st.error(
            "Your energy consumption is high. Immediate energy-saving actions are recommended."
        )

        st.write("• Reduce unnecessary appliance usage.")
        st.write("• Switch off appliances when not in use.")
        st.write("• Reduce usage hours.")
        st.write("• Avoid running multiple high-power appliances together.")


def trends():

    st.header("📈 Energy Usage Trends")

    data = pd.read_csv("data/energy_data.csv")

    st.subheader("Historical Energy Usage")

    st.line_chart(
        data[["previous_usage", "current_usage"]]
    )

    st.subheader("Energy Usage by Hours")

    chart_data = data[
        ["hours", "current_usage"]
    ].set_index("hours")

    st.bar_chart(chart_data)


def home():

    # Dashboard
    dashboard()

    st.divider()

    # Features
    st.header("✨ System Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🤖 **AI Prediction**")
        st.write(
            "Machine Learning predicts future energy consumption."
        )

    with col2:
        st.write("💡 **Smart Recommendations**")
        st.write(
            "The system provides energy-saving suggestions."
        )

    with col3:
        st.write("📊 **Usage Analysis**")
        st.write(
            "Analyze energy usage based on different inputs."
        )

    st.divider()

    # Analyze
    analyze_energy()

    st.divider()

    # Recommendations
    recommendations()

    st.divider()

    # Trends
    trends()


# --------------------------------------------------
# SHOW SELECTED SECTION
# --------------------------------------------------

if st.session_state.section == "Home":

    home()

elif st.session_state.section == "Dashboard":

    dashboard()

elif st.session_state.section == "Analyze":

    analyze_energy()

elif st.session_state.section == "Recommendations":

    recommendations()

elif st.session_state.section == "Trends":

    trends()
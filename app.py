import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="🌦️ Weather Prediction", page_icon="🌤️", layout="centered")

with open("naive_bayes_weather.pkl", "rb") as f:
    nb_model = pickle.load(f)

features = ['Humidity', 'Temperature', 'Wind Speed', 'Pressure']

st.markdown("<h1 style='text-align:center; color:#4B9CD3;'>🌦️ Weather Forecast App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Enter weather conditions below to check if it will rain tomorrow</p>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        humidity = st.number_input("💧 Humidity (%)", min_value=0, max_value=100, value=75, step=1)
        wind_speed = st.number_input("🌬️ Wind Speed (km/h)", min_value=0, max_value=150, value=12, step=1)

    with col2:
        temperature = st.number_input("🌡️ Temperature (°C)", min_value=-30, max_value=50, value=28, step=1)
        pressure = st.number_input("🌪️ Pressure (hPa)", min_value=800, max_value=1100, value=1010, step=1)

st.markdown("---")
if st.button("🔮 Predict Weather", use_container_width=True):
    custom_input = pd.DataFrame([[humidity, temperature, wind_speed, pressure]], columns=features)
    prediction = nb_model.predict(custom_input)[0]
    prob = nb_model.predict_proba(custom_input)[0][1] * 100

    if prediction == 1:
        st.success(f"🌧️ Yes, it looks like it will rain tomorrow! ☔\n\n💡 Probability: **{prob:.2f}%**")
    else:
        st.info(f"☀️ No, tomorrow should be dry and clear!\n\n💡 Probability: **{prob:.2f}%**")

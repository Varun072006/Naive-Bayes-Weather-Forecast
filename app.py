import gradio as gr
import pandas as pd
import pickle

with open("Naive-Bayes-Weather-Forecast/naive_bayes_weather_model.pkl", "rb") as f:
    nb_model = pickle.load(f)

features = ['Humidity', 'Temperature', 'Wind Speed', 'Pressure']

def predict_weather(humidity, temperature, wind_speed, pressure):
    custom_input = pd.DataFrame([[humidity, temperature, wind_speed, pressure]], columns=features)
    prediction = nb_model.predict(custom_input)[0]
    prob = nb_model.predict_proba(custom_input)[0][1] * 100
    
    if prediction == 1:
        return f"🌧️ Yes, it looks like it will rain tomorrow! ☔\n\n💡 Probability: **{prob:.2f}%**"
    else:
        return f"☀️ No, tomorrow should be dry and clear!\n\n💡 Probability: **{prob:.2f}%**"

def handle_login(username, password):
    if username == "user" and password == "pass":
        return gr.update(visible=False), gr.update(visible=True)
    else:
        return gr.update(visible=True, value="❌ Invalid credentials. Please try again."), gr.update(visible=False)

with gr.Blocks() as demo:
    with gr.Column(visible=True) as login_page:
        gr.Markdown("## 🔐 Login")
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        error_message = gr.Textbox(label="", interactive=False, visible=False)
        login_btn = gr.Button("Login")
    
    with gr.Column(visible=False) as main_page:
        gr.Markdown("## 🌦️ Weather Forecast App")
        gr.Markdown("Enter weather conditions below to check if it will rain tomorrow.")
        
        with gr.Row():
            humidity = gr.Number(label="💧 Humidity (%)", value=75, precision=0)
            temperature = gr.Number(label="🌡️ Temperature (°C)", value=28, precision=0)
        
        with gr.Row():
            wind_speed = gr.Number(label="🌬️ Wind Speed (km/h)", value=12, precision=0)
            pressure = gr.Number(label="🌪️ Pressure (hPa)", value=1010, precision=0)
        
        predict_btn = gr.Button("🔮 Predict Weather")
        output = gr.Textbox(label="Prediction Result", interactive=False)
        
        predict_btn.click(fn=predict_weather, 
                          inputs=[humidity, temperature, wind_speed, pressure], 
                          outputs=output)

    login_btn.click(fn=handle_login, 
                    inputs=[username, password], 
                    outputs=[error_message, main_page])

demo.launch(share=True)

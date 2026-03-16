import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="Diabetes Predictor", layout="centered")
st.markdown(
    """
    <style>
    /* Change all headers font */
    h1, h2, h3, h4, h5, h6, .css-1d391kg { 
        font-family: 'Times New Roman', serif !important;
    }
    /* Input box font */
    .stNumberInput>div>div>input {
        font-family: 'Times New Roman', serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Diabetes Prediction")
st.write("Enter patient details to predict the likelihood of diabetes.")

# --- SIDEBAR COLOR CUSTOMIZATION ---
st.sidebar.header("Customize Colors")

bg_color = st.sidebar.color_picker("Background Color", "#F5F5F5")
text_color = st.sidebar.color_picker("Text Color", "#000000")
button_color = st.sidebar.color_picker("Button Color", "#4CAF50")
button_text_color = st.sidebar.color_picker("Button Text Color", "#FFFFFF")
input_bg_color = st.sidebar.color_picker("Input Box Background", "#FFFFFF")
input_text_color = st.sidebar.color_picker("Input Text Color", "#000000")
success_bg_color = st.sidebar.color_picker("Success Box Background", "#D4EDDA")
success_text_color = st.sidebar.color_picker("Success Text Color", "#155724")
error_bg_color = st.sidebar.color_picker("Error Box Background", "#F8D7DA")
error_text_color = st.sidebar.color_picker("Error Text Color", "#721C24")

# --- APPLY CSS STYLES ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stButton>button {{
        background-color: {button_color};
        color: {button_text_color};
        font-weight: bold;
        height: 3em;
        width: 100%;
    }}
    input[type="number"] {{
        background-color: {input_bg_color};
        color: {input_text_color};
        font-size: 16px;
        height: 2em;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- INPUT FIELDS ---
glucose = st.number_input("Glucose Level", min_value=0.0, max_value=300.0, value=120.0)
bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0)
age = st.number_input("Age", min_value=0, max_value=120, value=30)
bp = st.number_input("Blood Pressure", min_value=0.0, max_value=200.0, value=70.0)

API_URL = "http://127.0.0.1:8000/predict"

# --- PREDICTION BUTTON ---
if st.button("Predict Diabetes"):
    data = {
        "Glucose": glucose,
        "BMI": bmi,
        "Age": age,
        "BloodPressure": bp
    }

    with st.spinner("Predicting..."):
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                result = response.json()
                if "prediction" in result:
                    outcome = "Diabetic" if result["prediction"] == 1 else "Non-Diabetic"
                    st.markdown(
                        f"<div style='background-color:{success_bg_color}; color:{success_text_color}; padding:10px; border-radius:5px; text-align:center;'>Prediction: <b>{outcome}</b></div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div style='background-color:{error_bg_color}; color:{error_text_color}; padding:10px; border-radius:5px; text-align:center;'>API Error: {result.get('error', 'Unknown error')}</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    f"<div style='background-color:{error_bg_color}; color:{error_text_color}; padding:10px; border-radius:5px; text-align:center;'>Error: Could not get prediction</div>",
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.markdown(
                f"<div style='background-color:{error_bg_color}; color:{error_text_color}; padding:10px; border-radius:5px; text-align:center;'>Error connecting to API: {e}</div>",
                unsafe_allow_html=True
            )


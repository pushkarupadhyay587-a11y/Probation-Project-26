import requests
import streamlit as st

API_URL = "https://probation-project-26.onrender.com/predict"

st.set_page_config(page_title="Income Predictor", page_icon="💼")
st.title("Adult Income Predictor")
st.write("Enter the person's details to predict their income category.")

with st.form("prediction_form"):
    age = st.number_input("Age", min_value=17, max_value=100, value=35)
    workclass = st.selectbox(
        "Workclass",
        ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov",
         "Local-gov", "State-gov", "Without-pay", "Never-worked"],
    )
    fnlwgt = st.number_input("Final weight (fnlwgt)", min_value=1, value=200000)
    education_num = st.number_input(
        "Education number", min_value=1, max_value=16, value=10
    )
    marital_status = st.selectbox(
        "Marital status",
        ["Never-married", "Married-civ-spouse", "Divorced", "Separated",
         "Widowed", "Married-spouse-absent", "Married-AF-spouse"],
    )
    occupation = st.selectbox(
        "Occupation",
        ["Adm-clerical", "Exec-managerial", "Handlers-cleaners",
         "Machine-op-inspct", "Other-service", "Sales", "Craft-repair",
         "Transport-moving", "Farming-fishing", "Tech-support",
         "Prof-specialty", "Protective-serv", "Armed-Forces",
         "Priv-house-serv"],
    )
    relationship = st.selectbox(
        "Relationship",
        ["Not-in-family", "Husband", "Wife", "Own-child", "Unmarried", "Other-relative"],
    )
    race = st.selectbox(
        "Race",
        ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"],
    )
    sex = st.selectbox("Sex", ["Male", "Female"])
    capital_gain = st.number_input("Capital gain", min_value=0, value=0)
    capital_loss = st.number_input("Capital loss", min_value=0, value=0)
    hours_per_week = st.number_input(
        "Hours per week", min_value=1, max_value=99, value=40
    )
    native_country = st.text_input("Native country", value="United-States")

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education.num": education_num,
        "marital.status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "sex": sex,
        "capital.gain": capital_gain,
        "capital.loss": capital_loss,
        "hours.per.week": hours_per_week,
        "native.country": native_country,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        prediction = result.get("income", result.get("prediction"))

        if prediction is None:
            st.error(f"Unexpected API response: {result}")
        else:
            st.success(f"Predicted income category: **{prediction}**")
    except requests.RequestException as exc:
        st.error(f"Could not reach the prediction API: {exc}")
    except (ValueError, KeyError) as exc:
        st.error(f"The API returned an unexpected response: {exc}")
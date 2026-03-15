import streamlit as st
import pickle
import pandas as pd

model = pickle.load(open("heart_model.pkl","rb"))
columns = pickle.load(open("columns.pkl","rb"))

st.set_page_config(page_title="Heart Disease Predictor", layout="centered")

st.title(" Heart Disease Prediction System")

st.write("Enter patient details below")

age = st.slider("Age",20,80,40)
bp = st.slider("Resting Blood Pressure",80,200,120)
chol = st.slider("Cholesterol",100,600,200)
maxhr = st.slider("Max Heart Rate",60,220,150)
oldpeak = st.slider("Oldpeak",0.0,6.0,1.0)

sex = st.selectbox("Sex",["Female","Male"])

chest_pain = st.selectbox(
    "Chest Pain Type",
    ["ATA","NAP","TA","ASY"]
    )

fasting = st.selectbox(
    "Fasting Blood Sugar > 120",
    ["No","Yes"]
    )

exercise = st.selectbox(
    "Exercise Induced Angina",
    ["No","Yes"]
    )

st_slope = st.selectbox(
    "ST Slope",
    ["Flat","Up","Down"]
    )
if st.button("Predict Heart Disease"):

    df = pd.DataFrame(columns=columns)
    df.loc[0] = 0

    df['Age'] = age
    df['RestingBP'] = bp
    df['Cholesterol'] = chol
    df['MaxHR'] = maxhr
    df['Oldpeak'] = oldpeak

    if sex == "Male":
        df['Sex_M'] = 1
        
    if chest_pain == "ATA":
        df['ChestPainType_ATA'] = 1
        
    elif chest_pain == "NAP":
        df['ChestPainType_NAP'] = 1
        
    elif chest_pain == "TA":
        df['ChestPainType_TA'] = 1
        
    if fasting == "Yes":
        df['FastingBS'] = 1
        
    if exercise == "Yes":
        df['ExerciseAngina_Y'] = 1
        
    if st_slope == "Flat":
        df['ST_Slope_Flat'] = 1
        
    elif st_slope == "Up":
        df['ST_Slope_Up'] = 1
        
    prediction = model.predict(df)
    probability = model.predict_proba(df)
    st.subheader("Prediction Result")

    if prediction[0] == 1:
            st.error(" 🔴 High Risk of Heart Disease")
    else:
            st.success("✅ Low Risk of Heart Disease")
            
    risk_prob = probability[0][1] * 100

    if risk_prob < 50:
        risk_level = "Low Risk"
    else:
        risk_level = "High Risk"
        color = "red"
        
    st.markdown("## 🫀 Heart Disease Risk Assessment")

    st.markdown(
        f"""
        <div style="
            padding:20px;
            border-radius:15px;
            background-color:#f5f5f5;
            text-align:center;
            box-shadow:2px 2px 10px rgba(0,0,0,0.1);
        ">
            <h2 style="color:{color};">{risk_level}</h2>
            <h1>{risk_prob:.1f}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    if risk_prob < 50:
        st.success("Patient shows low probability of heart disease.")
    else:
        st.error("Patient shows high probability of heart disease. Medical consultation advised.")
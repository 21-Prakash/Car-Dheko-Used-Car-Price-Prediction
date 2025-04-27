import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('car_price_prediction_model.pkl')

st.title("🚗 Car Price Prediction App")

st.markdown("Fill in the car details below to predict the price:")

# Input fields for the user to enter car details

# OEM - Let's assume you used label encoding for 'oem' column during training.
oem = st.selectbox("OEM", ['Maruti', 'Ford', 'Tata', 'Hyundai', 'BMW', 'Audi', 'Toyota'])  # Add other OEMs if necessary

# Other inputs
model_year = st.slider("Model Year", 2000, 2025, 2018)
km_driven = st.number_input("Kilometers Driven", min_value=0, step=1000)
transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])

# Engine CC, Max Power, Mileage, Seats
engine_cc = st.number_input("Engine CC", min_value=500, step=100)
power_bhp = st.number_input("Max Power (BHP)", min_value=20, step=1)
mileage = st.number_input("Mileage (kmpl)", min_value=5.0, step=0.1)
seats = st.selectbox("Seats", [2, 4, 5, 6, 7])

# For fuel type, let's assume the user selects fuel type (encoded as ft_* in training)
fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'Electric', 'LPG'])

# For cities, if the car is located in certain cities, the user can choose them
city_chennai = st.checkbox("City - Chennai")
city_delhi = st.checkbox("City - Delhi")
city_hyderabad = st.checkbox("City - Hyderabad")
city_jaipur = st.checkbox("City - Jaipur")
city_kolkata = st.checkbox("City - Kolkata")

# Encode categorical variables as you did during training (e.g., 'transmission', 'fuel_type', and others)
transmission_encoded = 1 if transmission == 'Manual' else 0
fuel_type_encoded = {
    'Petrol': 0,
    'Diesel': 1,
    'Electric': 2,
    'LPG': 3
}.get(fuel_type, 0)  # Default to 0 if no matching fuel type

# Process the input into a DataFrame matching training format
input_data = pd.DataFrame([{
    'it': 0, 'bt': 0, 'km': km_driven, 'transmission': transmission_encoded, 'ownerno': 1, 
    'oem': 1, 'model': 1, 'modelyear': model_year, 'centralvariantid': 0, 'variantname': 1, 
    'overview_registration_year': model_year, 'specs_mileage_kmpl': mileage, 'specs_engine_cc': engine_cc, 
    'specs_max_power_bhp': power_bhp, 'specs_torque_nm': 120, 'specs_seats': seats, 'specs_wheel_size': 15.0,
    'overview_insurance_validity_2': 0, 'overview_insurance_validity_Comprehensive': 1, 
    'overview_insurance_validity_Not Available': 0, 'overview_insurance_validity_Third Party': 0, 
    'overview_insurance_validity_Third Party insurance': 0, 'overview_insurance_validity_Unknown': 0, 
    'overview_insurance_validity_Zero Dep': 0, 'ft_Diesel': 1 if fuel_type == 'Diesel' else 0, 
    'ft_Electric': 1 if fuel_type == 'Electric' else 0, 'ft_Lpg': 1 if fuel_type == 'LPG' else 0, 
    'ft_Petrol': 1 if fuel_type == 'Petrol' else 0, 'city_Chennai': 1 if city_chennai else 0, 
    'city_Delhi': 1 if city_delhi else 0, 'city_Hyderabad': 1 if city_hyderabad else 0, 
    'city_Jaipur': 1 if city_jaipur else 0, 'city_Kolkata': 1 if city_kolkata else 0
}])

# Ensure order is exactly the same as the model's training data columns
training_columns = [
    'it', 'bt', 'km', 'transmission', 'ownerno', 'oem', 'model', 'modelyear', 'centralvariantid', 
    'variantname', 'overview_registration_year', 'specs_mileage_kmpl', 'specs_engine_cc', 
    'specs_max_power_bhp', 'specs_torque_nm', 'specs_seats', 'specs_wheel_size', 
    'overview_insurance_validity_2', 'overview_insurance_validity_Comprehensive', 
    'overview_insurance_validity_Not Available', 'overview_insurance_validity_Third Party', 
    'overview_insurance_validity_Third Party insurance', 'overview_insurance_validity_Unknown', 
    'overview_insurance_validity_Zero Dep', 'ft_Diesel', 'ft_Electric', 'ft_Lpg', 'ft_Petrol', 
    'city_Chennai', 'city_Delhi', 'city_Hyderabad', 'city_Jaipur', 'city_Kolkata'
]

# Reorder the input data to match training columns
input_data = input_data[training_columns]

# Prediction
if st.button("Predict Price"):
    # Ensure input features match the order and encoding of training data
    prediction = model.predict(input_data)[0]
    st.success(f"Estimated Car Price: ₹ {prediction:,.0f}")
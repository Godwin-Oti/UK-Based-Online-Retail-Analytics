import streamlit as st
import pandas as pd
import joblib
import os

# Function to load model, scaler, label encoder, and dataset
@st.cache_resource
def load_model_and_data():
    # Check if all required files exist
    if not os.path.exists('random_forest_model.pkl') or not os.path.exists('scaler.pkl') or not os.path.exists('label_encoder.pkl') or not os.path.exists('online_retail_cleaned_no_cancellations.csv'):
        st.error("Required files (model/scaler/encoder/data) are missing! Please check the directory.")
        st.stop()
    
    # Load the trained model, scaler, label encoder, and data
    model = joblib.load('random_forest_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    data = pd.read_csv('online_retail_cleaned_no_cancellations.csv')  # Load your dataset here (or pre-extracted unique stock codes)
    return model, scaler, label_encoder, data

# Load resources
rf_model, scaler, label_encoder, data = load_model_and_data()

# Extract unique StockCodes
unique_stock_codes = data['StockCode'].unique()  # Replace 'StockCode' with your column name
unique_stock_codes.sort()  # Sort for better usability

# Title of the web app
st.title('Unit Price Prediction for Stock Items')
st.markdown("""
This application predicts the unit price of a stock item based on various factors such as the stock code, day of the week, hour of the day, and month of the year.
Please provide the necessary details below to get a prediction.
""")

# Create a dropdown to select a Stock Code
stock_code = st.selectbox('Select Stock Code', unique_stock_codes, help="Choose a valid stock code from the dataset.")

# Create other input fields for the user
invoice_weekday = st.selectbox(
    'Select Invoice Weekday',
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    help="Choose the day of the week for the invoice."
)
invoice_hour = st.slider('Select Invoice Hour', 0, 23, 15, help="Pick the hour of the day (0-23). Default is 3 PM.")
invoice_month = st.slider('Select Invoice Month', 1, 12, 11, help="Pick the invoice month. Default is November.")

# Mapping weekdays to integers (0=Monday, 6=Sunday)
weekday_mapping = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
}
invoice_weekday_int = weekday_mapping[invoice_weekday]

# When the user presses the button to predict
if st.button('Predict Unit Price'):
    # Encode the stock code
    try:
        stock_code_encoded = label_encoder.transform([stock_code])[0]
    except ValueError:
        st.error("Invalid Stock Code! Please try a valid one.")
        st.stop()

    # Create the input features (replace lagged values with actual user input if available)
    input_features = pd.DataFrame({
        'StockCode_Encoded': [stock_code_encoded],
        'Quantity': [0],  # Replace with actual input if available
        'InvoiceHour': [invoice_hour],
        'InvoiceWeekday': [invoice_weekday_int],
        'InvoiceMonth': [invoice_month],
        'Quantity_Lagged_Avg': [0],  # Replace with actual input if available
        'UnitPrice_Lagged_Avg': [0],  # Replace with actual input if available
        'Quantity_UnitPrice_Lagged_Avg': [0]  # Replace with actual input if available
    })

    # Scale the features
    scaled_features = scaler.transform(input_features[['Quantity', 'Quantity_Lagged_Avg', 'UnitPrice_Lagged_Avg']])
    input_features[['Quantity', 'Quantity_Lagged_Avg', 'UnitPrice_Lagged_Avg']] = scaled_features

    # Predict the unit price
    try:
        predicted_price = rf_model.predict(input_features)
        st.write(f"Predicted Unit Price for StockCode {stock_code} on {invoice_weekday} at {invoice_hour}:00 is: £{predicted_price[0]:.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {str(e)}")

# Additional section for file upload (optional)
st.sidebar.title("Upload Model Files (Optional)")
st.sidebar.markdown("If the required files are not found, you can upload them here.")
uploaded_model = st.sidebar.file_uploader("Upload Random Forest Model (.pkl)", type=["pkl"])
uploaded_scaler = st.sidebar.file_uploader("Upload Scaler (.pkl)", type=["pkl"])
uploaded_encoder = st.sidebar.file_uploader("Upload Label Encoder (.pkl)", type=["pkl"])

# Replace files with uploaded versions (if provided)
if uploaded_model:
    rf_model = joblib.load(uploaded_model)
    st.sidebar.success("Random Forest model uploaded successfully!")
if uploaded_scaler:
    scaler = joblib.load(uploaded_scaler)
    st.sidebar.success("Scaler uploaded successfully!")
if uploaded_encoder:
    label_encoder = joblib.load(uploaded_encoder)
    st.sidebar.success("Label encoder uploaded successfully!")

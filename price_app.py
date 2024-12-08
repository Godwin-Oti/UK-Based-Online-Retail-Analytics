import streamlit as st
import pandas as pd
import joblib
import os

# Caching for reusable resources
@st.cache_resource
def load_model_and_data():
    if not all(os.path.exists(file) for file in ['random_forest_model.pkl', 'scaler.pkl', 'label_encoder.pkl', 'online_retail_cleaned_no_cancellations.csv']):
        st.error("Some required files (model, scaler, encoder, or data) are missing! Please check the directory.")
        st.stop()

    # Load model, scaler, label encoder, and data
    model = joblib.load('random_forest_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    data = pd.read_csv('online_retail_cleaned_no_cancellations.csv')
    return model, scaler, label_encoder, data

# Function to create input features for prediction (using pre-existing lagged averages)
def create_input_features(stock_code, invoice_weekday, invoice_hour, invoice_month, data, label_encoder, scaler):
    try:
        stock_code_encoded = label_encoder.transform([stock_code])[0]
    except ValueError:
        st.error("Invalid Stock Code! Please select a valid one.")
        st.stop()

    # Extract stock-specific data
    stock_data = data[data['StockCode'] == stock_code]
    if stock_data.empty:
        st.error(f"No historical data available for Stock Code: {stock_code}.")
        st.stop()

    # Use pre-calculated lagged averages from the data
    quantity_lagged_avg = stock_data['Quantity_Lagged_Avg'].iloc[-1] if 'Quantity_Lagged_Avg' in stock_data.columns else 0
    unitprice_lagged_avg = stock_data['UnitPrice_Lagged_Avg'].iloc[-1] if 'UnitPrice_Lagged_Avg' in stock_data.columns else 0
    quantity_unitprice_interaction = quantity_lagged_avg * unitprice_lagged_avg

    # Mapping weekdays to integers (0=Monday, 6=Sunday)
    weekday_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    invoice_weekday_int = weekday_mapping[invoice_weekday]

    # Create input DataFrame
    input_features = pd.DataFrame({
        'StockCode_Encoded': [stock_code_encoded],
        'Quantity': [0],  # This could be an actual user input if you want to incorporate that
        'Hour': [invoice_hour],
        'Day': [invoice_weekday_int],
        'Month': [invoice_month],
        'Quantity_Lagged_Avg': [quantity_lagged_avg],
        'UnitPrice_Lagged_Avg': [unitprice_lagged_avg],
        'Quantity_UnitPrice_Lagged_Avg': [quantity_unitprice_interaction]
    })

    # Scale the features
    scaled_features = scaler.transform(input_features[['Quantity', 'Quantity_Lagged_Avg', 'UnitPrice_Lagged_Avg']])
    input_features[['Quantity', 'Quantity_Lagged_Avg', 'UnitPrice_Lagged_Avg']] = scaled_features

    return input_features

# Load resources
rf_model, scaler, label_encoder, data = load_model_and_data()
unique_stock_codes = sorted(data['StockCode'].unique())

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "About", "Predict Unit Price"])

# Navigation: Home
if app_mode == "Home":
    st.title("Welcome to the Unit Price Prediction App")
    st.image("Retail.jpg", use_container_width=True)
    st.markdown("""
        ### Overview
        This app predicts the unit price of stock items based on various factors, such as:
        - **Stock Code**: Identifier for the product.
        - **Day of the Week**: Weekday of the invoice.
        - **Hour of the Day**: Time of purchase.
        - **Month of the Year**: Seasonal variations.

        ### Features
        - Intuitive UI for predictions.
        - Dynamic computation of lagged averages.
        - Support for file uploads for model customization.

        Use the sidebar to navigate to the prediction tool or learn more about the app.
    """)

# Navigation: About
elif app_mode == "About":
    st.title("About This App")
    st.markdown("""
        This app was designed to help retailers dynamically predict the price of items based on historical data and specific features.
        
        #### How It Works
        - The app uses a trained **Random Forest Regressor** model.
        - Features are preprocessed with lagged averages and scaling.
        - Users can input details and get predictions on the fly.

        #### Technologies Used
        - **Streamlit**: For the interactive interface.
        - **Pandas**: Data manipulation.
        - **Scikit-learn**: Machine learning modeling.

        #### Author
        - [Godwin Oti](https://www.datascienceportfol.io/godwinotigo)
    """)

# Navigation: Predict Unit Price
elif app_mode == "Predict Unit Price":
    st.title("Unit Price Prediction")
    st.markdown("Provide the details below to predict the unit price of a stock item.")

    # User inputs
    stock_code = st.selectbox('Select Stock Code', unique_stock_codes, help="Choose a valid stock code.")
    invoice_weekday = st.selectbox('Select Invoice Weekday', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    invoice_hour = st.slider('Select Invoice Hour', 0, 23, 12, help="Hour of the invoice (0-23).")
    invoice_month = st.slider('Select Invoice Month', 1, 12, 11, help="Month of the invoice (1-12).")

    # Prediction button
    if st.button("Predict Unit Price"):
        input_features = create_input_features(stock_code, invoice_weekday, invoice_hour, invoice_month, data, label_encoder, scaler)

        try:
            predicted_price = rf_model.predict(input_features)
            st.success(f"Predicted Unit Price: £{predicted_price[0]:.2f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

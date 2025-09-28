import streamlit as st 
import pickle
st.title('Health Insurance Premium Prediction')
age = st.number_input("Enter your age", min_value=0, max_value=100, value=30, step=1)
st.write("Your age is:", age)
bmi = st.number_input("Enter your BMI", min_value=12.5, max_value=35.0, value=25.0, step=0.5)
st.write("Your BMI is:", bmi)
children = st.selectbox(
    "Childrens:",
    (0,1,2,3,4,5,6,7,8,9),
    index=None,
)

st.write("You selected:", children)
gender = st.selectbox(
    "Gender:",
    ("Male", "Female"),
    index=None,
    placeholder="Select your gender...",
)
st.write("You selected:", gender)

smoker = st.selectbox(
    "Do you smoke?",
    ("Yes", "No"),
    index=None,
    placeholder="Select...",
)

st.write("You selected:", smoker)


    
    # Load the model outside the button click to avoid reloading it every time
# This is more efficient
try:
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file not found. Please make sure 'model.pkl' is in the correct directory.")
    model = None # Set model to None if it can't be loaded

if st.button('Predict Premium', type="primary"):
    # First, validate that all inputs have been selected
    if gender is None or smoker is None or children is None:
        st.error("🚨 Oops! Please make sure to select a value for all fields.")
    elif model is None:
        st.error("Model is not loaded, cannot make a prediction.")
    else:
        # Process the inputs for the model
        gender_numeric = 0 if gender == 'Male' else 1
        smoker_numeric = 1 if smoker == 'Yes' else 0

        # Create the input array for the model
        prediction_input = [[age, bmi, children, gender_numeric, smoker_numeric]]
        
        # Get the prediction
        predicted_premium = model.predict(prediction_input)[0]

        # --- Display the results beautifully ---
        
        st.snow() # A little celebration for the result!
        
        st.header('Prediction Result', divider='rainbow')

        st.metric(
            label="**Your Estimated Annual Premium**",
            value=f"$ {predicted_premium:,.2f}",
            help="This value is an estimate based on the provided data."
        )

        st.markdown("---")

        st.subheader("How Your Details Impact the Premium:")
        
        # Use columns for a clean layout
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### Your Inputs")
            st.write(f"**Age:** {age} years")
            st.write(f"**BMI:** {bmi}")
            st.write(f"**Children:** {children}")
        
        with col2:
            st.write("#### Lifestyle Factors")
            st.write(f"**Gender:** {gender}")
            st.write(f"**Smoker:** {smoker}")

        st.markdown("---")

        # Add a friendly disclaimer
        st.info(
            "**Disclaimer:** This is a machine learning-based prediction and should be considered an estimate. "
            "Actual insurance premiums can vary based on more detailed assessments by insurance providers.",
            icon="ℹ️"

        )


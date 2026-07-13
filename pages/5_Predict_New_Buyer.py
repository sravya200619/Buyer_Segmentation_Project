import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Predict Buyer Segment",
    page_icon="🔍",
    layout="wide"
)

# ==========================================================
# Load Models & Reference Data Structure
# ==========================================================

@st.cache_resource
def load_ml_assets():
    kmeans = joblib.load("models/kmeans_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return kmeans, scaler

@st.cache_data
def load_reference_columns():
    # Load the base file to capture the categorical variable options and exact training shape
    df_raw = pd.read_csv("data/Buyer_Segmentation_Final.csv")
    df_raw.columns = df_raw.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Drop columns that were NOT used as training features (like client ID, target labels)
    features_raw = df_raw.drop(columns=["client_id", "buyer_segment"], errors="ignore")
    
    # Mirror the exact one-hot encoding procedure used during model compilation
    features_encoded = pd.get_dummies(features_raw)
    return features_encoded.columns.tolist(), df_raw

try:
    kmeans, scaler = load_ml_assets()
    expected_columns, raw_df = load_reference_columns()
except Exception as e:
    st.error(f"Failed to load critical pipeline files: {e}")
    st.stop()

# ==========================================================
# Title
# ==========================================================

st.title("🔍 AI Buyer Segment Prediction")
st.markdown("""
Predict the most likely buyer segment using the trained Machine Learning model.
Enter the buyer information below and click **Predict Buyer Segment**.
""")
st.markdown("---")

# ==========================================================
# Buyer Information
# ==========================================================

st.subheader("📝 Buyer Information")
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 80, 30)
    gender = st.selectbox("Gender", sorted(raw_df["gender"].dropna().unique()) if "gender" in raw_df else ["Male", "Female"])
    client_type = st.selectbox("Client Type", sorted(raw_df["client_type"].dropna().unique()) if "client_type" in raw_df else ["Individual", "Corporate"])
    loan = st.selectbox("Loan Applied", sorted(raw_df["loan_applied"].dropna().unique()) if "loan_applied" in raw_df else ["Yes", "No"])

with col2:
    satisfaction = st.slider("Customer Satisfaction", 1.0, 5.0, 3.5)
    acquisition = st.selectbox("Acquisition Purpose", sorted(raw_df["acquisition_purpose"].dropna().unique()) if "acquisition_purpose" in raw_df else ["Investment", "Personal Use"])
    region = st.selectbox("Region", sorted(raw_df["region"].dropna().unique()))
    country = st.selectbox("Country", sorted(raw_df["country"].dropna().unique()))

st.markdown("---")

# ==========================================================
# Buyer Summary
# ==========================================================

st.subheader("📋 Buyer Profile")
summary = pd.DataFrame({
    "Feature": ["Age", "Gender", "Client Type", "Loan Applied", "Acquisition Purpose", "Region", "Country", "Satisfaction"],
    "Value": [age, gender, client_type, loan, acquisition, region, country, satisfaction]
})
st.dataframe(summary, use_container_width=True)
st.markdown("---")

# ==========================================================
# Prediction Engine
# ==========================================================

if st.button("🚀 Predict Buyer Segment"):
    try:
        # 1. Create a single row DataFrame matching raw user selections
        input_data = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "client_type": client_type,
            "loan_applied": loan,
            "acquisition_purpose": acquisition,
            "region": region,
            "country": country,
            "satisfaction_score": satisfaction
        }])
        
        # 2. One-hot encode the current single runtime observation
        input_encoded = pd.get_dummies(input_data)
        
        # 3. Align features: Create a blank vector structure matching the 3,584 training columns
        full_feature_df = pd.DataFrame(0, index=[0], columns=expected_columns)
        
        # 4. Fill in values for features present in our runtime single record match
        for col in input_encoded.columns:
            if col in full_feature_df.columns:
                full_feature_df[col] = input_encoded[col].values
                
        # 5. Extract matrix array values in the mathematically correct dimensions
        feature_vector = full_feature_df.values

        # 6. Apply preprocessing scaler and execute cluster tracking assignments
        scaled = scaler.transform(feature_vector)
        cluster = int(kmeans.predict(scaled)[0])

        cluster_names = {
            0: "🌍 Global Investors",
            1: "🏠 First-Time Buyers",
            2: "🏢 Corporate Buyers",
            3: "💎 Luxury Investors"
        }

        buyer_type = cluster_names.get(cluster, f"Cluster {cluster}")
        st.success(f"Predicted Segment: **{buyer_type}**")
        st.markdown("---")

        # Business Strategies Block
        st.subheader("📊 Business Recommendation")
        if buyer_type == "🌍 Global Investors":
            st.success("✅ Premium Investment Properties\n\n✅ International Projects\n\n✅ Luxury Apartments\n\n✅ Long-Term Investment Plans")
        elif buyer_type == "🏠 First-Time Buyers":
            st.info("✅ Affordable Housing\n\n✅ Home Loan Offers\n\n✅ EMI Assistance\n\n✅ Starter Homes")
        elif buyer_type == "🏢 Corporate Buyers":
            st.warning("✅ Commercial Buildings\n\n✅ Office Spaces\n\n✅ Bulk Purchase Offers\n\n✅ Corporate Discounts")
        elif buyer_type == "💎 Luxury Investors":
            st.error("✅ Luxury Villas\n\n✅ Premium Apartments\n\n✅ Exclusive Membership\n\n✅ VIP Investment Services")

        st.markdown("---")
        st.subheader("📌 Suggested Marketing Strategy")
        st.write("""
        - Personalized Email Campaign
        - Property Recommendation Engine
        - Dedicated Relationship Manager
        - Region-Based Property Promotions
        - AI-Powered Customer Engagement
        """)

        # Session Recording Loop
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "Age": age,
            "Client Type": client_type,
            "Country": country,
            "Prediction": buyer_type
        })

    except Exception as e:
        st.error(f"Prediction matrix processing failed: {e}")

st.markdown("---")

# ==========================================================
# Prediction History
# ==========================================================

if "history" in st.session_state and st.session_state.history:
    st.subheader("📜 Prediction History")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)
    st.markdown("---")
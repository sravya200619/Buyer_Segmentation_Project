import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Predict Buyer Segment",
    page_icon="🔍",
    layout="wide"
)

# ==========================================================
# Title
# ==========================================================

st.title("🔍 AI Buyer Segment Prediction")

st.markdown("""
Predict the buyer segment using the trained Machine Learning clustering model.
Provide buyer information below and click **Predict Segment**.
""")

st.markdown("---")

# ==========================================================
# Load Models
# ==========================================================

MODEL_PATH = "models/kmeans_model.pkl"
SCALER_PATH = "models/scaler.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("❌ kmeans_model.pkl not found inside models folder.")
    st.stop()

if not os.path.exists(SCALER_PATH):
    st.error("❌ scaler.pkl not found inside models folder.")
    st.stop()

kmeans = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ==========================================================
# User Inputs
# ==========================================================

st.subheader("Buyer Details")

col1, col2 = st.columns(2)

with col1:

    age = st.slider(
        "Age",
        18,
        80,
        30
    )

    satisfaction = st.slider(
        "Satisfaction Score",
        1.0,
        5.0,
        3.5
    )

with col2:

    loan = st.selectbox(
        "Loan Applied",
        ["Yes", "No"]
    )

    client_type = st.selectbox(
        "Client Type",
        ["Individual", "Corporate"]
    )

# ==========================================================
# Encoding
# ==========================================================

loan = 1 if loan == "Yes" else 0

client = 1 if client_type == "Corporate" else 0

# ==========================================================
# Feature Vector
# ==========================================================

features = np.array([
    [
        age,
        satisfaction,
        loan,
        client
    ]
])

# ==========================================================
# Prediction
# ==========================================================

st.markdown("---")

if st.button("🚀 Predict Buyer Segment"):

    try:

        scaled = scaler.transform(features)

        cluster = int(kmeans.predict(scaled)[0])

        segment_names = {
            0: "🏡 First-Time Buyers",
            1: "🌍 Global Investors",
            2: "🏢 Corporate Buyers",
            3: "💎 Luxury Investors"
        }

        segment = segment_names.get(cluster, f"Cluster {cluster}")

        st.success(f"Predicted Segment : **{segment}**")

        st.markdown("---")

        st.subheader("📈 Recommended Business Strategy")

        if cluster == 0:

            st.info("""
### First-Time Buyers

✔ Affordable Apartments

✔ Home Loan Assistance

✔ EMI Offers

✔ First Buyer Discounts

✔ Government Housing Schemes
""")

        elif cluster == 1:

            st.info("""
### Global Investors

✔ Premium Villas

✔ Rental Investments

✔ International Investment Support

✔ Property Portfolio Management
""")

        elif cluster == 2:

            st.info("""
### Corporate Buyers

✔ Commercial Buildings

✔ Office Spaces

✔ Bulk Purchase Discounts

✔ Enterprise Investment Plans
""")

        elif cluster == 3:

            st.info("""
### Luxury Investors

✔ Luxury Villas

✔ Penthouses

✔ Premium Concierge Services

✔ Exclusive Investment Opportunities
""")

        st.balloons()

    except Exception as e:

        st.error("Prediction Failed")

        st.code(str(e))

# ==========================================================
# Model Information
# ==========================================================

st.markdown("---")

st.subheader("🤖 Model Information")

st.write("Algorithm : **K-Means Clustering**")

st.write("Scaling : **StandardScaler**")

st.write("Prediction Type : **Buyer Segmentation**")

st.markdown("---")

st.warning("""
**Important**

This page assumes the K-Means model was trained using **exactly these four features**:

- Age
- Satisfaction Score
- Loan Applied
- Client Type

If your training notebook used One-Hot Encoding or additional features such as:

- Country
- Region
- Acquisition Purpose
- Referral Channel

then the prediction feature vector must be modified to match the training data exactly.
""")

st.success("✅ Buyer Prediction Module Loaded Successfully.")
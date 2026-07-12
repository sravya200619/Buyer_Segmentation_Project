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
# Load Models
# ==========================================================

kmeans = joblib.load("models/kmeans_model.pkl")
scaler = joblib.load("models/scaler.pkl")

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

col1,col2 = st.columns(2)

with col1:

    age = st.slider(
        "Age",
        18,
        80,
        30
    )

    gender = st.selectbox(
        "Gender",
        ["Male","Female"]
    )

    client_type = st.selectbox(
        "Client Type",
        ["Individual","Corporate"]
    )

    loan = st.selectbox(
        "Loan Applied",
        ["Yes","No"]
    )

with col2:

    satisfaction = st.slider(
        "Customer Satisfaction",
        1.0,
        5.0,
        3.5
    )

    acquisition = st.selectbox(
        "Acquisition Purpose",
        ["Investment","Personal Use"]
    )

    region = st.text_input(
        "Region",
        "North"
    )

    country = st.text_input(
        "Country",
        "India"
    )

st.markdown("---")

# ==========================================================
# Buyer Summary
# ==========================================================

st.subheader("📋 Buyer Profile")

summary = pd.DataFrame({
    "Feature":[
        "Age",
        "Gender",
        "Client Type",
        "Loan Applied",
        "Acquisition Purpose",
        "Region",
        "Country",
        "Satisfaction"
    ],
    "Value":[
        age,
        gender,
        client_type,
        loan,
        acquisition,
        region,
        country,
        satisfaction
    ]
})

st.dataframe(summary, use_container_width=True)

st.markdown("---")

# ==========================================================
# Prediction
# ==========================================================

if st.button("🚀 Predict Buyer Segment"):

    try:

        # ------------------------------------------------------
        # IMPORTANT
        # Replace this feature vector with the EXACT
        # encoded feature order used during model training.
        # ------------------------------------------------------

        feature_vector = np.array([
            [
                age,
                satisfaction,
                1 if loan=="Yes" else 0
            ]
        ])

        scaled = scaler.transform(feature_vector)

        cluster = int(kmeans.predict(scaled)[0])

        cluster_names = {
            0: "🌍 Global Investors",
            1: "🏠 First-Time Buyers",
            2: "🏢 Corporate Buyers",
            3: "💎 Luxury Investors"
        }

        buyer_type = cluster_names.get(
            cluster,
            f"Cluster {cluster}"
        )

        st.success(f"Predicted Segment: **{buyer_type}**")

        st.markdown("---")

        st.subheader("📊 Business Recommendation")

        if buyer_type == "🌍 Global Investors":

            st.success("""
✅ Premium Investment Properties

✅ International Projects

✅ Luxury Apartments

✅ Long-Term Investment Plans
""")

        elif buyer_type == "🏠 First-Time Buyers":

            st.info("""
✅ Affordable Housing

✅ Home Loan Offers

✅ EMI Assistance

✅ Starter Homes
""")

        elif buyer_type == "🏢 Corporate Buyers":

            st.warning("""
✅ Commercial Buildings

✅ Office Spaces

✅ Bulk Purchase Offers

✅ Corporate Discounts
""")

        elif buyer_type == "💎 Luxury Investors":

            st.error("""
✅ Luxury Villas

✅ Premium Apartments

✅ Exclusive Membership

✅ VIP Investment Services
""")

        st.markdown("---")

        st.subheader("📌 Suggested Marketing Strategy")

        st.write("""
- Personalized Email Campaign
- Property Recommendation Engine
- Dedicated Relationship Manager
- Region-Based Property Promotions
- AI-Powered Customer Engagement
""")

        # ==================================================
        # Session History
        # ==================================================

        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "Age": age,
            "Client Type": client_type,
            "Country": country,
            "Prediction": buyer_type
        })

    except Exception as e:

        st.error(f"Prediction failed: {e}")

st.markdown("---")

# ==========================================================
# Prediction History
# ==========================================================

if "history" in st.session_state and st.session_state.history:

    st.subheader("📜 Prediction History")

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        history_df,
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# Information Box
# ==========================================================

st.info("""
**Important:** This prediction page assumes the same preprocessing pipeline
used during training. If your K-Means model was trained with one-hot encoded
features, update the feature vector to include those encoded columns in the
exact same order before calling `scaler.transform()` and `kmeans.predict()`.
""")
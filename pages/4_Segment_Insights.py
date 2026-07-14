import streamlit as st
import pandas as pd

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Segment Insights",
    page_icon="💡",
    layout="wide"
)

# =====================================================
# Load Dataset
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/Buyer_Segmentation_Final.csv")

df = load_data()

# =====================================================
# Standardize Column Names
# =====================================================

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# =====================================================
# Required Columns
# =====================================================

required = [
    "buyer_segment",
    "age",
    "satisfaction_score",
    "loan_applied",
    "client_type",
    "country",
    "region",
    "acquisition_purpose"
]

missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing Columns: {missing}")
    st.write("Available Columns:")
    st.write(df.columns.tolist())
    st.stop()

# =====================================================
# Title
# =====================================================

st.title("💡 Buyer Segment Insights")

st.markdown("""
Explore detailed statistics and business insights for each buyer segment.
""")

st.markdown("---")

# =====================================================
# Sidebar Filter
# =====================================================

segment = st.sidebar.selectbox(
    "Select Buyer Segment",
    sorted(df["buyer_segment"].unique())
)

filtered = df[df["buyer_segment"] == segment]

# =====================================================
# KPI Cards
# =====================================================

st.subheader("📊 Segment KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Buyers",
        len(filtered)
    )

with col2:
    st.metric(
        "Average Age",
        round(filtered["age"].mean(), 1)
    )

with col3:
    st.metric(
        "Avg Satisfaction",
        round(filtered["satisfaction_score"].mean(), 2)
    )

with col4:
    loan_rate = (
        (filtered["loan_applied"] == "Yes").mean() * 100
        if filtered["loan_applied"].dtype == object
        else filtered["loan_applied"].mean() * 100
    )

    st.metric(
        "Loan Applicants",
        f"{loan_rate:.1f}%"
    )

st.markdown("---")

# =====================================================
# Segment Statistics
# =====================================================

st.subheader("📋 Statistical Summary")

summary = filtered.describe(include="all").transpose()

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# Country Distribution
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌍 Top Countries")

    country_df = (
        filtered["country"]
        .value_counts()
        .reset_index()
    )

    country_df.columns = ["Country", "Buyers"]

    st.dataframe(
        country_df,
        use_container_width=True
    )

with col2:

    st.subheader("📍 Top Regions")

    region_df = (
        filtered["region"]
        .value_counts()
        .reset_index()
    )

    region_df.columns = ["Region", "Buyers"]

    st.dataframe(
        region_df,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# Client Type
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏢 Client Types")

    client_df = (
        filtered["client_type"]
        .value_counts()
        .reset_index()
    )

    client_df.columns = ["Client Type", "Count"]

    st.dataframe(
        client_df,
        use_container_width=True
    )

with col2:

    st.subheader("🏠 Acquisition Purpose")

    purpose_df = (
        filtered["acquisition_purpose"]
        .value_counts()
        .reset_index()
    )

    purpose_df.columns = ["Purpose", "Count"]

    st.dataframe(
        purpose_df,
        use_container_width=True
    )

st.markdown("---")

# =====================================================
# Business Insights
# =====================================================

st.subheader("💼 Business Insights")

avg_age = filtered["age"].mean()
avg_sat = filtered["satisfaction_score"].mean()

if avg_age < 35:
    age_text = "This segment mainly consists of younger buyers."
elif avg_age < 50:
    age_text = "This segment is dominated by middle-aged buyers."
else:
    age_text = "This segment mostly includes senior investors."

if avg_sat >= 4:
    sat_text = "Customer satisfaction is very high."
elif avg_sat >= 3:
    sat_text = "Customer satisfaction is moderate."
else:
    sat_text = "Customer satisfaction needs improvement."

st.success(f"""
### Segment Analysis

• {age_text}

• {sat_text}

• Marketing campaigns can be personalized for this buyer segment.

• Property recommendations should align with this group's investment goals.

• Financing strategies can improve customer acquisition.

• Geographic targeting can further increase conversion rates.
""")

st.markdown("---")

# =====================================================
# Download Data
# =====================================================

csv = filtered.to_csv(index=False)

st.download_button(
    label="📥 Download Segment Data",
    data=csv,
    file_name=f"{segment}_buyers.csv",
    mime="text/csv"
)

st.markdown("---")

st.success("✅ Segment Insights Generated Successfully.")
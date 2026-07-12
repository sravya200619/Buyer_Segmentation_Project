import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Investor Behaviour Dashboard",
    page_icon="📈",
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
# Title
# =====================================================

st.title("📈 Investor Behaviour Dashboard")

st.markdown("""
Explore how different buyer segments behave based on their
investment purpose, financing choices, demographics, and customer satisfaction.
""")

st.markdown("---")

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.header("🔎 Filters")

purpose = st.sidebar.multiselect(
    "Acquisition Purpose",
    sorted(df["acquisition_purpose"].unique()),
    default=sorted(df["acquisition_purpose"].unique())
)

segment = st.sidebar.multiselect(
    "Buyer Segment",
    sorted(df["Buyer_Segment"].unique()),
    default=sorted(df["Buyer_Segment"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

filtered = df[
    (df["acquisition_purpose"].isin(purpose)) &
    (df["Buyer_Segment"].isin(segment)) &
    (df["region"].isin(region))
]

# =====================================================
# KPI Cards
# =====================================================

st.subheader("📊 Investor KPIs")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Total Investors",
        len(filtered)
    )

with col2:
    st.metric(
        "Average Age",
        round(filtered["Age"].mean(),1)
    )

with col3:
    st.metric(
        "Average Satisfaction",
        round(filtered["satisfaction_score"].mean(),2)
    )

with col4:
    st.metric(
        "Countries",
        filtered["country"].nunique()
    )

st.markdown("---")

# =====================================================
# Loan Behaviour
# =====================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("🏦 Loan Behaviour")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="Buyer_Segment",
        hue="loan_applied",
        palette="Set2",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

with col2:

    st.subheader("🏠 Acquisition Purpose")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="Buyer_Segment",
        hue="client_type",
        palette="Set3",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

st.markdown("---")

# =====================================================
# Satisfaction & Age
# =====================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("😊 Satisfaction Score")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.boxplot(
        data=filtered,
        x="Buyer_Segment",
        y="satisfaction_score",
        palette="viridis",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

with col2:

    st.subheader("👥 Age Distribution")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.histplot(
        filtered["Age"],
        bins=20,
        kde=True,
        color="skyblue",
        ax=ax
    )

    st.pyplot(fig)

st.markdown("---")

# =====================================================
# Geographic Distribution
# =====================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("🌍 Region-wise Investors")

    fig,ax = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=filtered,
        x="region",
        palette="Set1",
        ax=ax
    )

    plt.xticks(rotation=30)

    st.pyplot(fig)

with col2:

    st.subheader("🌎 Top Countries")

    country_count = filtered["country"].value_counts().head(10)

    fig,ax = plt.subplots(figsize=(8,5))

    country_count.plot(
        kind="bar",
        ax=ax
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

st.markdown("---")

# =====================================================
# Referral Channel
# =====================================================

st.subheader("📢 Referral Channel")

fig,ax = plt.subplots(figsize=(10,5))

sns.countplot(
    data=filtered,
    x="referral_channel",
    hue="Buyer_Segment",
    palette="tab10",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

# =====================================================
# Segment Summary
# =====================================================

st.subheader("📋 Segment Summary")

summary = filtered.groupby("Buyer_Segment").agg(

    Total_Buyers=("client_id","count"),

    Average_Age=("Age","mean"),

    Average_Satisfaction=("satisfaction_score","mean")

).round(2)

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# Raw Data
# =====================================================

with st.expander("📄 View Investor Dataset"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

# =====================================================
# Download Button
# =====================================================

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Investor Data",
    csv,
    file_name="Investor_Behaviour.csv",
    mime="text/csv"
)

st.markdown("---")

st.success("Investor Behaviour Analysis Completed Successfully.")
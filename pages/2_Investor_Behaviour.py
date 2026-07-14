import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Investor Behaviour",
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
# Recover Acquisition Purpose (One-Hot Encoded)
# =====================================================

purpose_cols = [c for c in df.columns if c.startswith("acquisition_purpose_")]

if purpose_cols:
    df["Acquisition_Purpose"] = (
        df[purpose_cols]
        .idxmax(axis=1)
        .str.replace("acquisition_purpose_", "", regex=False)
    )
else:
    df["Acquisition_Purpose"] = "Unknown"

# =====================================================
# Recover Client Type (if encoded)
# =====================================================

if "client_type" not in df.columns:
    client_cols = [c for c in df.columns if c.startswith("client_type_")]

    if client_cols:
        df["client_type"] = (
            df[client_cols]
            .idxmax(axis=1)
            .str.replace("client_type_", "", regex=False)
        )
    else:
        df["client_type"] = "Unknown"

# =====================================================
# Title
# =====================================================

st.title("📈 Investor Behaviour Dashboard")

st.markdown("""
Analyze investment behaviour across buyer segments, financing preferences,
and acquisition purposes using AI-driven clustering.
""")

st.divider()

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.header("Filters")

purpose = st.sidebar.selectbox(
    "Acquisition Purpose",
    sorted(df["Acquisition_Purpose"].unique())
)

client = st.sidebar.multiselect(
    "Client Type",
    sorted(df["client_type"].unique()),
    default=sorted(df["client_type"].unique())
)

filtered = df[
    (df["Acquisition_Purpose"] == purpose) &
    (df["client_type"].isin(client))
]

# =====================================================
# KPI Cards
# =====================================================

st.subheader("Investment Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Investors", len(filtered))

c2.metric(
    "Buyer Segments",
    filtered["Buyer_Segment"].nunique()
)

c3.metric(
    "Average Age",
    round(filtered["Age"].mean(), 1)
)

c4.metric(
    "Average Satisfaction",
    round(filtered["satisfaction_score"].mean(), 2)
)

st.divider()

# =====================================================
# Segment vs Loan Behaviour
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("Buyer Segment vs Loan")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.countplot(
        data=filtered,
        x="Buyer_Segment",
        hue="loan_applied",
        palette="Set2",
        ax=ax
    )

    plt.xticks(rotation=15)

    st.pyplot(fig)

with right:

    st.subheader("Loan Distribution")

    fig, ax = plt.subplots(figsize=(6,6))

    filtered["loan_applied"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

st.divider()

# =====================================================
# Satisfaction Analysis
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("Satisfaction by Segment")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.boxplot(
        data=filtered,
        x="Buyer_Segment",
        y="satisfaction_score",
        palette="Set3",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

with right:

    st.subheader("Age Distribution")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.histplot(
        filtered["Age"],
        kde=True,
        bins=20,
        color="orange",
        ax=ax
    )

    st.pyplot(fig)

st.divider()

# =====================================================
# Client Type Distribution
# =====================================================

st.subheader("Client Type Distribution")

fig, ax = plt.subplots(figsize=(8,5))

sns.countplot(
    data=filtered,
    x="client_type",
    hue="Buyer_Segment",
    palette="viridis",
    ax=ax
)

plt.xticks(rotation=15)

st.pyplot(fig)

st.divider()

# =====================================================
# Summary Table
# =====================================================

st.subheader("Investor Behaviour Summary")

summary = filtered.groupby("Buyer_Segment").agg(
    Total_Investors=("Buyer_Segment", "count"),
    Average_Age=("Age", "mean"),
    Average_Satisfaction=("satisfaction_score", "mean")
).round(2)

st.dataframe(summary, use_container_width=True)

st.divider()

# =====================================================
# Raw Data
# =====================================================

with st.expander("📄 View Filtered Dataset"):
    st.dataframe(filtered, use_container_width=True)

# =====================================================
# Download Button
# =====================================================

st.download_button(
    "📥 Download Investor Data",
    filtered.to_csv(index=False),
    file_name="Investor_Behaviour.csv",
    mime="text/csv"
)

st.success("✅ Investor Behaviour Dashboard Loaded Successfully.")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Buyer Segmentation",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/Buyer_Segmentation_Final.csv")

df = load_data()

# ==========================================================
# Recover Country & Region from One-Hot Encoding
# ==========================================================

country_cols = [c for c in df.columns if c.startswith("country_")]
region_cols = [c for c in df.columns if c.startswith("region_")]

if country_cols:
    df["Country"] = (
        df[country_cols]
        .idxmax(axis=1)
        .str.replace("country_", "", regex=False)
    )
else:
    df["Country"] = "Unknown"

if region_cols:
    df["Region"] = (
        df[region_cols]
        .idxmax(axis=1)
        .str.replace("region_", "", regex=False)
    )
else:
    df["Region"] = "Unknown"

# ==========================================================
# TITLE
# ==========================================================

st.title("🏠 Buyer Segmentation Dashboard")

st.markdown("""
Analyze different buyer groups identified using **Machine Learning K-Means Clustering**.
Use the filters on the left to explore buyer demographics.
""")

st.divider()

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

client_type = st.sidebar.multiselect(
    "Client Type",
    sorted(df["client_type"].unique()),
    default=sorted(df["client_type"].unique())
)

filtered = df[
    (df["Country"].isin(country)) &
    (df["Region"].isin(region)) &
    (df["client_type"].isin(client_type))
]

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Buyers", len(filtered))

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

# ==========================================================
# SEGMENT DISTRIBUTION
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("Buyer Segment Distribution")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="Buyer_Segment",
        palette="Set2",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

with right:

    st.subheader("Buyer Segment Share")

    fig, ax = plt.subplots(figsize=(6,6))

    filtered["Buyer_Segment"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

st.divider()

# ==========================================================
# AGE & SATISFACTION
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("Age Distribution")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.histplot(
        filtered["Age"],
        bins=20,
        kde=True,
        color="skyblue",
        ax=ax
    )

    st.pyplot(fig)

with right:

    st.subheader("Satisfaction Score")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.boxplot(
        data=filtered,
        x="Buyer_Segment",
        y="satisfaction_score",
        palette="Set3",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

st.divider()

# ==========================================================
# CLIENT TYPE & LOAN
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("Client Type")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="client_type",
        hue="Buyer_Segment",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

with right:

    st.subheader("Loan Applied")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="loan_applied",
        hue="Buyer_Segment",
        ax=ax
    )

    st.pyplot(fig)

st.divider()

# ==========================================================
# SUMMARY TABLE
# ==========================================================

st.subheader("Buyer Segment Summary")

summary = filtered.groupby("Buyer_Segment").agg(
    Total_Buyers=("Buyer_Segment","count"),
    Average_Age=("Age","mean"),
    Average_Satisfaction=("satisfaction_score","mean")
).round(2)

st.dataframe(summary, use_container_width=True)

st.divider()

# ==========================================================
# RAW DATA
# ==========================================================

with st.expander("View Dataset"):

    st.dataframe(filtered, use_container_width=True)

# ==========================================================
# DOWNLOAD
# ==========================================================

st.download_button(
    "Download Filtered Dataset",
    filtered.to_csv(index=False),
    "Buyer_Segmentation.csv",
    "text/csv"
)

st.success("Buyer Segmentation Dashboard Loaded Successfully.")
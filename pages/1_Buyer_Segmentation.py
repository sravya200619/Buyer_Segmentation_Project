import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Buyer Segmentation",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/Buyer_Segmentation_Final.csv")

df = load_data()

# -------------------------------------------------------
# Title
# -------------------------------------------------------

st.title("📊 Buyer Segmentation Dashboard")
st.markdown(
    "Analyze customer groups identified using **K-Means Clustering** and explore buyer demographics."
)

st.markdown("---")

# -------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------

st.sidebar.header("🔍 Filters")

country = st.sidebar.multiselect(
    "Country",
    sorted(df["country"].unique()),
    default=sorted(df["country"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

client_type = st.sidebar.multiselect(
    "Client Type",
    sorted(df["client_type"].unique()),
    default=sorted(df["client_type"].unique())
)

filtered = df[
    (df["country"].isin(country)) &
    (df["region"].isin(region)) &
    (df["client_type"].isin(client_type))
]

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

st.subheader("📈 Key Performance Indicators")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Total Buyers",
        len(filtered)
    )

with col2:
    st.metric(
        "Buyer Segments",
        filtered["Buyer_Segment"].nunique()
    )

with col3:
    st.metric(
        "Average Age",
        round(filtered["Age"].mean(),1)
    )

with col4:
    st.metric(
        "Average Satisfaction",
        round(filtered["satisfaction_score"].mean(),2)
    )

st.markdown("---")

# -------------------------------------------------------
# Buyer Segment Charts
# -------------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("Buyer Segment Distribution")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="Buyer_Segment",
        palette="Set2",
        ax=ax
    )

    plt.xticks(rotation=15)

    st.pyplot(fig)

with col2:

    st.subheader("Buyer Segment Share")

    fig,ax = plt.subplots(figsize=(6,6))

    filtered["Buyer_Segment"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)

st.markdown("---")

# -------------------------------------------------------
# Age Distribution
# -------------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("Age Distribution")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.histplot(
        filtered["Age"],
        kde=True,
        bins=20,
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("Satisfaction Score")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.boxplot(
        data=filtered,
        x="Buyer_Segment",
        y="satisfaction_score",
        palette="Set3",
        ax=ax
    )

    plt.xticks(rotation=15)

    st.pyplot(fig)

st.markdown("---")

# -------------------------------------------------------
# Client Type
# -------------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("Client Type")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="client_type",
        hue="Buyer_Segment",
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("Loan Behaviour")

    fig,ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="loan_applied",
        hue="Buyer_Segment",
        ax=ax
    )

    st.pyplot(fig)

st.markdown("---")

# -------------------------------------------------------
# Buyer Segment Summary
# -------------------------------------------------------

st.subheader("📋 Buyer Segment Summary")

summary = filtered.groupby("Buyer_Segment").agg(
    Total_Buyers=("client_id","count"),
    Average_Age=("Age","mean"),
    Average_Satisfaction=("satisfaction_score","mean")
).round(2)

st.dataframe(
    summary,
    use_container_width=True
)

# -------------------------------------------------------
# Raw Data
# -------------------------------------------------------

with st.expander("📄 View Complete Dataset"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

# -------------------------------------------------------
# Download Button
# -------------------------------------------------------

csv = filtered.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="Buyer_Segmentation.csv",
    mime="text/csv"
)

st.markdown("---")

st.success("Buyer Segmentation analysis completed successfully.")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Geographic Buyer Analysis",
    page_icon="🌍",
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
# Recover Country and Region from One-Hot Encoding
# =====================================================

country_cols = [col for col in df.columns if col.startswith("country_")]
region_cols = [col for col in df.columns if col.startswith("region_")]

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

# =====================================================
# Title
# =====================================================

st.title("🌍 Geographic Buyer Analysis")

st.markdown("""
Analyze buyer distribution across different **countries and regions**.
This dashboard helps identify regional investment opportunities and customer concentration.
""")

st.markdown("---")

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.header("🔍 Geographic Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_country = st.sidebar.multiselect(
    "Select Country",
    sorted(df["Country"].unique()),
    default=sorted(df["Country"].unique())
)

filtered = df[
    (df["Region"].isin(selected_region)) &
    (df["Country"].isin(selected_country))
]

# =====================================================
# KPI Cards
# =====================================================

st.subheader("📊 Geographic Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Buyers",
    len(filtered)
)

col2.metric(
    "Countries",
    filtered["Country"].nunique()
)

col3.metric(
    "Regions",
    filtered["Region"].nunique()
)

col4.metric(
    "Avg Satisfaction",
    round(filtered["satisfaction_score"].mean(), 2)
)

st.markdown("---")

# =====================================================
# Country Distribution
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("🌎 Buyers by Country")

    fig, ax = plt.subplots(figsize=(10,5))

    sns.countplot(
        data=filtered,
        y="Country",
        order=filtered["Country"].value_counts().index,
        palette="viridis",
        ax=ax
    )

    ax.set_xlabel("Number of Buyers")

    st.pyplot(fig)

with right:

    st.subheader("🌍 Buyers by Region")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="Region",
        palette="Set2",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

st.markdown("---")

# =====================================================
# Buyer Segment by Region
# =====================================================

st.subheader("🏠 Buyer Segments Across Regions")

fig, ax = plt.subplots(figsize=(10,5))

sns.countplot(
    data=filtered,
    x="Region",
    hue="Buyer_Segment",
    palette="Set1",
    ax=ax
)

plt.xticks(rotation=20)

st.pyplot(fig)

st.markdown("---")

# =====================================================
# Satisfaction by Region
# =====================================================

left, right = st.columns(2)

with left:

    st.subheader("😊 Satisfaction by Region")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.boxplot(
        data=filtered,
        x="Region",
        y="satisfaction_score",
        palette="coolwarm",
        ax=ax
    )

    plt.xticks(rotation=20)

    st.pyplot(fig)

with right:

    st.subheader("📈 Average Age by Region")

    age_summary = (
        filtered.groupby("Region")["Age"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8,5))

    age_summary.plot(
        kind="bar",
        ax=ax
    )

    ax.set_ylabel("Average Age")

    st.pyplot(fig)

st.markdown("---")

# =====================================================
# Geographic Summary
# =====================================================

st.subheader("📋 Geographic Summary")

summary = filtered.groupby(["Region", "Country"]).agg(
    Buyers=("Buyer_Segment", "count"),
    Avg_Age=("Age", "mean"),
    Avg_Satisfaction=("satisfaction_score", "mean")
).round(2)

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# Raw Dataset
# =====================================================

with st.expander("📄 View Geographic Dataset"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

# =====================================================
# Download
# =====================================================

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Geographic Report",
    csv,
    file_name="Geographic_Analysis.csv",
    mime="text/csv"
)

st.markdown("---")

st.success("✅ Geographic Buyer Analysis Completed Successfully.")
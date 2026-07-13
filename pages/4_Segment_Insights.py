import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===================================================
# Page Configuration
# ===================================================

st.set_page_config(
    page_title="Segment Insights",
    page_icon="💡",
    layout="wide"
)

# ===================================================
# Load Data
# ===================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/Buyer_Segmentation_Final.csv")

df = load_data()

# ===================================================
# Title
# ===================================================

st.title("💡 Buyer Segment Insights")

st.markdown("""
Explore detailed insights about each buyer segment including
demographics, investment behaviour, financing patterns,
customer satisfaction, and business recommendations.
""")

st.markdown("---")

# ===================================================
# Sidebar Filters
# ===================================================

st.sidebar.header("🔍 Segment Filters")

segment = st.sidebar.selectbox(
    "Buyer Segment",
    sorted(df["Buyer_Segment"].unique())
)

filtered = df[df["Buyer_Segment"] == segment]

# ===================================================
# KPI Cards
# ===================================================

st.subheader("📊 Segment KPIs")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Total Buyers",
        len(filtered)
    )

with c2:
    st.metric(
        "Average Age",
        round(filtered["Age"].mean(),1)
    )

with c3:
    st.metric(
        "Average Satisfaction",
        round(filtered["satisfaction_score"].mean(),2)
    )

with c4:
    st.metric(
        "Countries",
        filtered["country"].nunique()
    )

st.markdown("---")

# ===================================================
# Buyer Profile
# ===================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("👥 Gender Distribution")

    fig,ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=filtered,
        x="gender",
        palette="Set2",
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("🏢 Client Type")

    fig,ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=filtered,
        x="client_type",
        palette="Set3",
        ax=ax
    )

    st.pyplot(fig)

st.markdown("---")

# ===================================================
# Loan & Acquisition
# ===================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("🏦 Loan Behaviour")

    fig,ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=filtered,
        x="loan_applied",
        palette="Pastel1",
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("🏠 Acquisition Purpose")

    fig,ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=filtered,
        x="acquisition_purpose",
        palette="Set1",
        ax=ax
    )

    plt.xticks(rotation=15)

    st.pyplot(fig)

st.markdown("---")

# ===================================================
# Age & Satisfaction
# ===================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("📈 Age Distribution")

    fig,ax = plt.subplots(figsize=(6,4))

    sns.histplot(
        filtered["Age"],
        bins=20,
        kde=True,
        color="steelblue",
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("😊 Satisfaction Score")

    fig,ax = plt.subplots(figsize=(6,4))

    sns.boxplot(
        y=filtered["satisfaction_score"],
        color="lightgreen",
        ax=ax
    )

    st.pyplot(fig)

st.markdown("---")

# ===================================================
# Country & Region
# ===================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("🌍 Top Countries")

    st.dataframe(
        filtered["country"]
        .value_counts()
        .reset_index()
        .rename(columns={
            "index":"Country",
            "country":"Buyers"
        }),
        use_container_width=True
    )

with col2:

    st.subheader("🌎 Top Regions")

    st.dataframe(
        filtered["region"]
        .value_counts()
        .reset_index()
        .rename(columns={
            "index":"Region",
            "region":"Buyers"
        }),
        use_container_width=True
    )

st.markdown("---")

# ===================================================
# Referral Channel
# ===================================================

st.subheader("📢 Referral Channels")

fig,ax = plt.subplots(figsize=(8,4))

sns.countplot(
    data=filtered,
    x="referral_channel",
    palette="tab20",
    ax=ax
)

plt.xticks(rotation=30)

st.pyplot(fig)

st.markdown("---")

# ===================================================
# Statistical Summary
# ===================================================

st.subheader("📋 Statistical Summary")

summary = filtered.describe(include="all")

st.dataframe(
    summary,
    use_container_width=True
)

st.markdown("---")

# ===================================================
# Business Recommendations
# ===================================================

st.subheader("💼 Business Recommendation")

loan_mode = filtered["loan_applied"].mode()[0]
purpose_mode = filtered["acquisition_purpose"].mode()[0]
client_mode = filtered["client_type"].mode()[0]

if loan_mode == "Yes":
    recommendation = """
### Recommended Strategy

- Promote flexible financing and EMI plans.
- Partner with banks for attractive loan packages.
- Target first-time buyers with affordable properties.
- Highlight financing support in marketing campaigns.
"""
else:
    recommendation = """
### Recommended Strategy

- Focus on premium and luxury property listings.
- Promote long-term investment opportunities.
- Offer exclusive investment consultations.
- Target high-net-worth and corporate buyers.
"""

st.success(recommendation)

st.info(f"""
**Most Common Client Type:** {client_mode}

**Primary Acquisition Purpose:** {purpose_mode}

**Dominant Loan Preference:** {loan_mode}
""")

st.markdown("---")

# ===================================================
# Raw Data
# ===================================================

with st.expander("📄 View Segment Data"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

# ===================================================
# Download Button
# ===================================================

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Segment Report",
    csv,
    file_name=f"{segment}_Segment_Report.csv",
    mime="text/csv"
)

st.markdown("---")

st.success("✅ Segment Insights Generated Successfully.")
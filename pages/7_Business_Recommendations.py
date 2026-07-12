import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Business Recommendations",
    page_icon="📌",
    layout="wide"
)

# ======================================================
# Load Data
# ======================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/Buyer_Segmentation_Final.csv")

df = load_data()

# ======================================================
# Title
# ======================================================

st.title("📌 Business Recommendations Dashboard")

st.markdown("""
This dashboard transforms machine learning insights into practical business
recommendations for marketing, sales, and investment strategy.
""")

st.markdown("---")

# ======================================================
# Sidebar
# ======================================================

st.sidebar.header("🔍 Filters")

segment = st.sidebar.selectbox(
    "Buyer Segment",
    sorted(df["Buyer_Segment"].unique())
)

subset = df[df["Buyer_Segment"] == segment]

# ======================================================
# Executive KPIs
# ======================================================

st.subheader("📊 Executive KPIs")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("Total Buyers", len(subset))

with c2:
    st.metric(
        "Average Age",
        round(subset["Age"].mean(),1)
    )

with c3:
    st.metric(
        "Average Satisfaction",
        round(subset["satisfaction_score"].mean(),2)
    )

with c4:
    st.metric(
        "Countries",
        subset["country"].nunique()
    )

st.markdown("---")

# ======================================================
# Customer Profile
# ======================================================

st.subheader("👥 Customer Profile")

col1,col2 = st.columns(2)

with col1:

    fig,ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=subset,
        x="client_type",
        palette="Set2",
        ax=ax
    )

    ax.set_title("Client Type")

    st.pyplot(fig)

with col2:

    fig,ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=subset,
        x="loan_applied",
        palette="Set3",
        ax=ax
    )

    ax.set_title("Loan Behaviour")

    st.pyplot(fig)

st.markdown("---")

# ======================================================
# Geographic Insights
# ======================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("🌍 Top Countries")

    st.dataframe(
        subset["country"]
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
        subset["region"]
        .value_counts()
        .reset_index()
        .rename(columns={
            "index":"Region",
            "region":"Buyers"
        }),
        use_container_width=True
    )

st.markdown("---")

# ======================================================
# Satisfaction Analysis
# ======================================================

st.subheader("😊 Customer Satisfaction")

fig,ax = plt.subplots(figsize=(8,5))

sns.boxplot(
    data=subset,
    y="satisfaction_score",
    color="lightgreen",
    ax=ax
)

st.pyplot(fig)

st.markdown("---")

# ======================================================
# Business Strategy
# ======================================================

st.subheader("🎯 Recommended Business Strategy")

loan_mode = subset["loan_applied"].mode()[0]
purpose = subset["acquisition_purpose"].mode()[0]
client = subset["client_type"].mode()[0]

if loan_mode == "Yes":

    st.success("""
### 🏦 Financing Strategy

- Expand home loan partnerships
- Introduce flexible EMI plans
- Promote affordable housing
- Offer first-time buyer incentives
- Simplify loan approval support
""")

else:

    st.success("""
### 💎 Investment Strategy

- Focus on luxury properties
- Market premium investment opportunities
- Offer exclusive investment consultations
- Launch VIP customer programs
- Promote commercial property portfolios
""")

st.markdown("---")

# ======================================================
# AI Insights
# ======================================================

st.subheader("🤖 AI-Generated Insights")

st.info(f"""
**Dominant Client Type:** {client}

**Primary Acquisition Purpose:** {purpose}

**Preferred Financing:** {loan_mode}

**Average Customer Satisfaction:** {round(subset['satisfaction_score'].mean(),2)}

These insights indicate where marketing resources and product offerings
should be focused for this buyer segment.
""")

st.markdown("---")

# ======================================================
# SWOT Analysis
# ======================================================

st.subheader("📌 SWOT Analysis")

col1,col2 = st.columns(2)

with col1:

    st.success("""
### Strengths

✔ Clear buyer segmentation

✔ Targeted marketing opportunities

✔ Data-driven customer profiling

✔ Better customer understanding
""")

    st.warning("""
### Weaknesses

• Limited historical behaviour

• Dependent on available customer data

• Requires periodic retraining
""")

with col2:

    st.info("""
### Opportunities

✔ Personalized recommendations

✔ Geographic expansion

✔ Cross-selling opportunities

✔ Premium investment services
""")

    st.error("""
### Threats

• Changing market conditions

• Buyer preference shifts

• Economic fluctuations

• Competitive market
""")

st.markdown("---")

# ======================================================
# Executive Recommendations
# ======================================================

st.subheader("📈 Executive Action Plan")

recommendations = pd.DataFrame({

    "Priority":[
        "High",
        "High",
        "Medium",
        "Medium",
        "Low"
    ],

    "Recommendation":[
        "Launch targeted marketing campaigns",
        "Improve customer segmentation strategy",
        "Expand loan partnership programs",
        "Increase regional marketing",
        "Monitor customer satisfaction regularly"
    ]
})

st.dataframe(
    recommendations,
    use_container_width=True
)

st.markdown("---")

# ======================================================
# Business Summary
# ======================================================

st.subheader("📝 Executive Summary")

st.success(f"""
The selected buyer segment contains **{len(subset)} buyers**
with an average age of **{round(subset['Age'].mean(),1)} years**
and an average satisfaction score of
**{round(subset['satisfaction_score'].mean(),2)}**.

Based on the buyer profile, financing behaviour, and acquisition
preferences, personalized marketing strategies and investment
recommendations can improve customer engagement and increase
real estate sales performance.
""")

st.markdown("---")

# ======================================================
# Download Report
# ======================================================

csv = subset.to_csv(index=False)

st.download_button(
    "📥 Download Business Report",
    csv,
    file_name=f"{segment}_Business_Report.csv",
    mime="text/csv"
)

st.markdown("---")

st.success("✅ Business Recommendation Report Generated Successfully.")

st.caption("""
Machine Learning Based Buyer Segmentation & Investment Profiling
Developed using Python • Scikit-Learn • Streamlit
""")
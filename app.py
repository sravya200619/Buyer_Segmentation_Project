import streamlit as st

# ============================================
# Page Configuration
# ============================================

st.set_page_config(
    page_title="Real Estate Buyer Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# Custom CSS
# ============================================

st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:bold;
    color:#0E6BA8;
}

.sub-title{
    font-size:20px;
    color:gray;
}

.metric-box{
    background-color:#f5f7fa;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:2px 2px 8px rgba(0,0,0,0.1);
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# Sidebar
# ============================================

st.sidebar.title("🏠 Navigation")

st.sidebar.info("""
Use the pages below to explore:

📊 Buyer Segmentation

📈 Investor Behaviour

🌍 Geographic Analysis

💡 Segment Insights

📉 Cluster Visualization

📌 Business Recommendations

🔍 Predict New Buyer

📄 About Project
""")

st.sidebar.markdown("---")

st.sidebar.success("Machine Learning Project")

# ============================================
# Header
# ============================================

st.markdown(
    "<p class='main-title'>🏠 Machine Learning Based Buyer Segmentation & Investment Profiling</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>AI-Powered Real Estate Market Intelligence Dashboard</p>",
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================
# Welcome Section
# ============================================

st.info("""
Welcome to the **Real Estate Buyer Intelligence Dashboard**.

This project uses Machine Learning techniques to discover hidden buyer segments,
understand investment behaviour, and support data-driven real estate marketing strategies.
""")

# ============================================
# KPI Cards
# ============================================

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Machine Learning Model","K-Means")

with col2:
    st.metric("Secondary Model","Hierarchical")

with col3:
    st.metric("Visualization","PCA")

with col4:
    st.metric("Deployment","Streamlit")

st.markdown("---")

# ============================================
# Two Column Layout
# ============================================

left,right = st.columns([2,1])

# --------------------------------------------

with left:

    st.subheader("📌 Project Objectives")

    st.markdown("""
- Identify different types of property buyers
- Discover hidden investment patterns
- Analyze customer financing behaviour
- Study geographical investment trends
- Improve marketing effectiveness
- Support smarter business decisions
""")

    st.subheader("⚙ Machine Learning Workflow")

    st.markdown("""
1️⃣ Data Collection

⬇

2️⃣ Data Cleaning

⬇

3️⃣ Feature Engineering

⬇

4️⃣ Feature Encoding

⬇

5️⃣ Feature Scaling

⬇

6️⃣ K-Means Clustering

⬇

7️⃣ Hierarchical Clustering

⬇

8️⃣ PCA Visualization

⬇

9️⃣ Business Intelligence Dashboard
""")

# --------------------------------------------

with right:

    st.subheader("🧠 Algorithms Used")

    st.success("""
✔ K-Means Clustering

✔ Hierarchical Clustering

✔ PCA

✔ StandardScaler

✔ One-Hot Encoding

✔ Label Encoding
""")

    st.subheader("🛠 Technology Stack")

    st.info("""
Python

Pandas

NumPy

Scikit-Learn

Matplotlib

Seaborn

Streamlit
""")

st.markdown("---")

# ============================================
# Buyer Segments
# ============================================

st.subheader("🏘 Expected Buyer Segments")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.success("""
### 🌍 Global Investors

High investment potential

International buyers

Premium properties
""")

with c2:
    st.info("""
### 👨‍👩‍👧 First-Time Buyers

Young professionals

Loan dependent

Affordable homes
""")

with c3:
    st.warning("""
### 🏢 Corporate Buyers

Business investments

Commercial properties

Bulk purchases
""")

with c4:
    st.error("""
### 💎 Luxury Investors

High satisfaction

Premium investments

Luxury residences
""")

st.markdown("---")

# ============================================
# Dashboard Features
# ============================================

st.subheader("📊 Dashboard Modules")

feature1,feature2,feature3 = st.columns(3)

with feature1:

    st.markdown("""
### 📈 Analytics

- Buyer Segmentation
- Investor Behaviour
- Loan Analysis
- Customer Insights
""")

with feature2:

    st.markdown("""
### 🌍 Geographic Intelligence

- Country Analysis
- Regional Distribution
- Buyer Mapping
- Investment Trends
""")

with feature3:

    st.markdown("""
### 🤖 Machine Learning

- Clustering
- PCA
- Pattern Discovery
- AI Recommendations
""")

st.markdown("---")

# ============================================
# Business Benefits
# ============================================

st.subheader("🎯 Business Benefits")

st.markdown("""
✅ Better Customer Targeting

✅ Personalized Property Recommendations

✅ Smarter Investment Decisions

✅ Improved Marketing ROI

✅ Enhanced Customer Satisfaction

✅ Data-Driven Decision Making

✅ Geographic Market Intelligence
""")

st.markdown("---")

# ============================================
# Footer
# ============================================

st.markdown(
"""
<div class='footer'>

Developed using ❤️ with Python, Scikit-Learn & Streamlit

Machine Learning Based Buyer Segmentation & Investment Profiling

© 2026

</div>
""",
unsafe_allow_html=True
)
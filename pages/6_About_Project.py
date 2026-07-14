import streamlit as st

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="About Project",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# Title
# ==========================================================

st.title("📄 About the Project")

st.markdown("""
## 🏠 Machine Learning Based Buyer Segmentation and Investment Profiling for Real Estate Market Intelligence

This project leverages **Machine Learning** and **Business Intelligence** techniques to analyze real estate buyer behavior. By identifying hidden customer segments, the system enables real estate organizations to improve customer targeting, personalize marketing strategies, and make data-driven investment decisions.
""")

st.markdown("---")

# ==========================================================
# Project Overview
# ==========================================================

st.header("📌 Project Overview")

st.info("""
Real estate companies often deal with diverse customer groups such as first-time home buyers,
corporate investors, international buyers, and luxury investors. Traditional marketing treats
all customers similarly, leading to inefficient campaigns and missed investment opportunities.

This project uses **K-Means Clustering** and **Hierarchical Clustering** to discover hidden buyer
segments based on demographics, financing behavior, geographic location, and investment purpose.
""")

st.markdown("---")

# ==========================================================
# Project Objectives
# ==========================================================

st.header("🎯 Project Objectives")

col1, col2 = st.columns(2)

with col1:
    st.success("""
### Business Objectives

- Improve customer segmentation
- Identify investment behavior
- Enhance marketing effectiveness
- Support strategic business decisions
- Analyze geographic buyer trends
""")

with col2:
    st.success("""
### Technical Objectives

- Data Cleaning
- Feature Engineering
- Feature Scaling
- Machine Learning Clustering
- PCA Visualization
- Interactive Dashboard Development
""")

st.markdown("---")

# ==========================================================
# Machine Learning Workflow
# ==========================================================

st.header("⚙️ Machine Learning Workflow")

st.markdown("""
1️⃣ Data Collection

⬇️

2️⃣ Data Cleaning & Preprocessing

⬇️

3️⃣ Feature Encoding

⬇️

4️⃣ Feature Scaling

⬇️

5️⃣ K-Means Clustering

⬇️

6️⃣ Hierarchical Clustering

⬇️

7️⃣ PCA Visualization

⬇️

8️⃣ Business Insights & Recommendations

⬇️

9️⃣ Streamlit Dashboard Deployment
""")

st.markdown("---")

# ==========================================================
# Algorithms
# ==========================================================

st.header("🤖 Machine Learning Algorithms")

algorithms = {
    "Algorithm": [
        "K-Means Clustering",
        "Hierarchical Clustering",
        "Principal Component Analysis (PCA)",
        "StandardScaler",
        "One-Hot Encoding",
        "Label Encoding"
    ],
    "Purpose": [
        "Buyer Segmentation",
        "Cluster Validation",
        "Dimensionality Reduction",
        "Feature Scaling",
        "Categorical Feature Transformation",
        "Categorical Encoding"
    ]
}

st.dataframe(algorithms, use_container_width=True)

st.markdown("---")

# ==========================================================
# Dashboard Modules
# ==========================================================

st.header("📊 Dashboard Modules")

modules = [
    "🏠 Home Dashboard",
    "📊 Buyer Segmentation",
    "📈 Investor Behaviour Dashboard",
    "🌍 Geographic Buyer Analysis",
    "💡 Segment Insights",
    "🔍 Buyer Segment Prediction",
    "📉 PCA Cluster Visualization",
    "📌 Business Recommendations",
    "📄 About Project"
]

for module in modules:
    st.write(f"✅ {module}")

st.markdown("---")

# ==========================================================
# Technology Stack
# ==========================================================

st.header("🛠️ Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Programming & Libraries")

    st.write("""
- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Seaborn
- Joblib
""")

with col2:
    st.subheader("Development Tools")

    st.write("""
- Streamlit
- Google Colab
- Jupyter Notebook
- VS Code
- Git & GitHub
""")

st.markdown("---")

# ==========================================================
# Business Benefits
# ==========================================================

st.header("💼 Business Benefits")

benefits = [
    "🎯 Personalized Marketing Campaigns",
    "🏡 Smarter Property Recommendations",
    "📍 Geographic Buyer Intelligence",
    "💰 Better Investment Profiling",
    "📊 Improved Customer Segmentation",
    "📈 Higher Marketing ROI",
    "🤝 Better Customer Engagement",
    "🧠 Data-Driven Decision Making"
]

for benefit in benefits:
    st.write(benefit)

st.markdown("---")

# ==========================================================
# Key Features
# ==========================================================

st.header("⭐ Key Features")

st.success("""
✔ AI-based Buyer Segmentation

✔ Interactive Business Dashboard

✔ Geographic Buyer Analysis

✔ Customer Satisfaction Insights

✔ Investment Behaviour Analysis

✔ Loan Behaviour Analysis

✔ PCA Cluster Visualization

✔ AI-Powered Business Recommendations

✔ Buyer Segment Prediction
""")

st.markdown("---")

# ==========================================================
# Project Outcomes
# ==========================================================

st.header("📈 Expected Outcomes")

st.info("""
The developed system enables real estate organizations to:

• Understand customer buying patterns.

• Identify high-value investment segments.

• Optimize marketing campaigns.

• Improve customer targeting.

• Increase business profitability.

• Support strategic investment decisions.

• Enhance customer experience through data-driven insights.
""")

st.markdown("---")

# ==========================================================
# Future Enhancements
# ==========================================================

st.header("🚀 Future Enhancements")

st.write("""
- 🌍 Interactive Geographic Maps
- 🤖 Deep Learning-Based Segmentation
- 📈 Real-Time Customer Analytics
- ☁️ Cloud Database Integration
- 📊 Live Business Intelligence Dashboard
- 🔔 Automated Marketing Recommendations
- 📱 Mobile-Friendly Dashboard
""")

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.success("""
🎓 Developed as part of the **Unified Mentor Internship Project**

🏠 Machine Learning Based Buyer Segmentation & Investment Profiling for Real Estate Market Intelligence
""")

st.caption("""
Developed using Python • Scikit-Learn • Streamlit • Machine Learning

© 2026 | Unified Mentor Internship Project
""")
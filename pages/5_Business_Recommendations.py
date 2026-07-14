import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="Business Recommendations",
    page_icon="📌",
    layout="wide"
)

# ======================================================
# Load Data with Robust Path Fallbacks
# ======================================================

@st.cache_data
def load_data():
    possible_paths = [
        "data/Buyer_Segmentation_Final.csv",
        "Buyer_Segmentation_Final.csv",
        "../data/Buyer_Segmentation_Final.csv"
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if file_path is None:
        raise FileNotFoundError("Could not locate 'Buyer_Segmentation_Final.csv' in workspace directories.")
        
    df = pd.read_csv(file_path)
    # Standardize headers to lowercase snake_case to avoid case-sensitivity KeyErrors
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
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

    # Safety check if column mapping exists
    segment_col = "buyer_segment" if "buyer_segment" in df.columns else df.columns[0]

    segment = st.sidebar.selectbox(
        "Buyer Segment",
        sorted(df[segment_col].dropna().unique())
    )

    subset = df[df[segment_col] == segment]

    # ======================================================
    # Executive KPIs
    # ======================================================

    st.subheader("📊 Executive KPIs")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Buyers", len(subset))

    with c2:
        # Accessing standardized lowercase "age"
        avg_age = round(subset["age"].mean(), 1) if "age" in subset.columns and not subset.empty else 0
        st.metric("Average Age", avg_age)

    with c3:
        avg_sat = round(subset["satisfaction_score"].mean(), 2) if "satisfaction_score" in subset.columns and not subset.empty else 0
        st.metric("Average Satisfaction", avg_sat)

    with c4:
        unique_countries = subset["country"].nunique() if "country" in subset.columns else 0
        st.metric("Countries", unique_countries)

    st.markdown("---")

    # ======================================================
    # Customer Profile
    # ======================================================

    st.subheader("👥 Customer Profile")

    col1, col2 = st.columns(2)

    with col1:
        if "client_type" in subset.columns and not subset.empty:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(
                data=subset,
                x="client_type",
                palette="Set2",
                ax=ax
            )
            ax.set_title("Client Type")
            st.pyplot(fig)
        else:
            st.info("Client type feature metric visualization unavailable.")

    with col2:
        if "loan_applied" in subset.columns and not subset.empty:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(
                data=subset,
                x="loan_applied",
                palette="Set3",
                ax=ax
            )
            ax.set_title("Loan Behaviour")
            st.pyplot(fig)
        else:
            st.info("Loan behavior feature metric visualization unavailable.")

    st.markdown("---")

    # ======================================================
    # Geographic Insights
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Top Countries")
        if "country" in subset.columns and not subset.empty:
            country_df = subset["country"].value_counts().reset_index()
            country_df.columns = ["Country", "Buyers"]
            st.dataframe(country_df, use_container_width=True, hide_index=True)
        else:
            st.write("No country logs found.")

    with col2:
        st.subheader("🌎 Top Regions")
        if "region" in subset.columns and not subset.empty:
            region_df = subset["region"].value_counts().reset_index()
            region_df.columns = ["Region", "Buyers"]
            st.dataframe(region_df, use_container_width=True, hide_index=True)
        else:
            st.write("No regional logs found.")

    st.markdown("---")

    # ======================================================
    # Satisfaction Analysis
    # ======================================================

    st.subheader("😊 Customer Satisfaction")

    if "satisfaction_score" in subset.columns and not subset.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(
            data=subset,
            y="satisfaction_score",
            color="lightgreen",
            ax=ax
        )
        st.pyplot(fig)
    else:
        st.info("Satisfaction metrics are empty or missing.")

    st.markdown("---")

    # ======================================================
    # Business Strategy
    # ======================================================

    st.subheader("🎯 Recommended Business Strategy")

    # Extract dominant variables safely
    loan_mode = subset["loan_applied"].mode()[0] if "loan_applied" in subset.columns and not subset.empty else "No"
    purpose = subset["acquisition_purpose"].mode()[0] if "acquisition_purpose" in subset.columns and not subset.empty else "Unknown"
    client = subset["client_type"].mode()[0] if "client_type" in subset.columns and not subset.empty else "Unknown"

    if str(loan_mode).strip().lower() in ["yes", "y", "1", "true"]:
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

    **Average Customer Satisfaction:** {avg_sat}

    These insights indicate where marketing resources and product offerings
    should be focused for this buyer segment.
    """)

    st.markdown("---")

    # ======================================================
    # SWOT Analysis
    # ======================================================

    st.subheader("📌 SWOT Analysis")

    col1, col2 = st.columns(2)

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
        "Priority": ["High", "High", "Medium", "Medium", "Low"],
        "Recommendation": [
            "Launch targeted marketing campaigns",
            "Improve customer segmentation strategy",
            "Expand loan partnership programs",
            "Increase regional marketing",
            "Monitor customer satisfaction regularly"
        ]
    })

    st.dataframe(
        recommendations,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ======================================================
    # Business Summary
    # ======================================================

    st.subheader("📝 Executive Summary")

    st.success(f"""
    The selected buyer segment contains **{len(subset)} buyers**
    with an average age of **{avg_age} years**
    and an average satisfaction score of **{avg_sat}**.

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
    clean_filename = str(segment).lower().replace(" ", "_")

    st.download_button(
        "📥 Download Business Report",
        csv,
        file_name=f"{clean_filename}_business_report.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.success("✅ Business Recommendation Report Generated Successfully.")

    st.caption("""
    Machine Learning Based Buyer Segmentation & Investment Profiling
    Developed using Python • Scikit-Learn • Streamlit
    """)

except FileNotFoundError:
    st.error("🚨 **File Missing:** The application pipeline could not access `Buyer_Segmentation_Final.csv`.")
    st.info("Please verify the file exists within your workspace `/data` subdirectory.")
except Exception as e:
    st.error(f"An unexpected data layout error occurred: {e}")
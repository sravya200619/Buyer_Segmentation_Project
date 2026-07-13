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
    df = pd.read_csv("data/Buyer_Segmentation_Final.csv")
    
    # Standardize column names: strip whitespace, lowercase everything, replace spaces with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
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

    # All column queries now safely use normalized lowercase strings
    purpose = st.sidebar.multiselect(
        "Acquisition Purpose",
        sorted(df["acquisition_purpose"].unique()),
        default=sorted(df["acquisition_purpose"].unique())
    )

    segment = st.sidebar.multiselect(
        "Buyer Segment",
        sorted(df["buyer_segment"].unique()),
        default=sorted(df["buyer_segment"].unique())
    )

    region = st.sidebar.multiselect(
        "Region",
        sorted(df["region"].unique()),
        default=sorted(df["region"].unique())
    )

    filtered = df[
        (df["acquisition_purpose"].isin(purpose)) &
        (df["buyer_segment"].isin(segment)) &
        (df["region"].isin(region))
    ]

    # =====================================================
    # KPI Cards
    # =====================================================

    st.subheader("📊 Investor KPIs")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Investors",
            len(filtered)
        )

    with col2:
        st.metric(
            "Average Age",
            round(filtered["age"].mean(), 1) if not filtered.empty else 0
        )

    with col3:
        st.metric(
            "Average Satisfaction",
            round(filtered["satisfaction_score"].mean(), 2) if not filtered.empty else 0
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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏦 Loan Behaviour")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.countplot(
            data=filtered,
            x="buyer_segment",
            hue="loan_applied",
            palette="Set2",
            ax=ax
        )
        plt.xticks(rotation=20)
        st.pyplot(fig)

    with col2:
        st.subheader("🏠 Acquisition Purpose")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.countplot(
            data=filtered,
            x="buyer_segment",
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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("😊 Satisfaction Score")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.boxplot(
            data=filtered,
            x="buyer_segment",
            y="satisfaction_score",
            palette="viridis",
            ax=ax
        )
        plt.xticks(rotation=20)
        st.pyplot(fig)

    with col2:
        st.subheader("👥 Age Distribution")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.histplot(
            filtered["age"],
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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Region-wise Investors")
        fig, ax = plt.subplots(figsize=(8, 5))
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
        if not filtered.empty:
            country_count = filtered["country"].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(8, 5))
            country_count.plot(kind="bar", ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No data available for the selected filters.")

    st.markdown("---")

    # =====================================================
    # Referral Channel
    # =====================================================

    st.subheader("📢 Referral Channel")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(
        data=filtered,
        x="referral_channel",
        hue="buyer_segment",
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
    summary = filtered.groupby("buyer_segment").agg(
        Total_Buyers=("client_id", "count"),
        Average_Age=("age", "mean"),
        Average_Satisfaction=("satisfaction_score", "mean")
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

except KeyError as e:
    st.error(f"Missing Column: Could not find a matching variation of {e} in the CSV dataset.")
    st.warning("Available columns detected in your file: " + ", ".join(df.columns if 'df' in locals() else []))
except FileNotFoundError:
    st.error("Data file directory path not found. Please verify `data/Buyer_Segmentation_Final.csv` exists.")
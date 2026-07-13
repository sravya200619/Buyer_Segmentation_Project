import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===========================================================
# Page Configuration
# ===========================================================

st.set_page_config(
    page_title="Geographic Buyer Analysis",
    page_icon="🌍",
    layout="wide"
)

# ===========================================================
# Load Dataset
# ===========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/Buyer_Segmentation_Final.csv")
    
    # Standardize column names: strip whitespace, lowercase everything, replace spaces with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
    df = load_data()

    # ===========================================================
    # Title
    # ===========================================================

    st.title("🌍 Geographic Buyer Analysis")

    st.markdown("""
    Analyze buyer distribution across different countries and regions,
    along with customer demographics, loan behaviour, and investment patterns.
    """)

    st.markdown("---")

    # ===========================================================
    # Sidebar Filters
    # ===========================================================

    st.sidebar.header("🌍 Geographic Filters")

    # Using safely normalized lowercase identifiers globally
    region = st.sidebar.multiselect(
        "Region",
        sorted(df["region"].unique()),
        default=sorted(df["region"].unique())
    )

    country = st.sidebar.multiselect(
        "Country",
        sorted(df["country"].unique()),
        default=sorted(df["country"].unique())
    )

    segment = st.sidebar.multiselect(
        "Buyer Segment",
        sorted(df["buyer_segment"].unique()),
        default=sorted(df["buyer_segment"].unique())
    )

    filtered = df[
        (df["region"].isin(region)) &
        (df["country"].isin(country)) &
        (df["buyer_segment"].isin(segment))
    ]

    # ===========================================================
    # KPI Cards
    # ===========================================================

    st.subheader("📊 Geographic KPIs")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Buyers",
            len(filtered)
        )

    with c2:
        st.metric(
            "Countries",
            filtered["country"].nunique()
        )

    with c3:
        st.metric(
            "Regions",
            filtered["region"].nunique()
        )

    with c4:
        st.metric(
            "Average Satisfaction",
            round(filtered["satisfaction_score"].mean(), 2) if not filtered.empty else 0
        )

    st.markdown("---")

    # ===========================================================
    # Region & Country Distribution
    # ===========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏙 Buyers by Region")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.countplot(
            data=filtered,
            x="region",
            palette="Set2",
            ax=ax
        )
        plt.xticks(rotation=30)
        st.pyplot(fig)

    with col2:
        st.subheader("🌎 Buyers by Country")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(
            data=filtered,
            x="country",
            palette="Set3",
            ax=ax
        )
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.markdown("---")

    # ===========================================================
    # Buyer Segment by Country
    # ===========================================================

    st.subheader("🏠 Buyer Segments by Country")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.countplot(
        data=filtered,
        x="country",
        hue="buyer_segment",
        palette="tab10",
        ax=ax
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("---")

    # ===========================================================
    # Client Type & Loan Behaviour
    # ===========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏢 Client Type")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.countplot(
            data=filtered,
            x="region",
            hue="client_type",
            ax=ax
        )
        plt.xticks(rotation=30)
        st.pyplot(fig)

    with col2:
        st.subheader("🏦 Loan Behaviour")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.countplot(
            data=filtered,
            x="region",
            hue="loan_applied",
            ax=ax
        )
        plt.xticks(rotation=30)
        st.pyplot(fig)

    st.markdown("---")

    # ===========================================================
    # Satisfaction & Age
    # ===========================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("😊 Satisfaction by Region")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(
            data=filtered,
            x="region",
            y="satisfaction_score",
            palette="viridis",
            ax=ax
        )
        plt.xticks(rotation=30)
        st.pyplot(fig)

    with col2:
        st.subheader("👥 Age Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(
            data=filtered,
            x="region",
            y="age",
            palette="coolwarm",
            ax=ax
        )
        plt.xticks(rotation=30)
        st.pyplot(fig)

    st.markdown("---")

    # ===========================================================
    # Acquisition Purpose
    # ===========================================================

    st.subheader("🏘 Acquisition Purpose by Region")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(
        data=filtered,
        x="region",
        hue="acquisition_purpose",
        palette="Set1",
        ax=ax
    )
    plt.xticks(rotation=30)
    st.pyplot(fig)

    st.markdown("---")

    # ===========================================================
    # Heatmap
    # ===========================================================

    st.subheader("🔥 Buyer Segment Heatmap")
    if not filtered.empty:
        heat = pd.crosstab(
            filtered["region"],
            filtered["buyer_segment"]
        )
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(
            heat,
            annot=True,
            cmap="YlGnBu",
            fmt="d",
            ax=ax
        )
        st.pyplot(fig)
    else:
        st.info("No data satisfies the current filter combination to render the heatmap.")

    st.markdown("---")

    # ===========================================================
    # Geographic Summary
    # ===========================================================

    st.subheader("📋 Geographic Summary")
    summary = filtered.groupby(["region"]).agg(
        Buyers=("client_id", "count"),
        Avg_Age=("age", "mean"),
        Avg_Satisfaction=("satisfaction_score", "mean")
    ).round(2)

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.markdown("---")

    # ===========================================================
    # Raw Data
    # ===========================================================

    with st.expander("📄 View Geographic Dataset"):
        st.dataframe(
            filtered,
            use_container_width=True
        )

    # ===========================================================
    # Download Button
    # ===========================================================

    csv = filtered.to_csv(index=False)
    st.download_button(
        "📥 Download Geographic Data",
        csv,
        file_name="Geographic_Analysis.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.success("🌍 Geographic Buyer Analysis Completed Successfully.")

except KeyError as e:
    st.error(f"Missing Column: Verification variant of {e} could not be resolved from CSV context.")
    st.warning("Found file columns: " + ", ".join(df.columns if 'df' in locals() else []))
except FileNotFoundError:
    st.error("Target missing: Unable to read `data/Buyer_Segmentation_Final.csv` directory structure.")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Cluster Visualization",
    page_icon="📉",
    layout="wide"
)

# =====================================================
# Load Dataset with Path Fallbacks
# =====================================================

@st.cache_data
def load_data():
    # List of potential paths where the file could live depending on deployment directory
    possible_paths = [
        "data/buyer_segments_pca.csv",
        "buyer_segments_pca.csv",
        "../data/buyer_segments_pca.csv"
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if file_path is None:
        raise FileNotFoundError("Could not locate 'buyer_segments_pca.csv' in standard directories.")
        
    df = pd.read_csv(file_path)
    # Standardize column names: strip whitespace, lowercase everything, replace spaces with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

try:
    df = load_data()

    # =====================================================
    # Title
    # =====================================================

    st.title("📉 PCA Cluster Visualization")

    st.markdown("""
    Principal Component Analysis (PCA) projects high-dimensional buyer data into
    two dimensions, making it easier to visualize buyer clusters identified by
    the K-Means clustering algorithm.
    """)

    st.markdown("---")

    # =====================================================
    # Sidebar
    # =====================================================

    st.sidebar.header("Visualization Filters")

    # Access normalized lowercase columns safely
    clusters = sorted(df["cluster"].unique())

    selected_clusters = st.sidebar.multiselect(
        "Select Cluster(s)",
        clusters,
        default=clusters
    )

    filtered = df[df["cluster"].isin(selected_clusters)]

    # =====================================================
    # KPI Cards
    # =====================================================

    st.subheader("📊 Cluster Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Buyers",
            len(filtered)
        )

    with c2:
        st.metric(
            "Clusters",
            filtered["cluster"].nunique()
        )

    with c3:
        st.metric(
            "PC1 Mean",
            round(filtered["pc1"].mean(), 2) if not filtered.empty else 0
        )

    with c4:
        st.metric(
            "PC2 Mean",
            round(filtered["pc2"].mean(), 2) if not filtered.empty else 0
        )

    st.markdown("---")

    # =====================================================
    # PCA Scatter Plot
    # =====================================================

    st.subheader("📈 PCA Projection")

    if not filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 7))

        sns.scatterplot(
            data=filtered,
            x="pc1",
            y="pc2",
            hue="cluster",
            palette="Set1",
            s=100,
            alpha=0.8,
            edgecolor="black",
            ax=ax
        )

        ax.set_title("Buyer Segments using PCA")
        ax.set_xlabel("Principal Component 1")
        ax.set_ylabel("Principal Component 2")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.warning("No data points selected. Adjust sidebar filters to view projection plot.")

    st.markdown("---")

    # =====================================================
    # Cluster Distribution
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Cluster Distribution")
        if not filtered.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.countplot(
                data=filtered,
                x="cluster",
                palette="Set2",
                ax=ax
            )
            st.pyplot(fig)

    with col2:
        st.subheader("🥧 Cluster Share")
        if not filtered.empty:
            fig, ax = plt.subplots(figsize=(6, 6))
            filtered["cluster"].value_counts().plot(
                kind="pie",
                autopct="%1.1f%%",
                startangle=90,
                ax=ax
            )
            ax.set_ylabel("")
            st.pyplot(fig)

    st.markdown("---")

    # =====================================================
    # Cluster Statistics
    # =====================================================

    st.subheader("📋 Cluster Statistics")

    summary = filtered.groupby("cluster").agg(
        Buyers=("cluster", "count"),
        Avg_PC1=("pc1", "mean"),
        Avg_PC2=("pc2", "mean")
    ).round(2)

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # PCA Explanation
    # =====================================================

    st.subheader("🧠 Understanding PCA")

    st.info("""
    Principal Component Analysis (PCA) reduces many original buyer features into two
    principal components.

    • Nearby points indicate buyers with similar characteristics.

    • Well-separated groups indicate effective clustering.

    • Overlapping groups may suggest similar buyer behavior.
    """)

    st.markdown("---")

    # =====================================================
    # Business Insights
    # =====================================================

    st.subheader("💼 Business Insights")

    st.success("""
    ✅ Clearly separated clusters indicate distinct buyer groups.

    ✅ Marketing campaigns can be personalized for each segment.

    ✅ Buyer profiling improves investment recommendations.

    ✅ Geographic targeting becomes more effective.

    ✅ Customer engagement strategies can be optimized.
    """)

    st.markdown("---")

    # =====================================================
    # Raw Data
    # =====================================================

    with st.expander("📄 View PCA Dataset"):
        st.dataframe(
            filtered,
            use_container_width=True
        )

    st.markdown("---")

    # =====================================================
    # Download Button
    # =====================================================

    csv = filtered.to_csv(index=False)

    st.download_button(
        "📥 Download PCA Data",
        csv,
        file_name="buyer_segments_pca.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.success("✅ PCA Cluster Visualization Completed Successfully.")

except FileNotFoundError:
    st.error("🚨 **File Missing:** The file `buyer_segments_pca.csv` could not be located in your application workspace folder.")
    st.info("""
    **To fix this issue:**
    1. Verify that your PCA output generation script ran successfully.
    2. Confirm that the file is saved inside the `data/` directory.
    3. Ensure the filename is exactly lowercase: `buyer_segments_pca.csv` (Linux environments are case-sensitive).
    """)
except KeyError as e:
    st.error(f"Missing Expected Matrix Column: {e}")
    st.warning("Columns present in file: " + ", ".join(df.columns if 'df' in locals() else []))
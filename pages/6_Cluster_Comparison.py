import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Cluster Visualization",
    page_icon="📉",
    layout="wide"
)

# =====================================================
# Load Dataset
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/buyer_segments_pca.csv")

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

clusters = sorted(df["Cluster"].unique())

selected_clusters = st.sidebar.multiselect(
    "Select Cluster(s)",
    clusters,
    default=clusters
)

filtered = df[df["Cluster"].isin(selected_clusters)]

# =====================================================
# KPI Cards
# =====================================================

st.subheader("📊 Cluster Overview")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Total Buyers",
        len(filtered)
    )

with c2:
    st.metric(
        "Clusters",
        filtered["Cluster"].nunique()
    )

with c3:
    st.metric(
        "PC1 Mean",
        round(filtered["PC1"].mean(),2)
    )

with c4:
    st.metric(
        "PC2 Mean",
        round(filtered["PC2"].mean(),2)
    )

st.markdown("---")

# =====================================================
# PCA Scatter Plot
# =====================================================

st.subheader("📈 PCA Projection")

fig, ax = plt.subplots(figsize=(10,7))

sns.scatterplot(
    data=filtered,
    x="PC1",
    y="PC2",
    hue="Cluster",
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

st.markdown("---")

# =====================================================
# Cluster Distribution
# =====================================================

col1,col2 = st.columns(2)

with col1:

    st.subheader("📊 Cluster Distribution")

    fig, ax = plt.subplots(figsize=(7,5))

    sns.countplot(
        data=filtered,
        x="Cluster",
        palette="Set2",
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("🥧 Cluster Share")

    fig, ax = plt.subplots(figsize=(6,6))

    filtered["Cluster"].value_counts().plot(
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

summary = filtered.groupby("Cluster").agg(

    Buyers=("Cluster","count"),

    Avg_PC1=("PC1","mean"),

    Avg_PC2=("PC2","mean")

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
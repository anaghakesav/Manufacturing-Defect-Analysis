import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Manufacturing Defect Analysis",
    page_icon="🏭",
    layout="wide"
)


st.title("🏭 Manufacturing Defect Analysis Dashboard")

st.markdown(
    """
    Analyze manufacturing defects and production performance
    using interactive visualizations and business insights.
    """
)


df = pd.read_csv("manufacturing_data.csv")


st.sidebar.header("Filter Data")

machine_filter = st.sidebar.multiselect(
    "Select Machine",
    options=df["Machine"].unique()
)

shift_filter = st.sidebar.multiselect(
    "Select Shift",
    options=df["Shift"].unique()
)


filtered_df = df.copy()

if machine_filter:
    filtered_df = filtered_df[
        filtered_df["Machine"].isin(machine_filter)
    ]

if shift_filter:
    filtered_df = filtered_df[
        filtered_df["Shift"].isin(shift_filter)
    ]


total_products = len(filtered_df)

total_defects = len(
    filtered_df[filtered_df["Defect"] == "Yes"]
)

defect_percentage = (
    total_defects / total_products * 100
)

avg_temperature = (
    filtered_df["Temperature"].mean()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Products",
        total_products
    )

with col2:
    st.metric(
        "Total Defects",
        total_defects
    )

with col3:
    st.metric(
        "Defect Rate",
        f"{defect_percentage:.2f}%"
    )

with col4:
    st.metric(
        "Avg Temperature",
        f"{avg_temperature:.2f}"
    )


with st.expander("📄 View Dataset Preview"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )


fig1, ax1 = plt.subplots(figsize=(5, 3))

sns.countplot(
    x="Defect",
    data=filtered_df,
    ax=ax1
)

ax1.set_title("Product Quality Distribution")


fig2, ax2 = plt.subplots(figsize=(5, 3))

sns.countplot(
    x="Machine",
    hue="Defect",
    data=filtered_df,
    ax=ax2
)

ax2.set_title("Machine-wise Defects")


fig3, ax3 = plt.subplots(figsize=(5, 3))

sns.countplot(
    x="Shift",
    hue="Defect",
    data=filtered_df,
    ax=ax3
)

ax3.set_title("Shift-wise Defects")


fig4, ax4 = plt.subplots(figsize=(5, 3))

sns.histplot(
    filtered_df["Temperature"],
    bins=10,
    kde=True,
    ax=ax4
)

ax4.set_title("Temperature Distribution")


numeric_df = filtered_df.select_dtypes(
    include="number"
)

fig5, ax5 = plt.subplots(figsize=(5, 3))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    annot_kws={"size": 7},
    ax=ax5
)

ax5.set_title("Correlation Heatmap")


st.subheader("📊 Defect Analysis")

col_left, col_right = st.columns(2)

with col_left:
    st.pyplot(fig1)

with col_right:
    st.pyplot(fig2)


st.subheader("📈 Production Insights")

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.pyplot(fig3)

with col_right2:
    st.pyplot(fig4)


st.subheader("🔥 Correlation & Business Insights")

col_left3, col_right3 = st.columns(2)

with col_left3:
    st.pyplot(fig5)

with col_right3:

    st.markdown("### Key Insights")

    most_defective_machine = (
        filtered_df[
            filtered_df["Defect"] == "Yes"
        ]["Machine"]
        .value_counts()
    )

    if not most_defective_machine.empty:
        st.success(
            f"Machine with highest defects: "
            f"{most_defective_machine.idxmax()}"
        )

    st.info(
        f"Average Temperature: "
        f"{filtered_df['Temperature'].mean():.2f}"
    )

    st.info(
        f"Average Pressure: "
        f"{filtered_df['Pressure'].mean():.2f}"
    )

    st.info(
        f"Current Defect Rate: "
        f"{defect_percentage:.2f}%"
    )


st.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_manufacturing_data.csv",
    mime="text/csv"
)


st.markdown("---")

st.caption(
    "Built with Python • Pandas • Matplotlib • Seaborn • Streamlit"
)

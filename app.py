import streamlit as st
from analysis import *

st.set_page_config(page_title="Advanced Transaction Intelligence", layout="wide")

st.title("💳 Transaction Intelligence Platform")

# ==============================
# SIDEBAR NAVIGATION
# ==============================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Dataset Dashboard",
        "Global Filters",
        "Risk Control",
        "Analysis Mode",
        "Ask Questions",
        "Advance Analysis"
    ]
)

# ==============================
# 1️⃣ DATASET DASHBOARD
# ==============================

if page == "Dataset Dashboard":

    st.header("📊 Dataset Overview")

    summary = get_summary()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", summary["total_transactions"][0])
    col2.metric("Total Success", summary["total_success"][0])
    col3.metric("Total Failed", summary["total_failed"][0])
    col4.metric("Total Fraud ", summary["total_fraud"][0])

    st.divider()
    st.subheader("Sample Dataset")
    st.dataframe(get_sample_data())


# ==============================
# 2️⃣ GLOBAL FILTER SECTION
# ==============================

elif page == "Global Filters":

    st.header("🌍 Global Data Filters")

    df = get_full_data()

    col1, col2, col3 = st.columns(3)

    transaction_type = col1.selectbox(
        "Transaction Type",
        ["All"] + list(df["transaction type"].unique())
    )

    state = col2.selectbox(
        "Sender State",
        ["All"] + list(df["sender_state"].unique())
    )

    bank = col3.selectbox(
        "Sender Bank",
        ["All"] + list(df["sender_bank"].unique())
    )

    if transaction_type != "All":
        df = df[df["transaction type"] == transaction_type]

    if state != "All":
        df = df[df["sender_state"] == state]

    if bank != "All":
        df = df[df["sender_bank"] == bank]

    st.dataframe(df)


# ==============================
# 3️⃣ RISK CONTROL SECTION
# ==============================

elif page == "Risk Control":

    st.header("⚠ Risk Intelligence Panel")

    risk_data = get_risk_summary()

    st.subheader("Risk Distribution")

    st.plotly_chart(get_risk_pie_chart(risk_data), use_container_width=True)


# ==============================
# 4️⃣ ANALYSIS MODE
# ==============================

elif page == "Analysis Mode":

    st.header("📈 Full Analytical View")

    st.subheader("State Comparison")
    st.dataframe(compare_column("sender_state"))

    st.subheader("Bank Comparison")
    st.dataframe(compare_column("sender_bank"))

    st.subheader("Device Comparison")
    st.dataframe(compare_column("device_type"))

    st.subheader("Network Comparison")
    st.dataframe(compare_column("network_type"))


# ==============================
# 5️⃣ ASK QUESTIONS PANEL
# ==============================
elif page == "Ask Questions":

    st.header("💬 Intelligent Question Panel")

    query = st.text_input("Ask your question about transactions:")

    if st.button("Get Answer"):

        query_lower = query.lower()

        if "average" in query_lower and "type" in query_lower:
            st.subheader("Average Amount by Transaction Type")
            st.dataframe(avg_amount_by_type())

        elif "distribution" in query_lower or "percentage" in query_lower:
            st.subheader("Transaction Type Distribution")
            st.dataframe(transaction_type_distribution())

        elif "failure" in query_lower and "bank" in query_lower:
            st.subheader("Bank Failure Comparison")
            st.dataframe(compare_column("sender_bank"))

        elif "failure" in query_lower and "device" in query_lower:
            st.subheader("Device Failure Comparison")
            st.dataframe(compare_column("device_type"))

        elif "state" in query_lower:
            st.subheader("State Comparison")
            st.dataframe(compare_column("sender_state"))

        elif "network" in query_lower:
            st.subheader("Network Comparison")
            st.dataframe(compare_column("network_type"))

        elif "peak hour" in query_lower:
            peak_hour = get_peak_hour()
            st.success(f"Peak Hour: {peak_hour}")

            hour_df = get_hourly_distribution()

            st.subheader("Transactions by Hour")

            st.bar_chart(
                hour_df.set_index("hour_of_day")["total_transactions"]
            )

        elif "weekday" in query_lower:
            st.subheader("Weekday Analysis")
            st.dataframe(weekday_analysis())

        elif "high value" in query_lower:
            st.subheader("High Value Flag Analysis")
            st.dataframe(high_value_flag_analysis())

        elif "summary" in query_lower:
            st.subheader("Overall Summary")
            st.dataframe(get_summary())

        else:
            st.warning("Question not recognized. Try something like: 'failure rate by bank'")


elif page == "Advance Analysis":

    st.header("🚀 Advanced Intelligence Dashboard")

    df = get_full_data()

    # Ensure numeric conversion
    df["amount (INR)"] = pd.to_numeric(df["amount (INR)"], errors="coerce")

    # =============================
    # 1️⃣ RISK SCORE SYSTEM
    # =============================

    df["risk_score"] = (
        (df["amount (INR)"] > 10000) * 40 +
        (df["network_type"] == "2G") * 20 +
        (df["is_weekend"] == 1) * 10 +
        (df["hour_of_day"] > 22) * 15 +
        (df["fraud_flag"] == 1) * 50
    )

    df["risk_level"] = pd.cut(
        df["risk_score"],
        bins=[-1, 20, 60, 200],
        labels=["Low Risk", "Medium Risk", "High Risk"]
    )

    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]

    import plotly.express as px

    fig1 = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        title="Risk Level Distribution",
        color_discrete_sequence=["#00C9A7", "#FFC75F", "#FF6F91"]
    )

    st.plotly_chart(fig1, use_container_width=True)

    # =============================
    # 2️⃣ ANOMALY DETECTION
    # =============================

    mean = df["amount (INR)"].mean()
    std = df["amount (INR)"].std()

    df["anomaly"] = df["amount (INR)"] > (mean + 3*std)

    anomaly_counts = df["anomaly"].value_counts().reset_index()
    anomaly_counts.columns = ["Anomaly", "Count"]

    fig2 = px.pie(
        anomaly_counts,
        names="Anomaly",
        values="Count",
        title="Anomaly Detection Distribution",
        color_discrete_sequence=["#4D96FF", "#FF4D6D"]
    )

    st.plotly_chart(fig2, use_container_width=True)

    # =============================
    # 3️⃣ FRAUD VS NON-FRAUD
    # =============================

    fraud_counts = df["fraud_flag"].value_counts().reset_index()
    fraud_counts.columns = ["Fraud Flag", "Count"]

    fig3 = px.pie(
        fraud_counts,
        names="Fraud Flag",
        values="Count",
        title="Fraud vs Non-Fraud Transactions",
        color_discrete_sequence=["#6A67CE", "#FF9671"]
    )

    st.plotly_chart(fig3, use_container_width=True)

    # =============================
    # 4️⃣ WEEKEND RISK ANALYSIS
    # =============================

    weekend_counts = df["is_weekend"].value_counts().reset_index()
    weekend_counts.columns = ["Weekend", "Count"]

    fig4 = px.pie(
        weekend_counts,
        names="Weekend",
        values="Count",
        title="Weekend Transaction Distribution",
        color_discrete_sequence=["#00C2A8", "#845EC2"]
    )

    st.plotly_chart(fig4, use_container_width=True)
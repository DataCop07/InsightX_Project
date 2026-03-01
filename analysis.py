import sqlite3
import pandas as pd


# =============================
# CONNECTION
# =============================

def get_connection():
    return sqlite3.connect("transactions.db")


# =============================
# SUMMARY
# =============================

def get_summary():
    conn = get_connection()

    query = """
    SELECT 
        COUNT(*) as total_transactions,
        SUM(CASE WHEN transaction_status='SUCCESS' THEN 1 ELSE 0 END) as total_success,
        SUM(CASE WHEN transaction_status='FAILED' THEN 1 ELSE 0 END) as total_failed,
        SUM(CASE WHEN fraud_flag=1 THEN 1 ELSE 0 END) as total_fraud
    FROM transactions
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =============================
# GENERIC COMPARISON
# =============================

def compare_column(column_name):
    conn = get_connection()

    query = f"""
    SELECT 
        {column_name},
        COUNT(*) as total_transactions,
        AVG(CAST("amount (INR)" AS REAL)) as avg_amount,
        SUM(CASE WHEN transaction_status='FAILED' THEN 1 ELSE 0 END) as failed_transactions,
        ROUND(
            SUM(CASE WHEN transaction_status='FAILED' THEN 1 ELSE 0 END)*100.0 / COUNT(*),2
        ) as failure_rate_percentage,
        ROUND(
            SUM(CASE WHEN fraud_flag=1 THEN 1 ELSE 0 END)*100.0 / COUNT(*),2
        ) as fraud_rate_percentage
    FROM transactions
    GROUP BY {column_name}
    ORDER BY failure_rate_percentage DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =============================
# FULL DATA
# =============================

def get_full_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df


def get_sample_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM transactions LIMIT 10", conn)
    conn.close()
    return df


# =============================
# RISK SUMMARY
# =============================

def get_risk_summary():
    conn = get_connection()

    query = """
    SELECT
        SUM(CASE WHEN "amount (INR)" > 10000 THEN 1 ELSE 0 END) as high_value,
        SUM(CASE WHEN fraud_flag=1 THEN 1 ELSE 0 END) as fraud_flagged,
        SUM(CASE WHEN transaction_status='FAILED' THEN 1 ELSE 0 END) as failed
    FROM transactions
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df.iloc[0]


# =============================
# RISK PIE CHART
# =============================

def get_risk_pie_chart(data):
    import plotly.express as px

    labels = ["High Value", "Fraud Flagged", "Failed"]
    values = [data["high_value"], data["fraud_flagged"], data["failed"]]

    fig = px.pie(values=values, names=labels, title="Risk Distribution")
    return fig


# =============================
# PEAK HOUR
# =============================

def get_peak_hour():
    conn = get_connection()

    query = """
    SELECT hour_of_day, COUNT(*) as total
    FROM transactions
    GROUP BY hour_of_day
    ORDER BY total DESC
    LIMIT 1
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df.iloc[0]["hour_of_day"]


# =============================
# WEEKDAY ANALYSIS
# =============================

def weekday_analysis():
    conn = get_connection()

    query = """
    SELECT day_of_week, COUNT(*) as total_transactions
    FROM transactions
    GROUP BY day_of_week
    ORDER BY total_transactions DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =============================
# AVERAGE AMOUNT BY TYPE
# =============================

def avg_amount_by_type():
    conn = get_connection()

    query = """
    SELECT "transaction type", 
           AVG(CAST("amount (INR)" AS REAL)) as average_amount
    FROM transactions
    GROUP BY "transaction type"
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =============================
# TRANSACTION TYPE DISTRIBUTION
# =============================

def transaction_type_distribution():
    conn = get_connection()

    query = """
    SELECT "transaction type",
           COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions) as percentage
    FROM transactions
    GROUP BY "transaction type"
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =============================
# HIGH VALUE FLAG ANALYSIS
# =============================

def high_value_flag_analysis():
    conn = get_connection()

    query = """
    SELECT
        COUNT(*) as total_high_value,
        SUM(CASE WHEN fraud_flag=1 THEN 1 ELSE 0 END) as flagged_high_value,
        ROUND(
            SUM(CASE WHEN fraud_flag=1 THEN 1 ELSE 0 END)*100.0 / COUNT(*),2
        ) as flagged_percentage
    FROM transactions
    WHERE "amount (INR)" > 10000
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df
def get_hourly_distribution():
    conn = get_connection()

    query = """
    SELECT hour_of_day, COUNT(*) as total_transactions
    FROM transactions
    GROUP BY hour_of_day
    ORDER BY hour_of_day
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df
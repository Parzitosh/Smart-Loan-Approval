import streamlit as st
import pandas as pd
import os
import psycopg2

# 1. Page Config
st.set_page_config(page_title="FinTech Credit Analytics Engine", layout="wide")

# -----------------------------
# UI / UX styling (Streamlit)
# -----------------------------
st.markdown(
    """
    <style>
        .bb-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .bb-title {
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.15rem;
        }
        .bb-subtitle {
            color: rgba(255,255,255,0.75);
            margin-bottom: 1rem;
            font-size: 14px;
        }
        .bb-small {
            font-size: 12px;
            color: rgba(255,255,255,0.65);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="bb-title">📊 Smart Loan Risk Assessment System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="bb-subtitle">AI-inspired creditworthiness analysis dashboard</div>',
    unsafe_allow_html=True,
)

# DB Config from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "fintech_analytics")



def write_dataframe_to_postgres(df: pd.DataFrame):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credit_analytics (
            customer_id INTEGER,
            income NUMERIC,
            monthly_debt NUMERIC,
            credit_score INTEGER,
            employment_years INTEGER,
            dti DOUBLE PRECISION,
            status TEXT,
            interest_rate DOUBLE PRECISION
        );
    """)

    insert_query = """
        INSERT INTO credit_analytics (
            customer_id,
            income,
            monthly_debt,
            credit_score,
            employment_years,
            dti,
            status,
            interest_rate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            int(row["customer_id"]),
            float(row["income"]),
            float(row["monthly_debt"]),
            int(row["credit_score"]),
            int(row["employment_years"]),
            float(row["dti"]),
            str(row["status"]),
            float(row["interest_rate"])
        ))

    conn.commit()
    cursor.close()
    conn.close()



# 2. Sidebar: Batch Data Generator / CSV Upload
st.sidebar.header("📥 Financial Data Input")

input_method = st.sidebar.radio(
    "Choose Data Source",
    ["Generate Sample Data", "Upload CSV Dataset"]
)

if input_method == "Generate Sample Data":
    if st.sidebar.button("Generate Sample Bulk Data"):
        mock_data = pd.DataFrame({
            "customer_id": [101, 102, 103, 104, 105],
            "income": [45000, 120000, 30000, 85000, 60000],
            "monthly_debt": [2000, 1500, 1800, 2500, 4000],
            "credit_score": [550, 740, 620, 680, 580],
            "employment_years": [1, 5, 2, 4, 0]
        })
        st.session_state['batch_df'] = mock_data

elif input_method == "Upload CSV Dataset":
    uploaded_file = st.sidebar.file_uploader(
        "Upload Customer Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        st.session_state['batch_df'] = uploaded_df
        st.sidebar.success("✅ CSV uploaded successfully")




# ```python id="rbt7ie"
# 3. Main Body Pipeline
if 'batch_df' in st.session_state:
    st.subheader("📋 Ingested Raw Financial Records")
    st.dataframe(st.session_state['batch_df'], use_container_width=True)

    if st.button("🚀 Run Analytics Pipeline"):
        with st.spinner("Running analytics transformations..."):

            processed_pdf = st.session_state['batch_df'].copy()

            # Calculate DTI
            processed_pdf['dti'] = (
                processed_pdf['monthly_debt']
                / (processed_pdf['income'] / 12)
            )

            # Loan Approval Logic
            processed_pdf['status'] = processed_pdf.apply(
                lambda row: (
                    "Rejected"
                    if (
                        row['credit_score'] < 600
                        or row['dti'] > 0.45
                    )
                    else "Approved"
                ),
                axis=1
            )

            # Risk Category Classification
            def assign_risk(dti):
                if dti < 0.20:
                    return "Low Risk"
                elif dti < 0.35:
                    return "Medium Risk"
                elif dti <= 0.45:
                    return "High Risk"
                else:
                    return "Critical Risk"

            # Create risk category column
            processed_pdf['risk_category'] = (
                processed_pdf['dti']
                .apply(assign_risk)
            )

            # Interest Rate Calculation
            processed_pdf['interest_rate'] = 0.0

            approved_mask = (
                processed_pdf['status']
                == "Approved"
            )

            processed_pdf.loc[
                approved_mask,
                'interest_rate'
            ] = (
                0.05
                + (
                    0.10
                    * processed_pdf.loc[
                        approved_mask,
                        'dti'
                    ]
                )
            )

            st.success(
                "✅ Analytics pipeline completed successfully with pandas."
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total Records Processed",
                    len(processed_pdf)
                )

                st.subheader("Processed Results")
                st.dataframe(
                    processed_pdf,
                    use_container_width=True
                )

                # Download CSV
                csv = processed_pdf.to_csv(
                    index=False
                ).encode('utf-8')

                st.download_button(
                    label="⬇️ Download Processed Results",
                    data=csv,
                    file_name="credit_risk_results.csv",
                    mime="text/csv"
                )

            with col2:
                st.subheader(
                    "📊 Loan Approval Distribution"
                )
                st.bar_chart(
                    processed_pdf['status']
                    .value_counts()
                )

                st.subheader(
                    "⚠️ Risk Category Distribution"
                )
                st.bar_chart(
                    processed_pdf['risk_category']
                    .value_counts()
                )

            try:
                write_dataframe_to_postgres(
                    processed_pdf
                )
                st.info(
                    "💾 Analytics data successfully logged to PostgreSQL."
                )

            except Exception as e:
                st.warning(
                    f"Database write skipped or failed: {e}"
                )




# 4. History Tab
st.markdown("---")
st.subheader("📜 Historical Database Records (Live from AWS RDS)")
if st.button("Fetch Audit Logs"):
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        query = "SELECT * FROM credit_analytics ORDER BY customer_id DESC LIMIT 10;"
        history_df = pd.read_sql(query, conn)
        st.dataframe(history_df, use_container_width=True)
        conn.close()
    except Exception as e:
        st.error(f"Could not connect to database history: {e}")
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Page settings
st.set_page_config(layout="wide")
st.title("PostgreSQL Crime Data Explorer")

# Database connection using SQLAlchemy
@st.cache_resource
def connect_db():
    db_url = (
        f"postgresql+psycopg2://{st.secrets['DB_USER']}:"
        f"{st.secrets['DB_PASSWORD']}@{st.secrets['DB_HOST']}:"
        f"{st.secrets.get('DB_PORT', '5432')}/"
        f"{st.secrets['DB_NAME']}"
    )
    return create_engine(db_url)

conn = connect_db()

# SQL Query input
query = st.text_area("Enter your SQL query:")

if st.button("Run Query"):
    try:
        with st.spinner("Running query..."):
            df = pd.read_sql(query, conn)
            st.session_state['query_result'] = df
            st.success("Query executed successfully.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Show results if available
if 'query_result' in st.session_state:
    df = st.session_state['query_result']
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "query_result.csv", "text/csv")

    # Visualization
    st.subheader("📊 Visualization")
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Select X-axis", df.columns)
    with col2:
        y_axis = st.selectbox("Select Y-axis", df.columns)

    chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Scatter", "Area"])

    if chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif chart_type == "Area":
        fig = px.area(df, x=x_axis, y=y_axis)

    st.plotly_chart(fig, use_container_width=True)

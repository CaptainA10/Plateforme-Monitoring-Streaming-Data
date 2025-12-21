import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
import time

st.set_page_config(
    page_title="Monitoring Platform",
    page_icon="📊",
    layout="wide",
)

# Configuration
MONGO_URL = "mongodb://admin:password@localhost:27017/"
DB_NAME = "monitoring_datalake"
REFRESH_RATE = 5  # seconds

# Connect to MongoDB
@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URL)

client = init_connection()
db = client[DB_NAME]



st.title("🚀 Real-Time Data Monitoring")

# Placeholder for auto-refresh
placeholder = st.empty()

while True:
    with placeholder.container():
        # Fetch Data
        # 1. User Activity
        try:
            user_activity_count = db.raw_user_activity.count_documents({})
            # Get last 100 events for charts
            cursor = db.raw_user_activity.find().sort("timestamp", -1).limit(100)
            df_activity = pd.DataFrame(list(cursor))
        except Exception as e:
            st.error(f"Error connecting to MongoDB: {e}")
            time.sleep(REFRESH_RATE)
            continue

        # 2. Wikimedia Changes
        try:
            wikimedia_count = db.raw_wikimedia_changes.count_documents({})
        except:
            wikimedia_count = 0

        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total User Activities", user_activity_count)
        col2.metric("Total Wikimedia Changes", wikimedia_count)
        col3.metric("System Status", "🟢 Online")

        # Charts
        if not df_activity.empty:
            st.subheader("User Activity Trends")
            
            # Bar Chart: Events by Type
            if 'event_type' in df_activity.columns:
                fig_type = px.bar(
                    df_activity['event_type'].value_counts().reset_index(),
                    x='event_type',
                    y='count',
                    title="Events by Type (Last 100)"
                )
                st.plotly_chart(fig_type, use_container_width=True)
            
            # Data Table
            st.subheader("Latest Raw Events")
            st.dataframe(df_activity.drop(columns=['_id'], errors='ignore').head(10))
        else:
            st.info("Waiting for data...")

        time.sleep(REFRESH_RATE)

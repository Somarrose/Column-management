import streamlit as st
import pandas as pd
import psycopg2
import os
# PostgreSQL Connection URL (Replace with your Railway PostgreSQL URL)
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:rNJmKluuNByIxizCMxMzGlsaqqhxnwXo@shinkansen.proxy.rlwy.net:11248/railway")
# Connect to PostgreSQL
try:
   conn = psycopg2.connect(DB_URL)
   cursor = conn.cursor()
   st.success("✅ Connected to PostgreSQL successfully!")
except Exception as e:
   st.error(f"❌ Database connection failed: {e}")
# Streamlit App UI
st.title("📊 Analytical Column Management")
# Sidebar Navigation
menu = ["Home", "Register User", "Register Column", "Usage Entries"]
choice = st.sidebar.selectbox("Navigation", menu)
# Register User
if choice == "Register User":
   st.subheader("👤 Register User")
   name = st.text_input("Name")
   employee_id = st.text_input("Employee ID")
   if st.button("Register"):
       cursor.execute("INSERT INTO user (name, employee_id) VALUES (%s, %s)", (name, employee_id))
       conn.commit()
       st.success(f"User '{name}' registered successfully!")
# Register Analytical Column
elif choice == "Register Column":
   st.subheader("🧪 Register Analytical Column")
   sn = st.text_input("Serial Number")
   reference = st.text_input("Reference")
   supplier = st.text_input("Supplier")
   dimension = st.text_input("Dimension")
   if st.button("Register Column"):
       cursor.execute("INSERT INTO column_info (sn, reference, supplier, dimension) VALUES (%s, %s, %s, %s)",
                     (sn, reference, supplier, dimension))
       conn.commit()
       st.success(f"Column '{reference}' registered successfully!")
# View Usage Entries
elif choice == "Usage Entries":
   st.subheader("📋 Column Usage History")
   try:
       df = pd.read_sql_query("SELECT * FROM usage_entry", conn)
       st.dataframe(df)
   except Exception as e:
       st.error(f"❌ Error fetching data: {e}")
# Home Page
else:
   st.write("Welcome to the **Analytical Column Usage & Inventory** system!")
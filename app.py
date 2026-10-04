import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import json
import sqlite3
import time
from twilio.rest import Client
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime





# Page Configuration
st.set_page_config(
    page_title="SmartReceipt AI | Enterprise Expense Tracker",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional CSS
st.markdown("""
    <style>
    /* Main Background & Font Styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Custom Header Styling */
    .title-text {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .subtitle-text {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 25px;
    }
    
    /* Card Container Styling */
    .css-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    
    /* Metric Card Styling */
    .metric-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.25);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 8px;
        color: #475569;
        font-weight: 600;
        border: 1px solid #E2E8F0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="title-text">🧾 SmartReceipt AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Next-Gen Intelligent Receipt Parsing & Expense Analytics Powered by Gemini 3.8 Flash</div>', unsafe_allow_html=True)

# API Key Setup
API_KEY = st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_NUMBER = st.secrets["TWILIO_WHATSAPP_NUMBER"]
# Sidebar Setup
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/receipt.png", width=80)
    st.title("SmartReceipt AI")
    st.caption("v2.0 Professional Edition")
    st.markdown("---")
    st.header("⚙️ Configuration")
    st.success("🟢 API Engine Online")
    st.info("Model: Gemini 3.8 Flash")
    st.markdown("---")
    st.markdown("Developed for AI Competition 🏆")

# Database Setup
DB_NAME = "smartreceipt.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store TEXT,
            category TEXT,
            date TEXT,
            payment TEXT,
            total REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_expense(store, category, date, payment, total):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (store, category, date, payment, total)
        VALUES (?, ?, ?, ?, ?)
    """, (
        store,
        category,
        date,
        payment,
        total
    ))

    conn.commit()
    conn.close()


def load_expenses():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM expenses ORDER BY id DESC",
        conn
    )

    conn.close()

    return df
def save_setting(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES (?, ?)
    """, (key, str(value)))

    conn.commit()
    conn.close()


def load_setting(key, default_value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM settings WHERE key = ?",
        (key,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return float(result[0])

    return default_value

def create_pdf_report(df):
    file_path = "smartreceipt_report.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(
        50,
        height - 50,
        "SmartReceipt AI - Expense Report"
    )

    c.setFont("Helvetica", 10)

    c.drawString(
        50,
        height - 70,
        f"Total Transactions: {len(df)}"
    )

    total = df["total"].sum()

    c.drawString(
        50,
        height - 85,
        f"Total Spending: Rs. {total:,.2f}"
    )

    y = height - 120

    c.setFont("Helvetica-Bold", 10)

    c.drawString(50, y, "Store")
    c.drawString(180, y, "Category")
    c.drawString(300, y, "Date")
    c.drawString(390, y, "Payment")
    c.drawString(470, y, "Total")

    y -= 20

    c.setFont("Helvetica", 9)

    for _, row in df.iterrows():

        if y < 50:
            c.showPage()
            y = height - 50

        c.drawString(50, y, str(row["store"])[:18])
        c.drawString(180, y, str(row["category"])[:15])
        c.drawString(300, y, str(row["date"])[:12])
        c.drawString(390, y, str(row["payment"])[:10])

        c.drawString(
            470,
            y,
            f"Rs. {float(row['total']):,.2f}"
        )

        y -= 18

    c.save()

    return file_path

    
def send_whatsapp_message(to_number, message):
    try:
        client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )

        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=f"whatsapp:{to_number}"
        )

        return True, "WhatsApp message sent successfully."

    except Exception as e:
        error_message = str(e)

        if "trial accounts have limited parameter access" in error_message:
            return False, "WhatsApp is currently unavailable because the Twilio trial account has messaging restrictions."

        return False, f"WhatsApp could not be sent: {error_message}"
init_database()
# Initialize Session State
if "receipt_history" not in st.session_state:
    st.session_state.receipt_history = []

    # Load existing expenses from database
    existing_expenses = load_expenses()

    if not existing_expenses.empty:
        for _, row in existing_expenses.iterrows():
            st.session_state.receipt_history.append({
                "Store": row["store"],
                "Category": row["category"],
                "Date": row["date"],
                "Payment": row["payment"],
                "Total (₹)": float(row["total"])
            })

# Helper Function for Gemini AI
def analyze_receipt(image, api_key):
    client = genai.Client(api_key=api_key)

    prompt = """
You are an expert AI receipt analysis assistant.

Analyze the attached receipt image carefully and extract all clearly visible information.

Return ONLY valid JSON. Do not use markdown or code fences.

Use this exact structure:

{
  "store_name": "Merchant name",
  "date": "YYYY-MM-DD",
  "payment_method": "Cash/Card/UPI/Unknown",
  "category": "Groceries/Dining/Shopping/Transport/Utilities/Healthcare/Other",
  "items": [
    {
      "name": "Item name",
      "quantity": 1,
      "price": 0.00
    }
  ],
  "subtotal": 0.00,
  "tax_amount": 0.00,
  "total_amount": 0.00
}

Rules:
- Do not invent information that is not visible.
- If a value cannot be identified, use "Unknown" or 0.
- Keep the original currency amount from the receipt.
- Extract every clearly visible item when possible.
- Make sure total_amount is the final receipt total.
"""
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[prompt, image]
            )
            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < 4:
                time.sleep(10)
            else:
                raise
# Top Metrics Row
m1, m2, m3, m4 = st.columns(4)
total_spent = sum([x["Total (₹)"] for x in st.session_state.receipt_history])
total_receipts = len(st.session_state.receipt_history)
avg_spent = total_spent / total_receipts if total_receipts > 0 else 0.0

with m1:
    st.markdown(f'''
        <div class="metric-container">
            <div class="metric-label">Total Spend</div>
            <div class="metric-value">₹{total_spent:,.2f}</div>
        </div>
    ''', unsafe_allow_html=True)

with m2:
    st.markdown(f'''
        <div class="metric-container" style="background: linear-gradient(135deg, #059669 0%, #10B981 100%);">
            <div class="metric-label">Processed Receipts</div>
            <div class="metric-value">{total_receipts}</div>
        </div>
    ''', unsafe_allow_html=True)

with m3:
    st.markdown(f'''
        <div class="metric-container" style="background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);">
            <div class="metric-label">Avg / Receipt</div>
            <div class="metric-value">₹{avg_spent:,.2f}</div>
        </div>
    ''', unsafe_allow_html=True)

with m4:
    st.markdown(f'''
        <div class="metric-container" style="background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%);">
            <div class="metric-label">System Status</div>
            <div class="metric-value">Active</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Upload & Analyze",
    "📊 Expense Analytics",
    "📋 Transaction Logs",
    "🤖 AI Assistant",
    "💰 Budget Manager"
])
# Tab 1: Upload & Analyze
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📤 Upload Document")

        uploaded_file = st.file_uploader(
            "Drop receipt image here (JPG, PNG)",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Document Preview",
                use_container_width=True
            )

    with col2:
        st.markdown("### ⚡ AI Extraction Engine")

        if uploaded_file is not None:

            if st.button(
                "🔍 Extract & Process Receipt",
                type="primary",
                use_container_width=True
            ):

                with st.spinner("Processing image via Gemini Vision AI..."):

                    try:
                        # Send receipt to Gemini
                        raw_result = analyze_receipt(image, API_KEY)

                        # Clean Gemini response
                        cleaned = (
                            raw_result
                            .strip()
                            .removeprefix("```json")
                            .removeprefix("```")
                            .removesuffix("```")
                            .strip()
                        )

                        # Convert JSON text to Python dictionary
                        data = json.loads(cleaned)

                        st.success("Extraction Completed Successfully!")

                        # Receipt Summary
                        st.markdown(
                            f"#### 🏪 {data.get('store_name', 'Unknown Store')}"
                        )

                        st.markdown(
                            f"**Category:** `{data.get('category', 'General')}` | "
                            f"**Date:** {data.get('date', 'N/A')} | "
                            f"**Payment:** `{data.get('payment_method', 'Unknown')}`"
                        )

                        st.markdown("---")

                        # Purchased Items
                        st.markdown("### 🛒 Purchased Items")

                        items = data.get("items", [])

                        if items:
                            items_df = pd.DataFrame(items)

                            items_df = items_df.rename(
                                columns={
                                    "name": "Item",
                                    "quantity": "Qty",
                                    "price": "Price (₹)"
                                }
                            )

                            st.dataframe(
                                items_df,
                                use_container_width=True,
                                hide_index=True
                            )

                        else:
                            st.info("No item details were detected.")

                        # Financial Summary
                        st.markdown("### 💰 Financial Summary")

                        summary_col1, summary_col2, summary_col3 = st.columns(3)

                        with summary_col1:
                            st.metric(
                                "Subtotal",
                                f"₹{float(data.get('subtotal', 0)):,.2f}"
                            )

                        with summary_col2:
                            st.metric(
                                "Tax",
                                f"₹{float(data.get('tax_amount', 0)):,.2f}"
                            )

                        with summary_col3:
                            st.metric(
                                "Total",
                                f"₹{float(data.get('total_amount', 0)):,.2f}"
                            )

                            

                        # Save Expense to Database
                        save_expense(
                            data.get("store_name", "Unknown"),
                            data.get("category", "General"),
                            data.get("date", "N/A"),
                            data.get("payment_method", "N/A"),
                            float(data.get("total_amount", 0.0))
                        )

                        # Store in History
                        st.session_state.receipt_history.append({
                            "Store": data.get("store_name", "Unknown"),
                            "Category": data.get("category", "General"),
                            "Date": data.get("date", "N/A"),
                            "Payment": data.get("payment_method", "N/A"),
                            "Total (₹)": float(
                                data.get("total_amount", 0.0)
                            )
                        })

                        st.rerun()

                    except Exception as e:
                        st.error(f"Processing Error: {e}")

        else:
            st.info(
                "Upload a receipt on the left to begin extraction."
            )

# Tab 2: Dashboard

with tab2:

    st.markdown("## 📊 Expense Dashboard")
    st.caption("AI-powered overview of your spending")

    # Load data from database
    dashboard_df = load_expenses()

    if not dashboard_df.empty:

        # Convert total column to numeric
        dashboard_df["total"] = pd.to_numeric(
            dashboard_df["total"],
            errors="coerce"
        ).fillna(0)

        # ==============================
        # Dashboard Metrics
        # ==============================

        total_spend = dashboard_df["total"].sum()

        total_transactions = len(
            dashboard_df
        )

        average_expense = (
            total_spend / total_transactions
            if total_transactions > 0
            else 0
        )

        highest_expense = dashboard_df["total"].max()

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.metric(
                "💰 Total Spend",
                f"₹{total_spend:,.2f}"
            )

        with metric2:
            st.metric(
                "🧾 Transactions",
                total_transactions
            )

        with metric3:
            st.metric(
                "📈 Average Expense",
                f"₹{average_expense:,.2f}"
            )

        with metric4:
            st.metric(
                "🔝 Highest Expense",
                f"₹{highest_expense:,.2f}"
            )

        st.markdown("---")

        # ==============================
        # Date Conversion
        # ==============================

        dashboard_df["date"] = pd.to_datetime(
            dashboard_df["date"],
            errors="coerce"
        )

        dashboard_df = dashboard_df.dropna(
            subset=["date"]
        )

        # ==============================
        # Date Filter
        # ==============================

        st.markdown("### 📅 Filter Expenses")

        min_date = dashboard_df["date"].min().date()

        max_date = dashboard_df["date"].max().date()

        selected_dates = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if len(selected_dates) == 2:

            start_date, end_date = selected_dates

            filtered_df = dashboard_df[
                (dashboard_df["date"].dt.date >= start_date)
                &
                (dashboard_df["date"].dt.date <= end_date)
            ]

        else:

            filtered_df = dashboard_df.copy()

        st.markdown("---")

        # ==============================
        # Spending Charts
        # ==============================

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.markdown(
                "### 🏷️ Spending by Category"
            )

            category_data = (
                filtered_df
                .groupby("category")["total"]
                .sum()
                .sort_values(ascending=False)
            )

            st.bar_chart(
                category_data
            )

        with chart_col2:

            st.markdown(
                "### 🏪 Spending by Store"
            )

            store_data = (
                filtered_df
                .groupby("store")["total"]
                .sum()
                .sort_values(ascending=False)
            )

            st.bar_chart(
                store_data
            )

        st.markdown("---")

        # ==============================
        # Monthly Spending Trend
        # ==============================

        st.markdown(
            "### 📈 Monthly Spending Trend"
        )

        monthly_data = filtered_df.copy()

        monthly_data["Month"] = (
            monthly_data["date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_spending = (
            monthly_data
            .groupby("Month")["total"]
            .sum()
            .sort_index()
        )

        if not monthly_spending.empty:

            st.line_chart(
                monthly_spending
            )

        else:

            st.info(
                "No spending data available "
                "for the selected dates."
            )

        st.markdown("---")

        # ==============================
        # Recent Transactions
        # ==============================

        st.markdown(
            "### 🕒 Recent Transactions"
        )

        recent_data = (
            dashboard_df
            .head(10)
            .copy()
        )

        recent_data = recent_data.rename(
            columns={
                "store": "Store",
                "category": "Category",
                "date": "Date",
                "payment": "Payment",
                "total": "Amount (₹)"
            }
        )

        st.dataframe(
            recent_data[
                [
                    "Store",
                    "Category",
                    "Date",
                    "Payment",
                    "Amount (₹)"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expense data available yet. "
            "Process your first receipt to build "
            "your dashboard."
        )

   # Tab 3: Expense History & Export
with tab3:

    if len(st.session_state.receipt_history) > 0:

        df = pd.DataFrame(
            st.session_state.receipt_history
        )

        st.markdown("## 📋 Expense History")
        st.caption("Search, filter and export your recorded transactions")

        # -------------------------
        # SEARCH & FILTERS
        # -------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            search_store = st.text_input(
                "🔎 Search Store",
                placeholder="Example: Reliance",
                key="history_store_search"
            )

        with col2:

            categories = ["All"] + sorted(
                df["Category"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_category = st.selectbox(
                "🏷️ Category",
                categories,
                key="history_category_filter"
            )

        with col3:

            payments = ["All"] + sorted(
                df["Payment"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_payment = st.selectbox(
                "💳 Payment Method",
                payments,
                key="history_payment_filter"
            )

        # -------------------------
        # APPLY FILTERS
        # -------------------------

        filtered_df = df.copy()

        if search_store.strip():

            filtered_df = filtered_df[
                filtered_df["Store"]
                .astype(str)
                .str.contains(
                    search_store,
                    case=False,
                    na=False
                )
            ]

        if selected_category != "All":

            filtered_df = filtered_df[
                filtered_df["Category"]
                == selected_category
            ]

        if selected_payment != "All":

            filtered_df = filtered_df[
                filtered_df["Payment"]
                == selected_payment
            ]

        st.markdown("---")

        # -------------------------
        # SUMMARY
        # -------------------------

        filtered_total = filtered_df[
            "Total (₹)"
        ].sum()

        metric1, metric2 = st.columns(2)

        with metric1:

            st.metric(
                "🧾 Transactions",
                len(filtered_df)
            )

        with metric2:

            st.metric(
                "💰 Filtered Spending",
                f"₹{filtered_total:,.2f}"
            )

        st.markdown("---")

        # -------------------------
        # TRANSACTION TABLE
        # -------------------------

        st.markdown("### 📊 Transaction Records")

        if not filtered_df.empty:

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No transactions match the selected filters."
            )

        # -------------------------
        # CSV EXPORT
        # -------------------------

        st.markdown("---")

        st.markdown("### 📥 Export Reports")

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download CSV Report",
            data=csv_data,
            file_name="SmartReceipt_Expense_Report.csv",
            mime="text/csv",
            type="primary",
            key="download_csv_report"
        )

        # -------------------------
        # PDF REPORT
        # -------------------------

        st.markdown("### 📄 PDF Expense Report")

        if not filtered_df.empty:

            if st.button(
                "📄 Generate PDF Report",
                type="primary",
                key="generate_pdf_report"
            ):

                pdf_file = create_pdf_report(
                    filtered_df
                )

                with open(
                    pdf_file,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=file,
                        file_name="SmartReceipt_Expense_Report.pdf",
                        mime="application/pdf",
                        key="download_pdf_report"
                    )

        else:

            st.info(
                "No filtered transactions available for PDF."
            )

        # -------------------------
        # WHATSAPP
        # -------------------------

        st.markdown("---")

        st.markdown("### 📱 WhatsApp Report")

        st.caption(
            "Send the filtered expense summary through WhatsApp."
        )

        if st.button(
            "📲 Send Report to WhatsApp",
            type="primary",
            key="send_whatsapp_report"
        ):

            total_transactions = len(
                filtered_df
            )

            total_amount = filtered_df[
                "Total (₹)"
            ].sum()

            message = (
                "🧾 SmartReceipt AI Expense Report\n\n"
                f"Transactions: {total_transactions}\n"
                f"Total Spending: ₹{total_amount:,.2f}\n\n"
                "Generated by SmartReceipt AI"
            )

            try:

                success, result_message = send_whatsapp_message(
                    message
                )

                if success:

                    st.success(
                        result_message
                    )

                else:

                    st.error(
                        result_message
                    )

            except Exception as e:

                st.error(
                    f"WhatsApp Error: {e}"
                )

    else:

        st.info(
            "📭 No expense history found. "
            "Upload and analyze a receipt first."
        )
      # Tab 4: AI Assistant
with tab4:

    st.markdown("## 🤖 AI Expense Assistant")
    st.caption("Ask questions about your recorded expenses")

    user_question = st.text_input(
        "💬 Ask your expense question",
        placeholder="Example: Where did I spend the most?",
        key="ai_expense_question"
    )

    if st.button(
        "✨ Ask AI",
        type="primary",
        key="ask_ai_button"
    ):

        if not user_question.strip():

            st.warning("Please enter a question.")

        else:

            expense_data = load_expenses()

            if expense_data.empty:

                st.info(
                    "No expense data available. "
                    "Process some receipts first."
                )

            else:

                expense_context = expense_data.to_string(
                    index=False
                )

                assistant_prompt = f"""
You are SmartReceipt AI, an intelligent personal
expense analysis assistant.

Expense records:

{expense_context}

User question:
{user_question}

Rules:
- Use only the provided expense records.
- Do not invent transactions.
- Give concise and useful answers.
- Mention amounts in Indian Rupees (₹).
"""

                with st.spinner(
                    "🤖 AI is analyzing your expenses..."
                ):

                    try:

                        client = genai.Client(
                            api_key=API_KEY
                        )

                        response = None

                        for attempt in range(3):

                            try:

                                response = client.models.generate_content(
                                    model="gemini-3.8-flash",
                                    contents=assistant_prompt
                                )

                                break

                            except Exception as e:

                                if "503" in str(e) and attempt < 2:

                                    import time
                                    time.sleep(8)

                                else:

                                    raise

                        st.markdown("### 💡 AI Insight")

                        st.write(response.text)

                    except Exception as e:

                        st.error(
                            f"AI Assistant Error: {e}"
                        )

# Tab 5: Budget Manager
with tab5:

    st.markdown("## 💰 Budget Manager")
    st.caption("Set your monthly budget and monitor your spending")

    # -------------------------
    # MONTHLY BUDGET
    # -------------------------

    saved_budget = load_setting(
        "monthly_budget",
        10000.0
    )

    budget = st.number_input(
        "💰 Monthly Budget (₹)",
        min_value=0.0,
        value=saved_budget,
        step=500.0,
        key="monthly_budget_input"
    )

    save_setting(
        "monthly_budget",
        budget
    )

    st.markdown("---")

    # -------------------------
    # LOAD CURRENT MONTH DATA
    # -------------------------

    expense_data = load_expenses()

    if not expense_data.empty:

        expense_data["date"] = pd.to_datetime(
            expense_data["date"],
            errors="coerce"
        )

        expense_data = expense_data.dropna(
            subset=["date"]
        )

        current_month = datetime.now().month
        current_year = datetime.now().year

        expense_data = expense_data[
            (expense_data["date"].dt.month == current_month)
            &
            (expense_data["date"].dt.year == current_year)
        ]

        expense_data["total"] = pd.to_numeric(
            expense_data["total"],
            errors="coerce"
        ).fillna(0)

    # -------------------------
    # SPENDING SUMMARY
    # -------------------------

    if not expense_data.empty:

        total_spent = expense_data["total"].sum()

        remaining = budget - total_spent

        usage_percentage = (
            (total_spent / budget) * 100
            if budget > 0
            else 0
        )

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "💰 Monthly Budget",
                f"₹{budget:,.2f}"
            )

        with metric2:

            st.metric(
                "💸 Spent",
                f"₹{total_spent:,.2f}"
            )

        with metric3:

            st.metric(
                "💵 Remaining",
                f"₹{remaining:,.2f}"
            )

        st.markdown("---")

        # -------------------------
        # BUDGET PROGRESS
        # -------------------------

        st.markdown("### 📊 Budget Usage")

        progress_value = min(
            usage_percentage / 100,
            1.0
        )

        st.progress(progress_value)

        st.write(
            f"Budget used: **{usage_percentage:.1f}%**"
        )

        if usage_percentage >= 100:

            st.error(
                "🚨 You have exceeded your monthly budget."
            )

        elif usage_percentage >= 80:

            st.warning(
                "⚠️ You have used more than 80% of your budget."
            )

        else:

            st.success(
                "✅ Your spending is within the budget."
            )

        # -------------------------
        # CATEGORY BUDGETS
        # -------------------------

        st.markdown("---")

        st.markdown("### 🏷️ Category Budgets")

        budget_categories = [
            "Groceries",
            "Dining",
            "Shopping",
            "Transport",
            "Utilities",
            "Healthcare",
            "Other"
        ]

        category_budgets = {}

        budget_cols = st.columns(2)

        for index, category in enumerate(
            budget_categories
        ):

            saved_category_budget = load_setting(
                f"budget_{category}",
                0.0
            )

            with budget_cols[index % 2]:

                category_budgets[category] = st.number_input(
                    f"{category} Budget (₹)",
                    min_value=0.0,
                    value=saved_category_budget,
                    step=500.0,
                    key=f"budget_{category}"
                )

                save_setting(
                    f"budget_{category}",
                    category_budgets[category]
                )

        st.markdown("---")

        # -------------------------
        # CATEGORY STATUS
        # -------------------------

        st.markdown("### 📌 Category Status")

        category_summary = (
            expense_data
            .groupby("category")["total"]
            .sum()
            .sort_values(ascending=False)
        )

        for category in budget_categories:

            spent = category_summary.get(
                category,
                0
            )

            category_budget = category_budgets.get(
                category,
                0
            )

            if category_budget > 0:

                category_usage = (
                    spent / category_budget
                ) * 100

                if spent > category_budget:

                    st.error(
                        f"🚨 {category}: "
                        f"₹{spent:,.2f} / "
                        f"₹{category_budget:,.2f} "
                        f"({category_usage:.1f}%)"
                    )

                elif category_usage >= 80:

                    st.warning(
                        f"⚠️ {category}: "
                        f"₹{spent:,.2f} / "
                        f"₹{category_budget:,.2f} "
                        f"({category_usage:.1f}%)"
                    )

                else:

                    st.success(
                        f"✅ {category}: "
                        f"₹{spent:,.2f} / "
                        f"₹{category_budget:,.2f} "
                        f"({category_usage:.1f}%)"
                    )

        # -------------------------
        # SMART SPENDING INSIGHTS
        # -------------------------

        st.markdown("---")

        st.markdown("### 🧠 Smart Spending Insights")

        if not category_summary.empty:

            top_category = category_summary.index[0]

            top_category_amount = (
                category_summary.iloc[0]
            )

            st.info(
                f"💡 Highest spending category: "
                f"**{top_category}** — "
                f"₹{top_category_amount:,.2f}"
            )

        highest_transaction = expense_data.loc[
            expense_data["total"].idxmax()
        ]

        st.info(
            f"🔎 Highest transaction: "
            f"**₹{highest_transaction['total']:,.2f}** "
            f"at **{highest_transaction['store']}**"
        )

        store_summary = (
            expense_data
            .groupby("store")["total"]
            .sum()
            .sort_values(ascending=False)
        )

        if not store_summary.empty:

            top_store = store_summary.index[0]

            top_store_amount = (
                store_summary.iloc[0]
            )

            st.info(
                f"🏪 Highest spending store: "
                f"**{top_store}** — "
                f"₹{top_store_amount:,.2f}"
            )

        # -------------------------
        # SAVINGS STATUS
        # -------------------------

        st.markdown("---")

        if remaining > 0:

            st.success(
                f"💚 You still have "
                f"**₹{remaining:,.2f}** "
                f"available in this month's budget."
            )

        elif remaining == 0:

            st.warning(
                "⚠️ You have used your entire monthly budget."
            )

        else:

            st.error(
                f"🚨 You are "
                f"**₹{abs(remaining):,.2f}** "
                f"over your monthly budget."
            )

    else:

        st.info(
            "📭 No expenses recorded for the current month."
        )

        st.write(
            "Upload and analyze receipts to start tracking your budget."
        )
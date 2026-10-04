# 🧾 SmartReceipt AI

> **AI-Powered Receipt Analysis & Smart Expense Management Platform**

SmartReceipt AI is an intelligent expense management platform that uses **Google Gemini AI** to analyze receipt images, automatically extract transaction information, store expense records, and provide actionable spending insights.

The platform is designed to make expense tracking **faster, smarter, and easier** by combining AI-powered receipt understanding with a professional analytics dashboard.

---

## 🚀 Why SmartReceipt AI?

Managing expenses manually can be time-consuming and error-prone.

Users often need to:

* Read receipts manually
* Enter expenses one by one
* Categorize transactions
* Track monthly spending
* Calculate totals
* Generate reports
* Understand where their money is going

**SmartReceipt AI automates much of this workflow.**

Simply upload a receipt → AI analyzes it → structured expense data is created → the transaction is stored → dashboards and insights help understand spending.

---

## ✨ Key Features

### 🤖 AI Receipt Analysis

Upload a receipt image and Gemini AI extracts structured information such as:

* Store / merchant name
* Date
* Payment method
* Expense category
* Purchased items
* Quantity
* Item prices
* Subtotal
* Tax
* Final total

The application is designed to avoid inventing information when details are not visible on the receipt.

---

### 📊 Expense Dashboard

The analytics dashboard provides an overview of recorded expenses.

Includes:

* Total spending
* Total transactions
* Average expense
* Highest expense
* Category analysis
* Store analysis
* Spending trends
* Date-range filtering
* Recent transactions

---

### 📋 Expense History

All processed transactions can be viewed in a centralized history.

Users can:

* Search by store
* Filter by category
* Filter by payment method
* View filtered transaction totals
* Review complete transaction records

---

### 🤖 AI Expense Assistant

SmartReceipt AI includes an AI assistant that can answer questions based on recorded expense data.

Example questions:

* Where did I spend the most?
* Which category has the highest spending?
* What was my highest transaction?
* How much did I spend?

The assistant uses the available expense records as its context rather than inventing transactions.

---

### 💰 Budget Manager

Set and monitor a monthly spending budget.

Features include:

* Monthly budget
* Current-month spending
* Remaining budget
* Budget usage percentage
* Spending warnings
* Category-level budgets
* Category spending status
* Savings status

The system also highlights important spending patterns.

---

### 🧠 Smart Spending Insights

The platform identifies useful patterns such as:

* Highest spending category
* Highest individual transaction
* Highest spending store
* Current-month spending

These insights help users understand their spending behavior more easily.

---

### 📄 Expense Reports

Generate downloadable reports in:

* CSV
* PDF

Reports can be used for personal tracking, documentation, or further analysis.

---

### 📱 WhatsApp Integration

The project includes Twilio WhatsApp integration for sending expense summaries.

> **Note:** WhatsApp messaging availability depends on the Twilio account and messaging configuration.

---

### 🔐 Security

Sensitive credentials are kept outside the source code.

The project uses:

* Streamlit secrets
* `.gitignore`
* Environment-safe configuration
* Protected API credentials

Sensitive files such as:

```text
.streamlit/secrets.toml
.env
smartreceipt.db
```

are excluded from Git tracking.

---

## 🛠️ Technology Stack

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| Python        | Core application development              |
| Streamlit     | Web application interface                 |
| Google Gemini | AI receipt analysis and expense assistant |
| SQLite        | Local expense database                    |
| Pandas        | Data processing and analytics             |
| ReportLab     | PDF report generation                     |
| Twilio        | WhatsApp integration                      |
| Git           | Version control                           |
| GitHub        | Source code management                    |

---

## 🏗️ Application Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Streamlit Web App   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Receipt Upload     Expense Assistant   Budget Manager
             │                 │                 │
             ▼                 ▼                 │
       Gemini AI          Gemini AI              │
             │                 │                 │
             └────────────┬────┘                 │
                          ▼                      │
                   Structured Data              │
                          │                      │
                          ▼                      ▼
                    ┌────────────────────────────┐
                    │          SQLite             │
                    │      Expense Database       │
                    └──────────────┬─────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
                 Dashboard     Reports        Insights
                    │              │
                    ▼              ▼
                 Analytics      CSV / PDF
```

---

## 📂 Project Structure

```text
SmartReceipt-AI/
│
├── app.py
│
├── .gitignore
│
├── .streamlit/
│   └── secrets.toml
│
└── README.md
```

### Generated / Local Files

The application may generate local files such as:

```text
smartreceipt.db
smartreceipt_report.pdf
```

These are intentionally excluded from Git tracking.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/jnvishali294/SmartReceipt-AI.git
```

### 2. Open the project

```bash
cd SmartReceipt-AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

---

## 📦 Install Dependencies

Install the required packages:

```bash
pip install streamlit google-genai pillow pandas twilio reportlab
```

---

## 🔑 Configure API Keys

Create:

```text
.streamlit/secrets.toml
```

Add your credentials:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "YOUR_TWILIO_WHATSAPP_NUMBER"
```

### ⚠️ Important

Never commit `secrets.toml` to GitHub.

The project already ignores it through:

```text
.streamlit/secrets.toml
```

---

## ▶️ Run the Application

Start Streamlit:

```bash
python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 🧪 How It Works

### Step 1 — Upload Receipt

The user uploads a receipt image.

### Step 2 — AI Analysis

Gemini analyzes the receipt and extracts structured information.

### Step 3 — Data Processing

The application converts the AI response into structured expense data.

### Step 4 — Database Storage

The transaction is stored in SQLite.

### Step 5 — Analytics

The dashboard processes the stored transactions to calculate:

* Spending totals
* Category totals
* Store totals
* Average expenses
* Spending trends

### Step 6 — AI Insights

The AI Expense Assistant uses stored transaction data to answer expense-related questions.

### Step 7 — Reports

Users can export their expense information as CSV or PDF.

---

## 🎯 Project Goals

SmartReceipt AI aims to demonstrate how modern AI can be integrated into a practical software product.

The project focuses on:

* AI integration
* Computer vision-based document understanding
* Data extraction
* Database management
* Data analytics
* Budget management
* AI-powered insights
* Report generation
* API integration
* Secure credential management
* Version control
* Software development practices

---

## 🔮 Future Improvements

Planned improvements include:

* ☁️ Cloud deployment
* 📱 Improved mobile experience
* 🔐 User authentication
* 👥 Multi-user expense accounts
* 📈 Advanced analytics
* 🧠 More personalized financial insights
* 🔔 Automated notifications
* 🗃️ Cloud database support
* 📊 Advanced financial visualizations
* 🧾 Improved receipt handling
* 🔎 Advanced transaction search
* 🏦 Additional financial integrations

---

## 🏆 Project Use Cases

SmartReceipt AI can be useful for:

* Students
* Individuals
* Families
* Small businesses
* Freelancers
* Personal finance tracking
* Expense documentation

---

## 🌟 What Makes This Project Different?

SmartReceipt AI combines several software engineering concepts into one practical application:

```text
Receipt Image
     ↓
Gemini AI
     ↓
Structured Data
     ↓
SQLite Database
     ↓
Analytics
     ↓
Budget Monitoring
     ↓
AI Insights
     ↓
CSV / PDF Reports
```

Instead of being only a receipt scanner, the project aims to provide a complete **AI-assisted expense management workflow**.

---

## 🔒 Security Note

Do not upload or commit:

```text
.streamlit/secrets.toml
.env
API keys
Access tokens
Private credentials
```

If credentials are accidentally exposed, revoke and replace them immediately.

---

## 📌 Project Status

**Current Status:** 🚧 Active Development

Core functionality includes:

* [x] AI receipt analysis
* [x] Structured expense extraction
* [x] SQLite expense storage
* [x] Expense history
* [x] Search and filtering
* [x] Expense dashboard
* [x] AI Expense Assistant
* [x] Monthly budget manager
* [x] Category budgets
* [x] CSV export
* [x] PDF reports
* [x] Git/GitHub integration
* [x] Secure secret handling
* [ ] Production deployment
* [ ] Advanced authentication
* [ ] Expanded notification system

---

## 👩‍💻 Author

**Vishali JN**

SmartReceipt AI — AI-powered expense management project.

---

## 📜 License

This project is currently intended for educational, portfolio, and project-development purposes.

A formal open-source license can be added when the project is ready for public distribution.

---

## ⭐ Support the Project

If you find SmartReceipt AI interesting, consider giving the repository a ⭐ on GitHub.

Feedback, ideas, and improvements are welcome.

# 📊 InsightSphere

**An AI-powered business intelligence dashboard.** Upload any sales file and instantly get clean data, key metrics, charts, plain-English insights, and an AI assistant you can ask questions to.

**🔗 Live Demo:** https://insightsphere-4ffyceynrc7vmxwfriiq3q.streamlit.app/

---

## ✨ What it does

InsightSphere turns a raw CSV or Excel sales file into a full business intelligence dashboard, automatically:

- 🧹 **Cleans and validates** messy data — missing values, duplicates, inconsistent formatting
- 📈 **Calculates key metrics** — total revenue, orders, average order value, top products, top cities
- 📊 **Generates charts** — sales trends, revenue by city/category, top products
- 💡 **Writes plain-English insights** — turns numbers into sentences a manager can act on
- 🤖 **Answers questions** — a built-in AI assistant (powered by Groq/LLaMA) you can ask about your data
- 📄 **Exports reports** — download your data and insights as CSV, Excel, or PDF

No technical knowledge required — just upload a file and explore.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| 🎨 Frontend | Streamlit, custom CSS (glassmorphism UI) |
| 🐼 Data processing | Pandas |
| 📉 Visualization | Plotly |
| 🧠 AI Assistant | Groq API (LLaMA 3.3) |
| 📑 Reports | ReportLab (PDF), OpenPyXL (Excel) |

---

## 📂 Project Structure

```
InsightSphere/
├── app.py                  # Main Streamlit app
├── modules/
│   ├── loader.py           # Reads uploaded CSV/Excel files
│   ├── validator.py        # Checks data validity
│   ├── cleaner.py          # Cleans and standardizes data
│   ├── analyzer.py         # Calculates KPIs and creates features
│   ├── visualizer.py       # Generates charts
│   ├── insights.py         # Turns KPIs into plain-English insights
│   ├── query.py            # Predefined search/query functions
│   ├── exporter.py         # CSV/Excel/PDF export
│   ├── ai_assistant.py     # AI chat assistant (Groq)
│   └── theme.py            # Custom UI theme and styling
├── requirements.txt
└── README.md
```

---

## 🚀 Running it locally

**1️⃣ Clone the repository**
```bash
git clone https://github.com/mhammad-code/InsightSphere.git
cd InsightSphere
```

**2️⃣ Create a virtual environment and install dependencies**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

**3️⃣ Add your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

**4️⃣ Run the app**
```bash
streamlit run app.py
```

---

## 🧪 Try it out

Don't have a sales file handy? Use a sample CSV with columns like `OrderID, Date, Product, Category, Price, Quantity, City` — InsightSphere will auto-detect the relevant columns regardless of exact naming.

---

## 👤 Author

Built by [Hammad](https://github.com/mhammad-code) — Software Engineering student at COMSATS University Islamabad, Lahore Campus.
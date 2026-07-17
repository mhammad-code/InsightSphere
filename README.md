
```markdown
<h1 align="center">📊 InsightSphere</h1>
<h3 align="center">Simple Business Insights Dashboard</h3>

<p align="center">
  An interactive, intelligent Business Intelligence (BI) dashboard that combines dynamic data analytics with a natural language AI agent to bring sales data to life.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&amp;logo=streamlit&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq%20API-F55036?style=for-the-badge&amp;logo=meta&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

---

## 📖 Overview

**InsightSphere** is a professional data analytics platform built to transform messy transactional sales documents into clean, actionable business decisions. Users can drop in transactional records, apply dynamic local filters, view automated KPI metrics, and converse with an onboard automated AI data analyst. The platform features an intelligent dual-encoding system fallback engine to automatically prevent parsing crashes on historical retail datasets.

---

## ✨ Key Features

- 💬 **AI Intelligent Agent** — integrated **Llama 3.3** via the **Groq API** to analyze high-level summaries and answer natural language data questions on demand
- 🇵🇰 **PKR Local Currency Formatting** — explicit AI engineering instructions ensuring all pricing, revenue figures, and margins are displayed in standard Pakistani Rupee (PKR) formats
- 🔄 **High-Performance Caching** — utilizes Streamlit's `@st.cache_data` and raw `io.BytesIO` streams to stop redundant file reading and provide fast navigation between pages
- 🛠️ **Dual-Encoding Fallback Logic** — catches structural `UnicodeDecodeError` drops and auto-recovers using a robust secondary `latin1` decoding stream
- 📊 **Dynamic Locked Visualizations** — renders beautiful timeline trends, distribution matrix breakdowns, and analyst correlation heatmaps built using `Plotly Express`
- 💾 **Multi-Format Document Exporter** — compiles filtered business states directly into stylized Excel matrices, printable PDFs, or clean standard CSV rows

---

## 🏗️ How It Works

1. A raw sales spreadsheet file (CSV or XLSX format) is uploaded into the dashboard interface.
2. The column identification algorithm maps disparate headers to uniform data types (City, Category, Dates, Revenue).
3. Metric calculations process absolute KPIs, multi-select side filters reduce rows, and chart render engines layout visualizations.
4. The conversational state serializes key summaries into standard native integers/floats via a custom fallback `JSONEncoder` block.
5. The compiled clean profile is packed into system context parameters for the conversational Groq interface to answer queries securely.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Dashboard Engine | Streamlit |
| Data Manipulation | Pandas, NumPy |
| Interactive Visuals | Plotly Express |
| LLM Integration | Llama 3.3 via Groq API Cloud |
| Report Compiler | ReportLab (PDF), Openpyxl (Excel) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip
- A Groq Cloud API Key

### Installation

```bash
git clone [https://github.com/mhammad-code/InsightSphere.git](https://github.com/mhammad-code/InsightSphere.git)
cd InsightSphere
pip install -r requirements.txt

```

### Configuration

Create a `.env` file in the project root directory and insert your authentication key:

```env
GROQ_API_KEY=your_groq_api_key_here

```

### Run the project

```bash
streamlit run app.py

```

---

## 📂 Project Structure

```text
├── .env                       # Local Secrets (Git-ignored)
├── app.py                     # Main dashboard entrypoint & page router
├── requirements.txt           # Application dependencies
├── modules/
│   ├── ai_assistant.py        # Groq LLaMA integration & SafeJSON Encoder
│   ├── analyzer.py            # Automated KPI calculation & dynamic columns
│   ├── cleaner.py             # Data clean-up & normalization algorithms
│   ├── exporter.py            # Excel, PDF, and CSV compiler
│   ├── loader.py              # Robust dual-encoding file-reader
│   ├── theme.py               # Custom CSS UI design rules & templates
│   ├── validator.py           # Integrity and null-value checking
│   └── visualizer.py          # Plotly layout configurations

```

---

## 📸 Screenshots

> Add screenshots or a short demo GIF of the dashboard panels here once available.

---

## 📌 Future Improvements

* Support automated predictive forecasting using seasonal ARIMA models
* Enable drag-and-drop structural cross-filtering modules
* Build support for connecting directly to online relational SQL instances

---

## 👤 Author

**Muhammad Hammad Hussain**
📧 mhammadhussain81@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/hammad-h-b0ab66282) · [GitHub](https://github.com/mhammad-code)

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute with attribution.

```

```

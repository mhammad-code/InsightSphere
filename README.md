
<h1 align="center">📊 InsightSphere</h1>
<h3 align="center">Simple Business Insights Dashboard</h3>

<p align="center">
  An interactive, intelligent Business Intelligence (BI) dashboard that combines dynamic data analytics with a natural language AI agent to bring sales data to life.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&amp;logo=streamlit&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq%20API-F55036?style=for-the-badge&amp;logo=meta&amp;logoColor=white"/>
</p>

---

## 🔗 Live Demo

Experience the dashboard live in your browser:
🚀 **[Launch InsightSphere App](https://insightsphere-4ffyceynrc7vmxwfriiq3q.streamlit.app/)**

---

## 📖 Overview

**InsightSphere** is a simple data analytics tool built to turn messy sales files into clear business choices. Users can upload sales records, filter data by different categories, view instant charts, and chat directly with an AI data assistant. The app also includes smart file-reading tricks to prevent errors and crashes when uploading older data files.

---

## ✨ Key Features

- 💬 **AI Data Assistant** — Chat directly with your data using Llama 3.3 to get fast, smart answers to your business questions.
- 🇵🇰 **PKR Currency** — All money figures, profits, and revenue are automatically shown in Pakistani Rupees (PKR).
- 🔄 **Fast Performance** — Uses smart caching to load your files quickly and keep switching between pages smooth.
- 🛠️ **No More Crashes** — Automatically detects and fixes file encoding issues so your CSV or Excel files load without errors.
- 📊 **Interactive Charts** — View clear, beautiful timelines, sales breakdowns, and charts built with Plotly.
- 💾 **Easy Exports** — Save your filtered data directly into ready-to-use Excel files, clean PDFs, or standard CSV rows.

---

## 🏗️ How It Works

1. Upload any CSV or Excel sales file into the dashboard.
2. The app automatically finds important columns like City, Category, Dates, and Sales.
3. The dashboard instantly updates your KPIs, charts, and filters.
4. The data summary is securely formatted and shared with the AI engine.
5. Ask any question in the chat box to get clean, professional business insights.

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

Create a `.env` file in the project root directory and add your key:

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

## 📌 Future Improvements

* Add automated sales forecasting to predict future trends.
* Enable more advanced drag-and-drop filtering options.
* Connect the app directly to live SQL databases.

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

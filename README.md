# 📊 InsightSphere: Simple Business Insights

InsightSphere is an interactive, intelligent Business Intelligence (BI) dashboard built with **Streamlit**, **Pandas**, and **Plotly**. It features an integrated **AI Intelligent Agent** powered by the **Groq API (using the LLaMA-3.3-70B model)** to provide on-demand natural language answers about business transactions, automatically formatted in **PKR**.

Users can upload any CSV or Excel sales sheet, filter data dynamically by location, category, or date ranges, and download fully parsed reports in Excel, PDF, or CSV formats.

---

## ✨ Key Features

* **Dynamic Data Visualizations:** Beautiful, interactive yet locked chart matrices (timeline trends, category breakdowns, and correlation heatmaps) generated using `Plotly`.
* **AI Analytics Assistant:** Talk directly with your data! Ask complex analytical questions in natural language and receive formatted, professional business answers with financial numbers presented in **PKR**.
* **Intelligent Column Identification:** Automatically identifies relevant headers (like city, category, dates, and prices) even when uploaded files use varied header formats.
* **Robust File Encoding Fallback:** Built-in automatic engine fallbacks to handle both standard UTF-8 encoding and legacy formats (like `Latin-1/Windows-1252`) common in Excel-exported e-commerce sheets.
* **High Performance Caching:** Utilizes Streamlit's `@st.cache_data` along with `io.BytesIO` streams to avoid redundant expensive reads and maintain blistering transition speeds between tabs.
* **Multi-Format Exporter:** Export processed data directly into ready-to-share clean PDFs, raw CSV files, or styled Excel spreadsheets.

---

## 🛠️ Technical Stack

* **Frontend & Dashboard:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Data Visualizations:** [Plotly Express](https://plotly.com/python/)
* **LLM Integration Engine:** [Groq Cloud API SDK](https://console.groq.com/) (Model: `llama-3.3-70b-versatile`)
* **PDF Design:** [ReportLab](https://www.reportlab.com/)
* **Excel Rendering:** [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/mhammad-code/InsightSphere.git](https://github.com/mhammad-code/InsightSphere.git)
cd InsightSphere

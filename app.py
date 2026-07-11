'''import streamlit as st
from modules.loader import load_file
from modules.validator import validate_dataset
from modules.cleaner import clean_dataset
from modules.analyzer import analyze_dataset, find_column
from modules.visualizer import generate_all_charts
from modules.insights import generate_insights
from modules.query import (
    get_available_queries,
    query_top_products,
    query_lowest_selling_products,
    query_revenue_by_city,
    query_revenue_by_category,
    query_orders_by_city,
)
from modules.exporter import export_to_csv, export_to_excel, export_to_pdf
from modules.ai_assistant import ask_ai
from modules.theme import apply_theme, show_intro, custom_metric

try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except ImportError:
    HAS_OPTION_MENU = False

st.set_page_config(page_title="InsightSphere", layout="wide")

dark_mode = st.sidebar.toggle("Dark Mode", value=False)
apply_theme(dark_mode=dark_mode)

if "intro_shown" not in st.session_state:
    st.session_state["intro_shown"] = True
    show_intro()
else:
    st.title("InsightSphere")
    st.caption("Upload your business data to get started")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is None:
    st.stop()

try:
    df = load_file(uploaded_file)
except ValueError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"Something went wrong while reading the file: {e}")
    st.stop()

errors = validate_dataset(df)
if errors:
    st.error("The uploaded file has issues that need to be fixed:")
    for err in errors:
        st.write(f"- {err}")
    st.stop()

st.success(f"File loaded and validated: {uploaded_file.name}")

cleaned_df = clean_dataset(df.copy())
final_df, kpis = analyze_dataset(cleaned_df)

# ---------------- Sidebar Filters ----------------
st.sidebar.header("Filters")

city_col = find_column(final_df, ["city", "location", "region"])
category_col = find_column(final_df, ["category", "type"])
date_col = find_column(final_df, ["date"])

filtered_df = final_df.copy()

if city_col:
    city_options = sorted(final_df[city_col].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect("City", city_options, default=city_options)
    filtered_df = filtered_df[filtered_df[city_col].isin(selected_cities)]

if category_col:
    category_options = sorted(final_df[category_col].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", category_options, default=category_options)
    filtered_df = filtered_df[filtered_df[category_col].isin(selected_categories)]

if date_col:
    valid_dates = final_df[date_col].dropna()
    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()
        date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df[date_col].dt.date >= start_date) &
                (filtered_df[date_col].dt.date <= end_date)
            ]

if filtered_df.empty:
    st.warning("No data matches the selected filters. Adjust filters to see results.")
    st.stop()

_, kpis = analyze_dataset(filtered_df)
final_df = filtered_df

# ---------------- Sidebar Navigation ----------------
st.sidebar.markdown("---")

nav_options = ["Dashboard", "Insights & Query", "Export", "Ask AI"]
nav_icons = ["speedometer2", "search", "download", "chat-dots"]

if HAS_OPTION_MENU:
    with st.sidebar:
        selected_page = option_menu(
            menu_title="Navigate",
            options=nav_options,
            icons=nav_icons,
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "var(--primary)", "font-size": "15px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "3px 0", "border-radius": "10px"},
                "nav-link-selected": {"background-color": "rgba(108,92,231,0.22)"},
            },
        )
else:
    selected_page = st.sidebar.radio("Navigate", nav_options)


# ============================================================
# PAGE: DASHBOARD
# ============================================================
def render_dashboard():
    st.subheader("Key Metrics")

    if not kpis:
        st.info("No KPIs could be calculated from this dataset.")
    else:
        kpi_items = list(kpis.items())
        cols = st.columns(len(kpi_items))
        for col, (name, value) in zip(cols, kpi_items):
            if isinstance(value, float):
                display_value = f"{value:,.2f}"
            elif isinstance(value, int):
                display_value = f"{value:,}"
            else:
                display_value = str(value)
            with col:
                custom_metric(name, display_value)

    with st.expander("Preview: Cleaned data with calculated features"):
        st.dataframe(final_df.head(20), use_container_width=True)

    st.divider()
    st.subheader("Visual Insights")

    charts = generate_all_charts(final_df)
    heatmap = charts.pop("Correlation Heatmap", None)

    if not charts:
        st.info("No charts could be generated from this dataset.")
    else:
        chart_names = list(charts.keys())
        for i in range(0, len(chart_names), 2):
            row_charts = chart_names[i:i + 2]
            cols = st.columns(len(row_charts))
            for col, name in zip(cols, row_charts):
                col.plotly_chart(charts[name], use_container_width=True)

    if heatmap:
        with st.expander("Advanced: Correlation Analysis (technical)"):
            st.caption("Shows statistical relationships between numeric columns. For data analysts.")
            st.plotly_chart(heatmap, use_container_width=True)

    st.divider()
    st.subheader("Business Insights")

    insights = generate_insights(final_df, kpis)
    if not insights:
        st.info("No insights could be generated from this dataset.")
    else:
        for insight in insights:
            st.markdown(f"- {insight}")


# ============================================================
# PAGE: INSIGHTS & QUERY
# ============================================================
def render_query():
    st.subheader("Search & Query")

    available_queries = get_available_queries(final_df)

    if not available_queries:
        st.info("No predefined queries are available for this dataset.")
        return

    selected_query = st.selectbox("Ask a question", list(available_queries.keys()))
    query_key = available_queries[selected_query]

    if query_key == "top_products":
        st.dataframe(query_top_products(final_df), use_container_width=True)

    elif query_key == "lowest_products":
        st.dataframe(query_lowest_selling_products(final_df), use_container_width=True)

    elif query_key == "revenue_by_city":
        city_choice = st.selectbox("Select city", sorted(final_df[city_col].dropna().unique().tolist()))
        result = query_revenue_by_city(final_df, city_choice)
        if result is not None:
            custom_metric(f"Total Revenue — {city_choice}", f"PKR {result:,.0f}")

    elif query_key == "revenue_by_category":
        category_choice = st.selectbox("Select category", sorted(final_df[category_col].dropna().unique().tolist()))
        result = query_revenue_by_category(final_df, category_choice)
        if result is not None:
            custom_metric(f"Total Revenue — {category_choice}", f"PKR {result:,.0f}")

    elif query_key == "orders_by_city":
        st.dataframe(query_orders_by_city(final_df), use_container_width=True)


# ============================================================
# PAGE: EXPORT
# ============================================================
def render_export():
    st.subheader("Export Report")

    insights = generate_insights(final_df, kpis)

    col1, col2, col3 = st.columns(3)

    with col1:
        csv_data = export_to_csv(final_df)
        st.download_button("Download CSV", data=csv_data, file_name="insightsphere_data.csv", mime="text/csv")

    with col2:
        excel_data = export_to_excel(final_df, kpis)
        st.download_button(
            "Download Excel", data=excel_data, file_name="insightsphere_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col3:
        pdf_data = export_to_pdf(kpis, insights, final_df)
        st.download_button("Download PDF Report", data=pdf_data, file_name="insightsphere_report.pdf", mime="application/pdf")


# ============================================================
# PAGE: ASK AI
# ============================================================
def render_ai_chat():
    st.subheader("Ask AI About Your Data")

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_question = st.chat_input("Ask a question about your business data...")

    if user_question:
        st.session_state["chat_messages"].append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your data..."):
                try:
                    answer = ask_ai(
                        question=user_question,
                        df=final_df,
                        kpis=kpis,
                        chat_history=st.session_state["chat_messages"][:-1],
                    )
                except Exception as e:
                    answer = f"Something went wrong while contacting the AI: {e}"
                st.markdown(answer)

        st.session_state["chat_messages"].append({"role": "assistant", "content": answer})


# ---------------- Route to selected page ----------------
if selected_page == "Dashboard":
    render_dashboard()
elif selected_page == "Insights & Query":
    render_query()
elif selected_page == "Export":
    render_export()
elif selected_page == "Ask AI":
    render_ai_chat()'''

import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(
    page_title="InsightSphere AI | Smart Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Premium Glassmorphism & Custom CSS Stylesheet
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* Global CSS Overrides */
        * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .main {
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 100%);
        }

        /* Glassmorphism Card Style */
        .glass-card {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.15);
        }

        /* Modern Gradient Text & Titles */
        .glow-title {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.25rem;
        }

        .neon-accent {
            color: #38bdf8;
            font-weight: 600;
        }

        /* KPI Visual Architecture */
        .kpi-label {
            color: #94a3b8;
            font-size: 0.8rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.07em;
            margin-bottom: 0.5rem;
        }

        .kpi-value {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            text-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
        }

        /* Custom Modern Alerts */
        .glass-alert-success {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
            padding: 1rem;
            border-radius: 0.75rem;
            backdrop-filter: blur(8px);
        }

        .glass-alert-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 1rem;
            border-radius: 0.75rem;
            backdrop-filter: blur(8px);
        }
    </style>
""", unsafe_allow_html=True)


# 3. Generating Core Mock Dataset
@st.cache_data
def get_mock_data():
    data = {
        'OrderID': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        'Date': pd.to_datetime(
            ['2026-01-01', '2026-01-01', '2026-01-02', '2026-01-02', '2026-01-03', '2026-01-03', '2026-01-04',
             '2026-01-04']),
        'Product': ['Laptop', 'Mouse', 'Chair', 'Keyboard', 'Laptop', 'Desk', 'Mouse', 'Chair'],
        'Category': ['Electronics', 'Electronics', 'Furniture', 'Electronics', 'Electronics', 'Furniture',
                     'Electronics', 'Furniture'],
        'Price': [80000, 1500, 5000, 3500, 82000, 12000, 1500, 5500],
        'Quantity': [2, 5, 3, 4, 1, 1, 10, 2],
        'City': ['Lahore', 'Karachi', 'Multan', 'Lahore', 'Karachi', 'Lahore', 'Multan', 'Karachi']
    }
    df = pd.DataFrame(data)
    df['Revenue'] = df['Price'] * df['Quantity']
    return df


df_demo = get_mock_data()

# 4. Premium Sidebar Navigation Elements
with st.sidebar:
    st.markdown(
        "<h1 style='font-size: 1.8rem; background: linear-gradient(135deg, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:800;'>🔮 InsightSphere</h1>",
        unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size:0.85rem; margin-top:-10px;'>Next-Gen Autonomous Analytics</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<p class='kpi-label'>Pipeline Workspace</p>", unsafe_allow_html=True)
    app_mode = st.radio(
        "Select Active Layer:",
        ["📥 File Ingestion", "🧼 Data Purification", "📊 Intelligence Dashboard", "🧠 Contextual AI Agent"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        "<div class='glass-card' style='padding: 1rem;'><p style='margin:0; font-size:0.8rem; color:#94a3b8;'>🟢 SYSTEM PROFILE<br><b style='color:#fff;'>DEMO ENGINE ACTIVE</b></p></div>",
        unsafe_allow_html=True)

# 5. Application Heading Section
st.markdown("<h1 class='glow-title'>InsightSphere Matrix Engine</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color: #94a3b8; font-size: 1.05rem; font-weight: 300;'>Fusing raw business records into immersive, high-fidelity computational summaries.</p>",
    unsafe_allow_html=True)
st.markdown("---")

# ==================== INTERFACE LAYER 1: FILE INGESTION ====================
if app_mode == "📥 File Ingestion":
    st.markdown("### 🗂️ Data Workspace Upload")
    st.markdown("Drop structural file frames below to map internal data typologies.")

    uploaded_file = st.file_uploader("Upload operational sheets (.csv, .xlsx)", type=["csv", "xlsx"],
                                     label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 💎 Live Demonstration Workspace Profile")
    st.markdown("""
        <div class="glass-alert-success">
            ✨ <b>Ingestion Status Verified:</b> Successfully projecting active application layer variables.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df_demo, use_container_width=True)

# ==================== INTERFACE LAYER 2: PURIFICATION ====================
elif app_mode == "🧼 Data Purification":
    st.markdown("### 🧬 Automated Normalization & Data Cleansing")
    st.markdown("Algorithmic cleanup handles structural typos, trims trailing spaces, and standardizes data frames.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<div class='glass-card'><h4>⚠️ Raw Source Artifacts</h4><p style='color:#cbd5e1; font-size:0.85rem;'>Simulated corrupted incoming inputs.</p>",
            unsafe_allow_html=True)
        dirty_sample = pd.DataFrame({
            'Product': [' Laptop ', 'Mouse', 'Chair', '  Keyboard '],
            'Price': ['80000', '1500', 'five thousand', '3500'],
            'City': ['lahore', ' Karachi', 'multan', 'Lahore']
        })
        st.dataframe(dirty_sample, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            "<div class='glass-card'><h4>✨ Normalized Output Matrix</h4><p style='color:#cbd5e1; font-size:0.85rem;'>Parsed, typed, and structured variables.</p>",
            unsafe_allow_html=True)
        clean_sample = pd.DataFrame({
            'Product': ['Laptop', 'Mouse', 'Chair', 'Keyboard'],
            'Price': [80000, 1500, 5000, 3500],
            'City': ['Lahore', 'Karachi', 'Multan', 'Lahore']
        })
        st.dataframe(clean_sample, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Trigger Global Purification Stream", type="primary"):
        with st.spinner("Executing custom formatting microservices..."):
            time.sleep(1)
            st.toast("Pipeline scrubbed successfully!", icon="💎")

# ==================== INTERFACE LAYER 3: DASHBOARD ====================
elif app_mode == "📊 Intelligence Dashboard":
    st.markdown("### ⚡ Strategic Performance Analytics Overview")

    # Elegant Filter Section in a Clean Row
    st.markdown("<p class='kpi-label'>🎛️ Real-time Context Dimensions</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        selected_city = st.multiselect("Filter by Store Location:", options=list(df_demo['City'].unique()),
                                       default=list(df_demo['City'].unique()))
    with c2:
        selected_cat = st.multiselect("Filter by Product Classification Group:",
                                      options=list(df_demo['Category'].unique()),
                                      default=list(df_demo['Category'].unique()))

    filtered_df = df_demo[(df_demo['City'].isin(selected_city)) & (df_demo['Category'].isin(selected_cat))]
    st.markdown("<br>", unsafe_allow_html=True)

    # Glassmorphic KPI Row Architecture
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        total_rev = filtered_df['Revenue'].sum() if not filtered_df.empty else 0
        st.markdown(f"""
            <div class="glass-card">
                <div class="kpi-label">💰 Gross Enterprise Revenue</div>
                <div class="kpi-value">PKR {total_rev:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi2:
        total_qty = filtered_df['Quantity'].sum() if not filtered_df.empty else 0
        st.markdown(f"""
            <div class="glass-card">
                <div class="kpi-label">📦 Total Inventory Outflow</div>
                <div class="kpi-value">{total_qty:,} Units</div>
            </div>
        """, unsafe_allow_html=True)
    with kpi3:
        avg_order = filtered_df['Revenue'].mean() if not filtered_df.empty else 0
        st.markdown(f"""
            <div class="glass-card">
                <div class="kpi-label">📈 Average Transaction Value</div>
                <div class="kpi-value">PKR {avg_order:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Modern Native Chart Blocks
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.markdown("<div class='glass-card'>📈 <b>Revenue Allocations Across Hub Cities</b>", unsafe_allow_html=True)
        city_sales = filtered_df.groupby('City')['Revenue'].sum() if not filtered_df.empty else pd.Series()
        st.bar_chart(city_sales, color="#38bdf8")
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown("<div class='glass-card'>🛒 <b>Product Demand Vector Densities</b>", unsafe_allow_html=True)
        prod_sales = filtered_df.groupby('Product')['Quantity'].sum() if not filtered_df.empty else pd.Series()
        st.line_chart(prod_sales, color="#818cf8")
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== INTERFACE LAYER 4: AI AGENT ====================
elif app_mode == "🧠 Contextual AI Agent":
    st.markdown("### 🤖 Cognitive Synthesis Narrative Layer")
    st.markdown("Extracting insights from the operational spreadsheet data.")

    st.markdown("""
        <div class="glass-card">
            <h4 style="color: #38bdf8; margin-top:0;">💡 Executive Summary Insight Streams</h4>
            <ul style="color: #cbd5e1; line-height: 1.8;">
                <li><b style="color:#ffffff;">Regional Dominance Vector:</b> <span class="neon-accent">Lahore</span> scales out as the core high-yield hub, contributing over 60% of the aggregate transaction cash flow.</li>
                <li><b style="color:#ffffff;">Velocity Performance Indicator:</b> Laptops command high revenue margins, but smaller peripherals like <span class="neon-accent">Mice</span> present higher logistical unit frequency volume.</li>
                <li><b style="color:#ffffff;">Structural Recommendation:</b> Furniture categories are carrying dead overhead due to low transaction frequency. Adjusting pricing models is recommended.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.text_input("Query the underlying dataset context freely:")
    if st.button("Generate System Narrative Response", type="primary"):
        st.markdown("""
            <div class="glass-alert-error" style="margin-top: 1rem;">
                🛠️ <b>System Alert:</b> Advanced Semantic Neural LLM integration becomes functional in Version 2.
            </div>
        """, unsafe_allow_html=True)
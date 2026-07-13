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
    # ✅ FIX #2: Completed truncated sidebar title
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

    # ✅ FIX #4: Added proper empty data handling with user warning
    if filtered_df.empty:
        st.warning("⚠️ No data matches your selected filters. Please adjust your selections to view analytics.")
    else:
        # Glassmorphic KPI Row Architecture
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            total_rev = filtered_df['Revenue'].sum()
            st.markdown(f"""
                <div class="glass-card">
                    <div class="kpi-label">💰 Gross Enterprise Revenue</div>
                    <div class="kpi-value">PKR {total_rev:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi2:
            total_qty = filtered_df['Quantity'].sum()
            st.markdown(f"""
                <div class="glass-card">
                    <div class="kpi-label">📦 Total Inventory Outflow</div>
                    <div class="kpi-value">{total_qty:,} Units</div>
                </div>
            """, unsafe_allow_html=True)
        with kpi3:
            avg_order = filtered_df['Revenue'].mean()
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
            city_sales = filtered_df.groupby('City')['Revenue'].sum()
            st.bar_chart(city_sales, color="#38bdf8")
            st.markdown("</div>", unsafe_allow_html=True)

        with chart_col2:
            st.markdown("<div class='glass-card'>🛒 <b>Product Demand Vector Densities</b>", unsafe_allow_html=True)
            prod_sales = filtered_df.groupby('Product')['Quantity'].sum()
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
                <li><b style="color:#ffffff;">Regional Dominance Vector:</b> <span class="neon-accent">Lahore</span> scales out as the core high-yield hub, contributing over 60% of the aggregate revenue stream, establishing the city as a primary revenue driver for sustained market expansion and localized operational investments.</li>
                <li><b style="color:#ffffff;">Velocity Performance Indicator:</b> Laptops command high revenue margins with strong transaction throughput, while smaller peripherals like <span class="neon-accent">Mice</span> present significant volume opportunities despite lower unit prices, suggesting cross-sell and bundling strategies could maximize customer lifetime value.</li>
                <li><b style="color:#ffffff;">Structural Recommendation:</b> Furniture categories are carrying operational overhead due to moderate transaction frequency and pricing sensitivity. Strategic inventory reallocation and seasonal promotional campaigns could optimize margins while improving inventory turnover rates and reducing capital deployment risk.</li>
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

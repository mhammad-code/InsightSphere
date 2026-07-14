import streamlit as st
import pandas as pd
import datetime
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
from modules.theme import apply_theme, custom_metric, render_metric_grid, render_central_brand, sidebar_nav, fix_sidebar_icon

st.set_page_config(page_title="InsightSphere", layout="wide", initial_sidebar_state="expanded")


@st.cache_data(show_spinner="Reading your file...")
def cached_load_and_clean(file_bytes, file_name):
    """
    Cached so re-clicking nav tabs or changing filters doesn't re-read and
    re-clean the file from scratch every time -- only reruns when the
    actual uploaded file changes. This is the main performance fix, since
    Streamlit reruns the whole script on every button/filter click.
    """
    import io
    file_like = io.BytesIO(file_bytes)
    file_like.name = file_name
    raw_df = load_file(file_like)
    errors = validate_dataset(raw_df)
    if errors:
        return None, errors
    cleaned = clean_dataset(raw_df.copy())
    return cleaned, None



apply_theme()
fix_sidebar_icon()
render_central_brand()

st.markdown(
    "<p style='text-align: center; color: #94A3B8; margin-top: -15px; margin-bottom: 35px; font-weight: 500;'>"
    "Upload your sales file below and see what it tells you.</p>",
    unsafe_allow_html=True
)

# ---------------- Sidebar Navigation (stable button-based) ----------------
nav_options = ["Dashboard", "Ask Questions", "Download", "AI Chat"]
nav_icons = ["📊", "🔍", "💾", "💬"]
clean_route = sidebar_nav(nav_options, nav_icons)

uploaded_file = st.file_uploader("Upload CSV or Excel sheet", type=["csv", "xlsx"], label_visibility="collapsed")

final_df = None
kpis = {}
city_col, category_col, date_col = None, None, None

if uploaded_file is not None:
    try:
        cleaned_df, errors = cached_load_and_clean(uploaded_file.getvalue(), uploaded_file.name)

        if errors:
            st.error("This file has a problem. Please check it and upload again.")
            st.stop()

        st.sidebar.markdown("<hr style='margin:15px 0; border-color:rgba(255,255,255,0.05);'/>", unsafe_allow_html=True)
        st.sidebar.markdown(
            "<p style='font-size:0.7rem; letter-spacing:1.5px; text-transform:uppercase; "
            "color:#64748B; font-weight:800; margin-bottom:12px;'>Filters</p>",
            unsafe_allow_html=True
        )

        city_col = find_column(cleaned_df, ["city", "location", "region"])
        category_col = find_column(cleaned_df, ["category", "type"])
        date_col = find_column(cleaned_df, ["date"])

        filtered_df = cleaned_df.copy()

        if city_col:
            city_options = sorted(cleaned_df[city_col].dropna().unique().tolist())
            selected_cities = st.sidebar.multiselect("City", city_options, default=city_options)
            filtered_df = filtered_df[filtered_df[city_col].isin(selected_cities)]

        if category_col:
            category_options = sorted(cleaned_df[category_col].dropna().unique().tolist())
            selected_categories = st.sidebar.multiselect(
                "Category", category_options, default=category_options
            )
            filtered_df = filtered_df[filtered_df[category_col].isin(selected_categories)]

        if date_col:
            filtered_df[date_col] = pd.to_datetime(filtered_df[date_col], errors="coerce")
            valid_dates = filtered_df[date_col].dropna()
            if not valid_dates.empty:
                min_date: datetime.date = valid_dates.min().date()
                max_date: datetime.date = valid_dates.max().date()

                date_range = st.sidebar.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
                    start_date, end_date = date_range
                    filtered_df = filtered_df[
                        (filtered_df[date_col].dt.date >= start_date) &
                        (filtered_df[date_col].dt.date <= end_date)
                    ]

        if not filtered_df.empty:
            final_df = filtered_df
            _, kpis = analyze_dataset(final_df)
    except Exception as e:
        st.error("Something went wrong while reading this file. Please try again.")

# ---------------- PAGE: Executive Dashboard ----------------
if clean_route == "Dashboard":
    st.subheader("Your Key Numbers")
    if final_df is None:
        st.info("📊 Upload a file above to see your numbers here.")
    else:
        render_metric_grid(kpis)

        st.divider()
        st.subheader("Charts")
        charts = generate_all_charts(final_df)
        heatmap = charts.pop("Correlation Heatmap", None)

        if charts:
            chart_names = list(charts.keys())
            for i in range(0, len(chart_names), 2):
                row_items = chart_names[i:i + 2]
                cols = st.columns(len(row_items))
                for col, name in zip(cols, row_items):
                    with col:
                        # staticPlot disables zoom, click, dragging, and hover editing
                        st.plotly_chart(charts[name], use_container_width=True, config={"staticPlot": True})

        if heatmap:
            with st.expander("Advanced: Show number relationships (for data experts)"):
                st.caption("This chart shows how different numbers relate to each other. It's more technical and mainly useful for analysts.")
                st.plotly_chart(heatmap, use_container_width=True, config={"staticPlot": True})

        st.divider()
        st.subheader("What This Means")
        insights = generate_insights(final_df, kpis)
        if insights:
            for insight in insights:
                st.markdown(f"✨ {insight}")

# ---------------- PAGE: Interactive Studio ----------------
elif clean_route == "Ask Questions":
    st.subheader("Ask a Question")
    if final_df is None:
        st.info("💡 Upload a file first to ask questions about your data.")
    else:
        available_queries = get_available_queries(final_df)
        if available_queries:
            selected_query = st.selectbox("What would you like to know?", list(available_queries.keys()))
            query_key = available_queries[selected_query]

            if query_key == "top_products":
                st.dataframe(query_top_products(final_df), use_container_width=True)
            elif query_key == "lowest_products":
                st.dataframe(query_lowest_selling_products(final_df), use_container_width=True)
            elif query_key == "revenue_by_city" and city_col:
                city_choice = st.selectbox(
                    "Choose a city:", sorted(final_df[city_col].dropna().unique().tolist())
                )
                res = query_revenue_by_city(final_df, city_choice)
                if res is not None:
                    custom_metric(f"Total Revenue Generated — {city_choice}", f"{res:,.2f}", "PKR")
            elif query_key == "revenue_by_category" and category_col:
                cat_choice = st.selectbox(
                    "Choose a category:", sorted(final_df[category_col].dropna().unique().tolist())
                )
                res = query_revenue_by_category(final_df, cat_choice)
                if res is not None:
                    custom_metric(f"Total Revenue Generated — {cat_choice}", f"{res:,.2f}", "PKR")
            elif query_key == "orders_by_city":
                st.dataframe(query_orders_by_city(final_df), use_container_width=True)

# ---------------- PAGE: Data Exporter ----------------
elif clean_route == "Download":
    st.subheader("Download Your Reports")
    if final_df is None:
        st.info("💾 Upload a file first to download your reports.")
    else:
        insights = generate_insights(final_df, kpis)

        # Row 1: CSV Export
        d_col1, d_col2 = st.columns([5, 1])
        with d_col1:
            st.markdown("""
            <div class="premium-download-card">
                <div class="download-tile-left-content">
                    <div class="download-tile-icon-frame">📄</div>
                    <div class="download-tile-text-fields">
                        <div class="download-tile-title">CSV File</div>
                        <div class="download-tile-desc">A simple file you can open in Excel or Google Sheets.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with d_col2:
            st.markdown('<div class="export-col-wrapper" style="margin-top: 20px;">', unsafe_allow_html=True)
            st.download_button(
                "Export CSV", data=export_to_csv(final_df), file_name="raw_metrics.csv",
                mime="text/csv", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Row 2: Excel Export
        d_col1, d_col2 = st.columns([5, 1])
        with d_col1:
            st.markdown("""
            <div class="premium-download-card">
                <div class="download-tile-left-content">
                    <div class="download-tile-icon-frame">📊</div>
                    <div class="download-tile-text-fields">
                        <div class="download-tile-title">Excel Report</div>
                        <div class="download-tile-desc">A ready-to-use Excel file with your data and key numbers.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with d_col2:
            st.markdown('<div class="export-col-wrapper" style="margin-top: 20px;">', unsafe_allow_html=True)
            st.download_button(
                "Export Excel", data=export_to_excel(final_df, kpis),
                file_name="performance_summary.xlsx", mime="application/vnd.ms-excel",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Row 3: PDF Export
        d_col1, d_col2 = st.columns([5, 1])
        with d_col1:
            st.markdown("""
            <div class="premium-download-card">
                <div class="download-tile-left-content">
                    <div class="download-tile-icon-frame">💼</div>
                    <div class="download-tile-text-fields">
                        <div class="download-tile-title">PDF Report</div>
                        <div class="download-tile-desc">A clean summary you can print or share with your team.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with d_col2:
            st.markdown('<div class="export-col-wrapper" style="margin-top: 20px;">', unsafe_allow_html=True)
            st.download_button(
                "Generate PDF", data=export_to_pdf(kpis, insights, final_df),
                file_name="executive_briefing.pdf", mime="application/pdf", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PAGE: AI Intelligent Agent ----------------
elif clean_route == "AI Chat":
    st.subheader("Chat with AI")
    if final_df is None:
        st.info("💡 Upload a file first to chat with the AI about your data.")
    else:
        if "chat_messages" not in st.session_state:
            st.session_state["chat_messages"] = []

        for msg in st.session_state["chat_messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_question = st.chat_input("Ask me anything about your data...")
        if user_question:
            st.session_state["chat_messages"].append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_ai(
                        question=user_question, df=final_df, kpis=kpis,
                        chat_history=st.session_state["chat_messages"][:-1]
                    )
                    st.markdown(answer)
            st.session_state["chat_messages"].append({"role": "assistant", "content": answer})
import streamlit as st
from modules.loader import load_file
from modules.validator import validate_dataset
from modules.cleaner import clean_dataset
from modules.analyzer import analyze_dataset
from modules.visualizer import generate_all_charts
from modules.insights import generate_insights

st.set_page_config(page_title="InsightSphere", layout="wide")

st.title("InsightSphere")
st.caption("Upload your business data to get started")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
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

    with st.expander("Preview: Raw data (before cleaning)"):
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        st.dataframe(df.head())

    cleaned_df = clean_dataset(df.copy())
    st.session_state["clean_df"] = cleaned_df

    st.success("Data cleaned successfully")

    with st.expander("Preview: Cleaned data (after cleaning)"):
        st.write(f"Rows: {cleaned_df.shape[0]}, Columns: {cleaned_df.shape[1]}")
        st.dataframe(cleaned_df.head())

    final_df, kpis = analyze_dataset(cleaned_df)
    st.session_state["final_df"] = final_df

    st.divider()
    st.subheader("Key Metrics")

    if not kpis:
        st.info("No KPIs could be calculated from this dataset.")
    else:
        kpi_items = list(kpis.items())
        cols = st.columns(len(kpi_items))

        for col, (name, value) in zip(cols, kpi_items):
            if isinstance(value, (int, float)):
                display_value = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
            else:
                display_value = str(value)
            col.metric(label=name, value=display_value)

    with st.expander("Preview: Data with calculated features (e.g. Revenue)"):
        st.dataframe(final_df.head())

    # Visualization
    st.divider()
    st.subheader("Visual Insights")

    charts = generate_all_charts(final_df)

    if not charts:
        st.info("No charts could be generated from this dataset.")
    else:
        chart_names = list(charts.keys())
        for i in range(0, len(chart_names), 2):
            row_charts = chart_names[i:i + 2]
            cols = st.columns(len(row_charts))
            for col, name in zip(cols, row_charts):
                col.plotly_chart(charts[name], use_container_width=True)

    # Business Insights
    st.divider()
    st.subheader("Business Insights")

    insights = generate_insights(final_df, kpis)

    if not insights:
        st.info("No insights could be generated from this dataset.")
    else:
        for insight in insights:
            st.markdown(f"- {insight}")
import plotly.express as px
from modules.analyzer import find_column


def chart_sales_trend(df):
    """
    Line chart showing revenue over time.
    Returns None if no date or revenue column is found.
    """
    date_col = find_column(df, ["date"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not date_col or not revenue_col:
        return None

    trend_df = df.groupby(date_col)[revenue_col].sum().reset_index()

    fig = px.line(
        trend_df,
        x=date_col,
        y=revenue_col,
        title="Sales Trend Over Time",
        markers=True,
    )
    fig.update_layout(template="plotly_dark")
    return fig


def chart_revenue_by_city(df):
    """
    Bar chart showing total revenue per city.
    """
    city_col = find_column(df, ["city", "location", "region"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not city_col or not revenue_col:
        return None

    city_df = df.groupby(city_col)[revenue_col].sum().reset_index()
    city_df = city_df.sort_values(by=revenue_col, ascending=False)

    fig = px.bar(
        city_df,
        x=city_col,
        y=revenue_col,
        title="Revenue by City",
        color=revenue_col,
        color_continuous_scale="Blues",
    )
    fig.update_layout(template="plotly_dark")
    return fig


def chart_category_distribution(df):
    """
    Pie chart showing revenue share by category.
    """
    category_col = find_column(df, ["category", "type"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not category_col or not revenue_col:
        return None

    cat_df = df.groupby(category_col)[revenue_col].sum().reset_index()

    fig = px.pie(
        cat_df,
        names=category_col,
        values=revenue_col,
        title="Revenue by Category",
        hole=0.4,
    )
    fig.update_layout(template="plotly_dark")
    return fig


def chart_top_products(df, top_n=10):
    """
    Horizontal bar chart showing the top N products by revenue.
    """
    product_col = find_column(df, ["product", "item"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not product_col or not revenue_col:
        return None

    top_df = (
        df.groupby(product_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(by=revenue_col, ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        top_df,
        x=revenue_col,
        y=product_col,
        title=f"Top {top_n} Products by Revenue",
        orientation="h",
        color=revenue_col,
        color_continuous_scale="Tealgrn",
    )
    fig.update_layout(template="plotly_dark", yaxis={"categoryorder": "total ascending"})
    return fig


def chart_correlation_heatmap(df):
    """
    Heatmap showing correlation between numeric columns.
    """
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r",
        aspect="auto",
    )
    fig.update_layout(template="plotly_dark")
    return fig


def generate_all_charts(df):
    """
    Runs all chart functions and returns a dict of chart name -> figure.
    Charts that couldn't be generated (missing columns) are excluded.
    """
    charts = {
        "Sales Trend": chart_sales_trend(df),
        "Revenue by City": chart_revenue_by_city(df),
        "Category Distribution": chart_category_distribution(df),
        "Top Products": chart_top_products(df),
        "Correlation Heatmap": chart_correlation_heatmap(df),
    }
    return {name: fig for name, fig in charts.items() if fig is not None}
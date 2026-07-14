import plotly.express as px
import plotly.graph_objects as go
from modules.analyzer import find_column

# Distinct neon palette -- each chart gets its own identity instead of one repeated color
NEON_CYAN = "#00F5D4"
NEON_VIOLET = "#8B5CF6"
NEON_PINK = "#EC4899"
NEON_ORANGE = "#F97316"
NEON_BLUE = "#3B82F6"

DARK_TEMPLATE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#C7CEDB", family="Plus Jakarta Sans, sans-serif"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
    margin=dict(l=10, r=10, t=40, b=10),
)


def chart_sales_trend(df):
    """Neon cyan area/line chart showing revenue over time."""
    date_col = find_column(df, ["date"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])
    if not date_col or not revenue_col:
        return None

    trend_df = df.groupby(date_col)[revenue_col].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend_df[date_col], y=trend_df[revenue_col],
        mode="lines", line=dict(color=NEON_CYAN, width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(0, 245, 212, 0.12)",
    ))
    fig.update_layout(**DARK_TEMPLATE_LAYOUT, title="Sales Over Time")
    return fig


def chart_revenue_by_city(df):
    """Violet-to-pink gradient bar chart showing total revenue per city."""
    city_col = find_column(df, ["city", "location", "region"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])
    if not city_col or not revenue_col:
        return None

    city_df = df.groupby(city_col)[revenue_col].sum().reset_index()
    city_df = city_df.sort_values(by=revenue_col, ascending=False)

    fig = px.bar(
        city_df, x=city_col, y=revenue_col,
        color=revenue_col, color_continuous_scale=[NEON_VIOLET, NEON_PINK],
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**DARK_TEMPLATE_LAYOUT, title="Revenue by City", coloraxis_showscale=False)
    return fig


def chart_category_distribution(df):
    """Multi-color donut chart showing revenue share by category."""
    category_col = find_column(df, ["category", "type"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])
    if not category_col or not revenue_col:
        return None

    cat_df = df.groupby(category_col)[revenue_col].sum().reset_index()

    fig = px.pie(
        cat_df, names=category_col, values=revenue_col, hole=0.55,
        color_discrete_sequence=[NEON_CYAN, NEON_VIOLET, NEON_PINK, NEON_ORANGE, NEON_BLUE],
    )
    fig.update_traces(marker=dict(line=dict(color="#070A12", width=2)))
    fig.update_layout(**DARK_TEMPLATE_LAYOUT, title="Revenue by Category")
    return fig


def chart_top_products(df, top_n=10):
    """Orange-to-pink gradient horizontal bar chart of top products."""
    product_col = find_column(df, ["product", "item"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])
    if not product_col or not revenue_col:
        return None

    top_df = (
        df.groupby(product_col)[revenue_col].sum().reset_index()
        .sort_values(by=revenue_col, ascending=False).head(top_n)
    )

    fig = px.bar(
        top_df, x=revenue_col, y=product_col, orientation="h",
        color=revenue_col, color_continuous_scale=[NEON_ORANGE, NEON_PINK],
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**DARK_TEMPLATE_LAYOUT, title=f"Top {top_n} Products", coloraxis_showscale=False)
    fig.update_yaxes(categoryorder="total ascending")
    return fig


def chart_correlation_heatmap(df):
    """Blue-violet heatmap showing correlation between numeric columns."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    fig = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale=[[0, "#3B82F6"], [0.5, "#0D1527"], [1, "#EC4899"]],
    )
    fig.update_layout(**DARK_TEMPLATE_LAYOUT, title="Correlation Heatmap")
    return fig


def generate_all_charts(df):
    """Runs all chart functions and returns a dict of chart name -> figure,
    excluding any that couldn't be generated due to missing columns."""
    charts = {
        "Sales Trend": chart_sales_trend(df),
        "Revenue by City": chart_revenue_by_city(df),
        "Category Distribution": chart_category_distribution(df),
        "Top Products": chart_top_products(df),
        "Correlation Heatmap": chart_correlation_heatmap(df),
    }
    return {name: fig for name, fig in charts.items() if fig is not None}
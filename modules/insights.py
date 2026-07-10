from modules.analyzer import find_column


def insight_overview(df, kpis):
    """
    Basic summary insight using Total Revenue and Total Orders.
    """
    if "Total Revenue" in kpis and "Total Orders" in kpis:
        return (
            f"The business generated a total revenue of PKR {kpis['Total Revenue']:,.0f} "
            f"across {kpis['Total Orders']:,} orders."
        )
    return None


def insight_top_city(df, kpis):
    """
    Highlights the best performing city and its revenue share.
    """
    city_col = find_column(df, ["city", "location", "region"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not city_col or not revenue_col or "Total Revenue" not in kpis:
        return None

    city_revenue = df.groupby(city_col)[revenue_col].sum()
    top_city = city_revenue.idxmax()
    share = (city_revenue.max() / kpis["Total Revenue"]) * 100

    return f"{top_city} is the highest-performing city, contributing {share:.1f}% of total revenue."


def insight_top_category(df, kpis):
    """
    Highlights the best performing category and its revenue share.
    """
    category_col = find_column(df, ["category", "type"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not category_col or not revenue_col or "Total Revenue" not in kpis:
        return None

    cat_revenue = df.groupby(category_col)[revenue_col].sum()
    top_category = cat_revenue.idxmax()
    share = (cat_revenue.max() / kpis["Total Revenue"]) * 100

    return f"{top_category} generated {share:.1f}% of total revenue, making it the top-performing category."


def insight_best_product(df, kpis):
    """
    Highlights the best selling product by revenue.
    """
    if "Best Selling Product" in kpis:
        return f"{kpis['Best Selling Product']} is the best-selling product by total revenue."
    return None


def insight_trend(df):
    """
    Compares revenue in the first half vs second half of the date range
    to give a simple directional trend insight.
    """
    date_col = find_column(df, ["date"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not date_col or not revenue_col:
        return None

    trend_df = df.dropna(subset=[date_col]).sort_values(by=date_col)

    if trend_df.empty or trend_df[date_col].nunique() < 2:
        return None

    midpoint = len(trend_df) // 2
    first_half_revenue = trend_df.iloc[:midpoint][revenue_col].sum()
    second_half_revenue = trend_df.iloc[midpoint:][revenue_col].sum()

    if first_half_revenue == 0:
        return None

    change_pct = ((second_half_revenue - first_half_revenue) / first_half_revenue) * 100

    if change_pct > 0:
        return f"Revenue increased by {change_pct:.1f}% in the later part of the period compared to the earlier part."
    elif change_pct < 0:
        return f"Revenue decreased by {abs(change_pct):.1f}% in the later part of the period compared to the earlier part."
    else:
        return "Revenue remained stable across the period."


def generate_insights(df, kpis):
    """
    Runs all insight functions and returns a list of insight sentences.
    Insights that couldn't be generated (missing columns) are excluded.
    """
    insight_functions = [
        lambda: insight_overview(df, kpis),
        lambda: insight_top_city(df, kpis),
        lambda: insight_top_category(df, kpis),
        lambda: insight_best_product(df, kpis),
        lambda: insight_trend(df),
    ]

    insights = [fn() for fn in insight_functions]
    return [i for i in insights if i is not None]
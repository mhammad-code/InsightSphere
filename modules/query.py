import pandas as pd
from modules.analyzer import find_column


def query_top_products(df, n=10):
    """
    Returns top N products by revenue as a DataFrame.
    """
    product_col = find_column(df, ["product", "item"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not product_col or not revenue_col:
        return None

    result = (
        df.groupby(product_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(by=revenue_col, ascending=False)
        .head(n)
    )
    result.columns = ["Product", "Revenue"]
    return result


def query_revenue_by_city(df, city_name):
    """
    Returns total revenue for a specific city.
    """
    city_col = find_column(df, ["city", "location", "region"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not city_col or not revenue_col:
        return None

    city_data = df[df[city_col].str.lower() == city_name.lower()]

    if city_data.empty:
        return None

    return city_data[revenue_col].sum()


def query_revenue_by_category(df, category_name):
    """
    Returns total revenue for a specific category.
    """
    category_col = find_column(df, ["category", "type"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not category_col or not revenue_col:
        return None

    cat_data = df[df[category_col].str.lower() == category_name.lower()]

    if cat_data.empty:
        return None

    return cat_data[revenue_col].sum()


def query_lowest_selling_products(df, n=5):
    """
    Returns the bottom N products by revenue.
    """
    product_col = find_column(df, ["product", "item"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if not product_col or not revenue_col:
        return None

    result = (
        df.groupby(product_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(by=revenue_col, ascending=True)
        .head(n)
    )
    result.columns = ["Product", "Revenue"]
    return result


def query_orders_by_city(df):
    """
    Returns order count per city as a DataFrame.
    """
    city_col = find_column(df, ["city", "location", "region"])

    if not city_col:
        return None

    result = df[city_col].value_counts().reset_index()
    result.columns = ["City", "Order Count"]
    return result


def get_available_queries(df):
    """
    Returns a dict of query label -> whether it's available for this dataset,
    based on which columns exist.
    """
    city_col = find_column(df, ["city", "location", "region"])
    category_col = find_column(df, ["category", "type"])
    product_col = find_column(df, ["product", "item"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    queries = {}

    if product_col and revenue_col:
        queries["Top 10 products"] = "top_products"
        queries["Lowest selling products"] = "lowest_products"

    if city_col and revenue_col:
        queries["Revenue by city (select city)"] = "revenue_by_city"

    if category_col and revenue_col:
        queries["Revenue by category (select category)"] = "revenue_by_category"

    if city_col:
        queries["Order count by city"] = "orders_by_city"

    return queries
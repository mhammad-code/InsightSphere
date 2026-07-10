import pandas as pd


def find_column(df, keywords):
    """
    Finds the first column whose name contains any of the given keywords
    (case-insensitive). Returns None if no match is found.
    """
    for col in df.columns:
        for keyword in keywords:
            if keyword.lower() in col.lower():
                return col
    return None


def create_revenue_column(df):
    """
    Creates a Revenue column (Price * Quantity) if both a price-like
    and quantity-like column exist and Revenue doesn't already exist.
    """
    price_col = find_column(df, ["price", "amount", "cost"])
    qty_col = find_column(df, ["quantity", "qty", "units"])
    revenue_col = find_column(df, ["revenue", "sales", "total"])

    if revenue_col is None and price_col is not None and qty_col is not None:
        df["Revenue"] = df[price_col] * df[qty_col]

    return df


def calculate_kpis(df):
    """
    Calculates key business KPIs from the cleaned dataset.
    Returns a dictionary of KPI name -> value.
    Any KPI whose required column is missing is simply skipped.
    """
    kpis = {}

    revenue_col = find_column(df, ["revenue", "sales", "total"])
    qty_col = find_column(df, ["quantity", "qty", "units"])
    product_col = find_column(df, ["product", "item"])
    city_col = find_column(df, ["city", "location", "region"])
    category_col = find_column(df, ["category", "type"])

    kpis["Total Orders"] = len(df)

    if revenue_col:
        kpis["Total Revenue"] = df[revenue_col].sum()
        kpis["Average Order Value"] = df[revenue_col].mean()

    if qty_col:
        kpis["Total Units Sold"] = df[qty_col].sum()

    if product_col and revenue_col:
        kpis["Best Selling Product"] = (
            df.groupby(product_col)[revenue_col].sum().idxmax()
        )

    if city_col and revenue_col:
        kpis["Top Performing City"] = (
            df.groupby(city_col)[revenue_col].sum().idxmax()
        )

    if category_col and revenue_col:
        kpis["Top Category"] = (
            df.groupby(category_col)[revenue_col].sum().idxmax()
        )

    return kpis


def analyze_dataset(df):
    """
    Runs feature creation and KPI calculation together.
    Returns (updated_df, kpis_dict).
    """
    df = create_revenue_column(df)
    kpis = calculate_kpis(df)
    return df, kpis
import pandas as pd


def strip_whitespace(df):
    """
    Removes leading/trailing whitespace from all text (object) columns.
    """
    text_cols = df.select_dtypes(include="object").columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
    return df


def convert_numeric_columns(df):
    """
    Attempts to convert object columns that actually contain numbers
    (e.g. "80000" stored as text) into real numeric dtype.
    Columns that fail to convert (truly text) are left unchanged.
    """
    for col in df.select_dtypes(include="object").columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        # Only convert if most values successfully became numbers
        # (avoids wrecking genuine text columns like "Product")
        if converted.notna().sum() >= 0.8 * len(df[col].dropna()):
            df[col] = converted
    return df


def drop_duplicate_rows(df):
    """
    Removes exact duplicate rows from the dataset.
    """
    return df.drop_duplicates()


def handle_missing_values(df):
    """
    Fills missing values:
    - Numeric columns -> filled with column median
    - Text columns -> filled with "Unknown"
    """
    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    for col in numeric_cols:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)

    for col in text_cols:
        df[col] = df[col].fillna("Unknown")

    return df


def parse_dates(df):
    """
    Detects columns that look like dates (based on column name or content)
    and converts them to proper datetime dtype.
    Invalid/unparseable dates become NaT (kept, not dropped, since dropping
    silently loses rows -- can be handled explicitly later if needed).
    """
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def clean_dataset(df):
    """
    Runs the full cleaning pipeline on the DataFrame, in order:
    1. Strip whitespace
    2. Convert numeric-looking text columns to real numbers
    3. Remove duplicate rows
    4. Handle missing values
    5. Parse date columns
    """
    df = strip_whitespace(df)
    df = convert_numeric_columns(df)
    df = drop_duplicate_rows(df)
    df = handle_missing_values(df)
    df = parse_dates(df)
    return df
def validate_dataset(df):
    """
    Validates a DataFrame and returns a list of error messages.
    An empty list means the dataset passed all checks.
    """
    errors = []

    if df is None:
        errors.append("No data was loaded.")
        return errors

    if df.empty:
        errors.append("The uploaded file contains no data.")

    if len(df.columns) == 0:
        errors.append("The uploaded file has no columns.")

    duplicate_cols = df.columns[df.columns.duplicated()].tolist()
    if duplicate_cols:
        errors.append(f"Duplicate column names found: {', '.join(set(duplicate_cols))}")

    empty_cols = [col for col in df.columns if df[col].isna().all()]
    if empty_cols:
        errors.append(f"These columns are completely empty: {', '.join(empty_cols)}")

    return errors
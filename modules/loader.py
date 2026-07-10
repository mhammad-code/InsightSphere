import pandas as pd


def load_file(uploaded_file):
    """
    Takes a file uploaded through Streamlit's file_uploader
    and returns it as a Pandas DataFrame.
    Supports .csv and .xlsx files.
    """
    file_name = uploaded_file.name

    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")

    return df


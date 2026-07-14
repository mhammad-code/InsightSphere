import os
import json
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from modules.analyzer import find_column

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class SafeJSONEncoder(json.JSONEncoder):
    """
    A robust JSON encoder that handles NumPy types, pandas types,
    and NaN/Inf values that standard json.dumps crashes on.
    """
    def default(self, obj):
        # Handle NumPy integers (e.g., int64)
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        # Handle NumPy floats (e.g., float64)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            # Convert NaN or Inf to None (represented as null in JSON)
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        # Handle NumPy arrays or Pandas series
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # Handle float('nan') or float('inf') standard python types
        elif isinstance(obj, float):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return obj
        return super(SafeJSONEncoder, self).default(obj)


def build_data_summary(df, kpis):
    """
    Builds a compact, token-efficient summary of the dataset
    for the AI to reason over, instead of sending raw rows.
    """
    summary = {}

    summary["kpis"] = {
        k: (round(v, 2) if isinstance(v, float) else v)
        for k, v in kpis.items()
    }

    revenue_col = find_column(df, ["revenue", "sales", "total"])
    city_col = find_column(df, ["city", "location", "region"])
    category_col = find_column(df, ["category", "type"])
    product_col = find_column(df, ["product", "item"])

    if revenue_col and city_col:
        city_summary = df.groupby(city_col)[revenue_col].sum().round(2).to_dict()
        summary["revenue_by_city"] = city_summary

    if revenue_col and category_col:
        category_summary = df.groupby(category_col)[revenue_col].sum().round(2).to_dict()
        summary["revenue_by_category"] = category_summary

    if revenue_col and product_col:
        product_summary = (
            df.groupby(product_col)[revenue_col]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .round(2)
            .to_dict()
        )
        summary["top_10_products_by_revenue"] = product_summary

    summary["total_rows"] = len(df)

    return summary


def ask_ai(question, df, kpis, chat_history=None):
    """
    Sends the user's question, along with a data summary, to Groq's LLM.
    chat_history is a list of {"role": ..., "content": ...} dicts for context.
    Returns the AI's text response.
    """
    data_summary = build_data_summary(df, kpis)

    # Convert keys to strings to handle any non-string dictionary keys (like dates or numbers)
    # and use the SafeJSONEncoder to dump without crashes
    try:
        serialized_summary = json.dumps(data_summary, cls=SafeJSONEncoder)
    except Exception:
        # Fallback string representation just in case
        serialized_summary = str(data_summary)

    system_prompt = (
        "You are a business data analyst assistant inside a BI dashboard called InsightSphere. "
        "You are given a summary of the user's business dataset as JSON. "
        "Answer questions ONLY using this data. "
        "Do not invent numbers that are not present or derivable from the summary. "
        "If the data summary does not contain enough information to answer, say so clearly. "
        "CRITICAL: All monetary figures, prices, revenues, and costs MUST be presented and formatted as PKR "
        "(e.g., prefix with 'Rs.' or 'PKR' and format with commas like 'Rs. 1,500,000' or '1.5 Million PKR'). "
        "Keep answers concise and business-focused, written like a report insight, not raw code or JSON.\n\n"
        f"Data summary:\n{serialized_summary}"
    )

    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content
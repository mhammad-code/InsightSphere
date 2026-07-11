import io
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm


def export_to_csv(df):
    """
    Converts a DataFrame to CSV bytes, ready for download.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def export_to_excel(df, kpis):
    """
    Creates an Excel file with two sheets:
    - 'Data' containing the cleaned/filtered dataset
    - 'KPIs' containing the calculated key metrics
    Returns bytes ready for download.
    """
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Data", index=False)

        if kpis:
            kpi_df = pd.DataFrame(list(kpis.items()), columns=["Metric", "Value"])
            kpi_df.to_excel(writer, sheet_name="KPIs", index=False)

    buffer.seek(0)
    return buffer.getvalue()


def export_to_pdf(kpis, insights, df):
    """
    Generates a PDF business report containing:
    - Title and summary
    - KPI table
    - Business insights (bullet points)
    - A preview of the data (first 15 rows)
    Returns bytes ready for download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=22, spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8
    )
    body_style = styles["BodyText"]

    elements = []

    elements.append(Paragraph("InsightSphere Business Report", title_style))
    elements.append(Paragraph("Automated summary of business performance", body_style))
    elements.append(Spacer(1, 12))

    # KPI section
    if kpis:
        elements.append(Paragraph("Key Metrics", heading_style))

        table_data = [["Metric", "Value"]]
        for name, value in kpis.items():
            if isinstance(value, float):
                display_value = f"{value:,.2f}"
            elif isinstance(value, int):
                display_value = f"{value:,}"
            else:
                display_value = str(value)
            table_data.append([name, display_value])

        kpi_table = Table(table_data, colWidths=[8 * cm, 8 * cm])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 1), (1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(kpi_table)

    # Insights section
    if insights:
        elements.append(Paragraph("Business Insights", heading_style))
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", body_style))
            elements.append(Spacer(1, 4))

    # Data preview section
    elements.append(Paragraph("Data Preview (first 15 rows)", heading_style))

    preview_df = df.head(15)
    preview_data = [list(preview_df.columns)] + preview_df.astype(str).values.tolist()

    preview_table = Table(preview_data, repeatRows=1)
    preview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))
    elements.append(preview_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
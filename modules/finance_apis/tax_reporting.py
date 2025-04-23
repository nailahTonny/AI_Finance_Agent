import sqlite3, os
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import re

def sanitize_column_name(name):
    """Convert to SQLite-compatible snake_case column name."""
    return re.sub(r'\W+', '_', str(name).strip().lower())

def parse_excel_to_db(file_path, db_path="data/financial_data.db"):
    df = pd.read_excel(file_path)
    original_columns = df.columns
    sanitized_columns = [sanitize_column_name(col) for col in original_columns]
    df.columns = sanitized_columns

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_name = f"financial_data_{timestamp}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create dynamic SQL table
    columns_sql = ", ".join([f"`{col}` TEXT" for col in sanitized_columns])
    create_sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_sql})"
    cursor.execute(create_sql)

    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    return table_name

def find_latest_excel(folder="data/uploaded_files"):
    files = [f for f in os.listdir(folder) if f.endswith(".xlsx")]
    if not files:
        return None
    files.sort(reverse=True)
    return os.path.join(folder, files[0])

def generate_report():
    db_path = "data/financial_data.db"
    uploads_folder = "data/uploaded_files"  # Changed to the correct folder
    pdf_folder = "pdf_reports"

    # Step 1: Get the latest Excel file
    latest_excel = find_latest_excel(uploads_folder)
    if not latest_excel:
        return {"error": "No Excel files found in uploads folder."}

    # Step 2: Parse and save to DB
    table_name = parse_excel_to_db(latest_excel, db_path)

    # Step 3: Fetch data
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 5")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    # Step 4: Generate PDF
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    filename = f"{pdf_folder}/tax_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tax Report", ln=True, align="C")

    # Header
    for col in columns:
        pdf.cell(40, 10, txt=str(col), border=1)
    pdf.ln()

    # Rows
    for row in rows:
        for val in row:
            pdf.cell(40, 10, txt=str(val), border=1)
        pdf.ln()

    pdf.output(filename)

    return {"status": "Report generated", "link": f"/{filename}", "table_name": table_name}

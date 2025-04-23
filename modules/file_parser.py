import pandas as pd
import sqlite3
import os
from datetime import datetime
import re

def sanitize_column_name(name):
    """Remove special characters and convert to snake_case."""
    return re.sub(r'\W+', '_', str(name).strip().lower())

def parse_and_store(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read Excel file and get first row as header
    df = pd.read_excel(file_path)

    # Sanitize column names to be SQLite-compatible
    original_columns = df.columns
    sanitized_columns = [sanitize_column_name(col) for col in original_columns]
    df.columns = sanitized_columns

    # Create dynamic table name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_name = f"financial_data_{timestamp}"

    # Create SQLite connection
    conn = sqlite3.connect("data/financial_data.db")
    cursor = conn.cursor()

    # Generate CREATE TABLE statement dynamically
    create_table_sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n  id INTEGER PRIMARY KEY AUTOINCREMENT,"
    for col in sanitized_columns:
        create_table_sql += f"\n  `{col}` TEXT,"
    create_table_sql = create_table_sql.rstrip(',') + "\n);"

    cursor.execute(create_table_sql)

    # Insert all rows into the table
    df.to_sql(table_name, conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

    return table_name, sanitized_columns

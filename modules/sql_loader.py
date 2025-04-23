from langchain.schema import Document
import sqlite3

def load_table_data(table_name: str):
    conn = sqlite3.connect("data/financial_data.db")
    cursor = conn.cursor()

    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info if col[1] != "id"]

    # Fetch all rows
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    documents = []
    for row in rows:
        row_dict = dict(zip(column_names, row[1:]))  # Skip the ID column
        page_content = "\n".join([f"{k}: {v}" for k, v in row_dict.items()])
        documents.append(Document(page_content=page_content, metadata={"source_table": table_name}))

    conn.close()
    return documents

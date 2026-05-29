import sqlite3
import json
import os


# -----------------------------------------------------
# Create database folder automatically
# -----------------------------------------------------
os.makedirs(
    "database",
    exist_ok=True
)


# -----------------------------------------------------
# Database path
# -----------------------------------------------------
DB_PATH = os.path.join(
    "database",
    "documents.db"
)


# -----------------------------------------------------
# Connect to SQLite database
# -----------------------------------------------------
conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()


# -----------------------------------------------------
# Create table if not exists
# -----------------------------------------------------
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        extracted_data TEXT
    )
    """
)

conn.commit()


# -----------------------------------------------------
# Save extracted document
# -----------------------------------------------------
def save_document(filename, extracted_data):

    cursor.execute(
        """
        INSERT INTO documents
        (filename, extracted_data)

        VALUES (?, ?)
        """,
        (
            filename,
            json.dumps(extracted_data)
        )
    )

    conn.commit()


# -----------------------------------------------------
# Retrieve all documents
# -----------------------------------------------------
def get_all_documents():

    cursor.execute(
        """
        SELECT filename, extracted_data
        FROM documents
        """
    )

    rows = cursor.fetchall()

    documents = []

    for row in rows:

        documents.append({

            "filename": row[0],

            "data": json.loads(row[1])
        })

    return documents

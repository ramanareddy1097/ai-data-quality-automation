import sqlite3
from pathlib import Path


DATABASE_FILE = Path("data/quality.db")


def initialize_database():

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            total_records INTEGER NOT NULL,
            quality_score REAL NOT NULL,
            issue_count INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_quality_run(
    file_name,
    total_records,
    quality_score,
    issue_count,
    created_at
):

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO quality_runs (
            file_name,
            total_records,
            quality_score,
            issue_count,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        file_name,
        total_records,
        quality_score,
        issue_count,
        created_at
    ))

    connection.commit()
    connection.close()


if __name__ == "__main__":

    initialize_database()

    print(
        f"Database initialized: {DATABASE_FILE}"
    )
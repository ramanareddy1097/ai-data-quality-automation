import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="AI Data Quality Automation API",
    description="API for monitoring data quality, AI analysis, and quality history.",
    version="1.0.0"
)


DATABASE_FILE = Path("data/quality.db")


@app.get("/")
def root():

    return {
        "application": "AI Data Quality Automation Platform",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/quality-runs")
def get_quality_runs():

    if not DATABASE_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="Database not found."
        )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            file_name,
            total_records,
            quality_score,
            issue_count,
            created_at
        FROM quality_runs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return {
        "count": len(rows),
        "quality_runs": [
            dict(row)
            for row in rows
        ]
    }


@app.get("/quality-runs/{run_id}")
def get_quality_run(run_id: int):

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            file_name,
            total_records,
            quality_score,
            issue_count,
            created_at
        FROM quality_runs
        WHERE id = ?
    """, (run_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:

        raise HTTPException(
            status_code=404,
            detail="Quality run not found."
        )

    return dict(row)
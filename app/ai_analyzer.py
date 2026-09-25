import json
from datetime import datetime
from pathlib import Path

import requests

from quality_checker import check_data_quality
from database import initialize_database, save_quality_run


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

REPORT_DIR = Path("reports")


def analyze_quality_report(quality_report):

    prompt = f"""
You are an AI Data Quality Analyst.

Analyze the following data quality report.

DATA QUALITY REPORT:
{json.dumps(quality_report, indent=2)}

Provide:

1. Summary of the data quality problems
2. Possible root cause for each problem
3. Business impact
4. Recommended remediation actions
5. Overall assessment

Important:
- Do not change or recalculate the numbers in the report.
- Use the exact issue counts provided.
- Keep the response clear, concise, and professional.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


def create_incident_report(quality_report, ai_analysis):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_file = REPORT_DIR / f"incident_{timestamp}.json"

    incident = {
        "generated_at": datetime.now().isoformat(),
        "file": quality_report["file"],
        "total_records": quality_report["total_records"],
        "quality_score": quality_report["quality_score"],
        "issues": quality_report["issues"],
        "ai_analysis": ai_analysis
    }

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            incident,
            file,
            indent=4
        )

    return report_file


if __name__ == "__main__":

    file = "data/incoming/transactions_bad.csv"

    print("\nRunning data quality checks...")

    quality_report = check_data_quality(file)

    # Initialize SQLite database
    initialize_database()

    # Save this quality run to SQLite
    save_quality_run(
        file_name=quality_report["file"],
        total_records=quality_report["total_records"],
        quality_score=quality_report["quality_score"],
        issue_count=len(quality_report["issues"]),
        created_at=datetime.now().isoformat()
    )

    print("\nDATA QUALITY REPORT")
    print("=" * 60)

    print(f"File: {quality_report['file']}")
    print(f"Records: {quality_report['total_records']}")
    print(f"Quality Score: {quality_report['quality_score']}%")

    print("\nIssues:")

    for issue in quality_report["issues"]:
        print(
            f"- {issue['issue']} | "
            f"Records: {issue['records_affected']} | "
            f"Severity: {issue['severity']}"
        )

    print("\nSending report to local AI...")

    ai_analysis = analyze_quality_report(
        quality_report
    )

    print("\nAI DATA QUALITY ANALYSIS")
    print("=" * 60)

    print(ai_analysis)

    report_file = create_incident_report(
        quality_report,
        ai_analysis
    )

    print("\nINCIDENT REPORT CREATED")
    print("=" * 60)
    print(f"Report: {report_file}")
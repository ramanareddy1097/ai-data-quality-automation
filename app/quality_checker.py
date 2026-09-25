import re

import pandas as pd


EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def check_data_quality(file_path: str):

    df = pd.read_csv(file_path)

    issues = []

    # 1. Missing customer IDs
    missing_customer_ids = df["customer_id"].isna().sum()

    if missing_customer_ids > 0:
        issues.append({
            "issue": "Missing customer_id",
            "records_affected": int(missing_customer_ids),
            "severity": "HIGH"
        })

    # 2. Invalid emails
    invalid_emails = (
        ~df["email"]
        .fillna("")
        .str.match(EMAIL_PATTERN)
    ).sum()

    if invalid_emails > 0:
        issues.append({
            "issue": "Invalid email address",
            "records_affected": int(invalid_emails),
            "severity": "MEDIUM"
        })

    # 3. Negative amounts
    negative_amounts = (df["amount"] < 0).sum()

    if negative_amounts > 0:
        issues.append({
            "issue": "Negative transaction amount",
            "records_affected": int(negative_amounts),
            "severity": "HIGH"
        })

    # 4. Invalid statuses
    valid_statuses = {
        "COMPLETED",
        "PENDING",
        "FAILED",
        "REFUNDED"
    }

    invalid_statuses = (
        ~df["status"].isin(valid_statuses)
    ).sum()

    if invalid_statuses > 0:
        issues.append({
            "issue": "Invalid transaction status",
            "records_affected": int(invalid_statuses),
            "severity": "MEDIUM"
        })

    # 5. Duplicate transactions
    duplicates = (
        df["transaction_id"]
        .duplicated()
        .sum()
    )

    if duplicates > 0:
        issues.append({
            "issue": "Duplicate transaction",
            "records_affected": int(duplicates),
            "severity": "HIGH"
        })

    # Calculate quality score
    total_issues = sum(
        issue["records_affected"]
        for issue in issues
    )

    total_records = len(df)

    issue_rate = (
        total_issues / total_records
        if total_records > 0
        else 0
    )

    quality_score = max(
        0,
        round(100 - (issue_rate * 100), 2)
    )

    return {
        "file": str(file_path),
        "total_records": total_records,
        "quality_score": quality_score,
        "issues": issues
    }


if __name__ == "__main__":

    file = "data/incoming/transactions_bad.csv"

    result = check_data_quality(file)

    print("\nDATA QUALITY REPORT")
    print("=" * 50)

    print(f"File: {result['file']}")
    print(f"Records: {result['total_records']}")
    print(f"Quality Score: {result['quality_score']}%")

    print("\nIssues:")

    for issue in result["issues"]:
        print(
            f"- {issue['issue']} | "
            f"Records: {issue['records_affected']} | "
            f"Severity: {issue['severity']}"
        )
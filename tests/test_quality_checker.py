from app.quality_checker import check_data_quality


def test_bad_transaction_file():

    result = check_data_quality(
        "data/incoming/transactions_bad.csv"
    )

    assert result["total_records"] == 10010

    assert result["quality_score"] == 99.5

    assert len(result["issues"]) == 5


def test_issue_types():

    result = check_data_quality(
        "data/incoming/transactions_bad.csv"
    )

    issue_names = {
        issue["issue"]
        for issue in result["issues"]
    }

    assert "Missing customer_id" in issue_names
    assert "Invalid email address" in issue_names
    assert "Negative transaction amount" in issue_names
    assert "Invalid transaction status" in issue_names
    assert "Duplicate transaction" in issue_names
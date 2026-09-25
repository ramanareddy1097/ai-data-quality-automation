from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/sample/transactions.csv")
OUTPUT_FILE = Path("data/incoming/transactions_bad.csv")


def create_bad_data():
    df = pd.read_csv(INPUT_FILE)

    # Missing customer IDs
    df.loc[10:19, "customer_id"] = None

    # Invalid email addresses
    df.loc[20:29, "email"] = "invalid-email"

    # Negative transaction amounts
    df.loc[30:39, "amount"] = -100

    # Invalid statuses
    df.loc[40:49, "status"] = "UNKNOWN"

    # Duplicate records
    duplicates = df.iloc[50:60].copy()

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Created bad dataset: {OUTPUT_FILE}")
    print(f"Total records: {len(df)}")


if __name__ == "__main__":
    create_bad_data()
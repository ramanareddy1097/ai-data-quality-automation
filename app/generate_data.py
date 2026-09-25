from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


fake = Faker()

OUTPUT_FILE = Path("data/sample/transactions.csv")

ROWS = 10000


def generate_data():
    rows = []

    statuses = ["COMPLETED", "PENDING", "FAILED", "REFUNDED"]
    countries = ["US", "CA", "UK", "IN", "DE"]

    start_date = datetime(2026, 1, 1)

    for i in range(ROWS):
        transaction_id = f"TXN-{i + 1:07d}"

        transaction_date = start_date + timedelta(
            days=random.randint(0, 250)
        )

        amount = round(random.uniform(10, 5000), 2)

        row = {
            "transaction_id": transaction_id,
            "customer_id": f"CUST-{random.randint(1, 3000):05d}",
            "customer_name": fake.name(),
            "email": fake.email(),
            "transaction_date": transaction_date.strftime("%Y-%m-%d"),
            "amount": amount,
            "currency": "USD",
            "country": random.choice(countries),
            "status": random.choice(statuses),
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Created {len(df)} records.")
    print(f"File: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_data()